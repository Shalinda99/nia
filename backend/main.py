import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import HOST, PORT, CORS_ORIGINS, LOG_LEVEL, ASSEMBLYAI_API_KEY, GROQ_API_KEY
from database import get_all_patients_summary, find_patient
from llm_handler import get_llm_handler
from rag_engine import get_rag_engine
from voice_handler import AssemblyAITranscriber, get_tts_handler

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Nia API...")
    logger.info("Initializing RAG engine...")
    get_rag_engine()
    logger.info("Initializing LLM handler...")
    try:
        get_llm_handler()
    except ValueError as e:
        logger.error(f"LLM init failed: {e}")
    logger.info("Initializing TTS handler...")
    get_tts_handler()
    logger.info("Nia API ready.")
    yield
    logger.info("Nia API shutting down.")


app = FastAPI(
    title="Nia Clinical AI",
    description="Hands-free AI voice assistant for clinical nurses powered by AssemblyAI",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VoiceSession:
    def __init__(self, session_id: str, websocket: WebSocket, loop: asyncio.AbstractEventLoop):
        self.session_id = session_id
        self.websocket = websocket
        self.loop = loop
        self.conversation_history = []
        self.transcriber: AssemblyAITranscriber = None
        self.is_processing = False
        self.current_patient_id = None

    async def start(self):
        self.transcriber = AssemblyAITranscriber(
            on_final=self._on_final_transcript,
            on_error=self._on_stt_error,
            loop=self.loop,
        )
        self.transcriber.connect()
        await self.send({"type": "session_started", "session_id": self.session_id})

    async def send(self, data: dict):
        try:
            await self.websocket.send_json(data)
        except Exception as e:
            logger.error(f"[{self.session_id}] WebSocket send error: {e}")

    def feed_audio(self, audio_bytes: bytes):
        if self.transcriber and not self.is_processing:
            self.transcriber.stream(audio_bytes)

    def start_utterance(self):
        if self.transcriber and not self.is_processing:
            self.transcriber.start_utterance()

    async def end_utterance(self):
        if self.transcriber and not self.is_processing:
            await self.transcriber.end_utterance()

    async def _on_final_transcript(self, text: str):
        if self.is_processing:
            return

        self.is_processing = True
        await self.send({"type": "transcript_final", "text": text})
        await self.send({"type": "processing"})

        try:
            llm = get_llm_handler()
            tts = get_tts_handler()

            called_tools = []

            def on_tool_call(tool_name: str, args: dict):
                called_tools.append({"tool": tool_name, "args": args})
                asyncio.run_coroutine_threadsafe(
                    self.send({"type": "tool_called", "tool": tool_name, "args": args}),
                    self.loop,
                )
                if tool_name in ("get_patient_info", "get_vital_signs", "get_medications", "get_lab_results", "get_upcoming_medications", "get_pending_orders"):
                    identifier = args.get("patient_identifier", "")
                    patient = find_patient(identifier)
                    if patient:
                        asyncio.run_coroutine_threadsafe(
                            self.send({"type": "patient_updated", "patient": {
                                "id": patient["id"],
                                "name": patient["name"],
                                "room": patient["room"],
                                "diagnosis": patient["diagnosis"],
                                "attending": patient["attending"],
                                "code_status": patient["code_status"],
                                "fall_risk": patient["fall_risk"],
                                "isolation": patient["isolation"],
                                "allergies": patient["allergies"],
                            }}),
                            self.loop,
                        )

            response_text = await llm.process(
                user_text=text,
                conversation_history=self.conversation_history,
                on_tool_call=on_tool_call,
            )

            self.conversation_history.append({"role": "user", "content": text})
            self.conversation_history.append({"role": "assistant", "content": response_text})

            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]

            audio_b64 = None
            if tts.has_tts:
                loop = asyncio.get_event_loop()
                audio_b64 = await loop.run_in_executor(None, tts.synthesize, response_text)

            await self.send({
                "type": "agent_response",
                "text": response_text,
                "audio": audio_b64,
                "tools_used": called_tools,
            })

        except Exception as e:
            logger.error(f"[{self.session_id}] Processing error: {e}", exc_info=True)
            await self.send({
                "type": "agent_response",
                "text": "I encountered an error processing your request. Please try again.",
                "audio": None,
            })
        finally:
            self.is_processing = False

    async def _on_stt_error(self, message: str):
        await self.send({"type": "error", "message": f"Speech recognition error: {message}"})

    def cleanup(self):
        if self.transcriber:
            self.transcriber.close()
        logger.info(f"Session {self.session_id} cleaned up")


active_sessions: Dict[str, VoiceSession] = {}


@app.websocket("/ws/voice")
async def voice_websocket(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())[:8]
    loop = asyncio.get_event_loop()
    session = VoiceSession(session_id, websocket, loop)
    active_sessions[session_id] = session

    logger.info(f"New voice session: {session_id}")

    try:
        await session.start()

        while True:
            message = await websocket.receive()

            if message["type"] == "websocket.disconnect":
                break

            if "bytes" in message and message["bytes"]:
                session.feed_audio(message["bytes"])

            elif "text" in message and message["text"]:
                try:
                    data = json.loads(message["text"])
                    msg_type = data.get("type", "")

                    if msg_type == "utterance_start":
                        session.start_utterance()
                        await session.send({"type": "listening"})

                    elif msg_type == "utterance_end":
                        await session.end_utterance()

                    elif msg_type == "ping":
                        await session.send({"type": "pong"})

                    elif msg_type == "clear_history":
                        session.conversation_history = []
                        await session.send({"type": "history_cleared"})

                    elif msg_type == "switch_patient":
                        patient_id = data.get("patient_id", "")
                        patient = find_patient(patient_id)
                        if patient:
                            session.current_patient_id = patient["id"]
                            await session.send({
                                "type": "patient_updated",
                                "patient": {
                                    "id": patient["id"],
                                    "name": patient["name"],
                                    "room": patient["room"],
                                    "diagnosis": patient["diagnosis"],
                                    "attending": patient["attending"],
                                    "code_status": patient["code_status"],
                                    "fall_risk": patient["fall_risk"],
                                    "isolation": patient["isolation"],
                                    "allergies": patient["allergies"],
                                },
                            })

                    elif msg_type == "text_input":
                        text = data.get("text", "").strip()
                        if text and not session.is_processing:
                            await session._on_final_transcript(text)

                    elif msg_type == "get_patients":
                        patients = get_all_patients_summary()
                        await session.send({"type": "patients_list", "patients": patients})

                except json.JSONDecodeError:
                    pass

    except WebSocketDisconnect:
        logger.info(f"Session {session_id} disconnected")
    except Exception as e:
        logger.error(f"Session {session_id} error: {e}", exc_info=True)
    finally:
        session.cleanup()
        active_sessions.pop(session_id, None)


@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "service": "Nia Clinical AI",
        "version": "1.0.0",
        "assemblyai_configured": bool(ASSEMBLYAI_API_KEY),
        "groq_configured": bool(GROQ_API_KEY),
        "active_sessions": len(active_sessions),
    })


@app.get("/api/patients")
async def list_patients():
    return JSONResponse({"patients": get_all_patients_summary()})


@app.get("/api/patients/{patient_id}")
async def get_patient(patient_id: str):
    patient = find_patient(patient_id)
    if not patient:
        return JSONResponse({"error": "Patient not found"}, status_code=404)
    safe = {k: v for k, v in patient.items() if k != "notes"}
    return JSONResponse(safe)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False, log_level=LOG_LEVEL.lower())
