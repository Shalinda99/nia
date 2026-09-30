import asyncio
import base64
import logging
from typing import Callable, Optional

import assemblyai as aai
from config import ASSEMBLYAI_API_KEY, AUDIO_SAMPLE_RATE

logger = logging.getLogger(__name__)

aai.settings.api_key = ASSEMBLYAI_API_KEY

CLINICAL_KEYTERMS = [
    "patient", "medication", "vitals", "blood pressure", "heart rate",
    "oxygen saturation", "temperature", "nurse", "physician", "allergy",
    "protocol", "sepsis", "insulin", "heparin", "milligrams", "micrograms",
    "furosemide", "metoprolol", "vancomycin", "meropenem", "norepinephrine",
]


class AssemblyAITranscriber:
    """
    Wraps AssemblyAI DictationTranscriber (SDK 1.x).
    One DictationLiveSession is opened per utterance.
    Utterance boundaries are signaled by the caller (frontend VAD).
    """

    def __init__(
        self,
        on_final: Callable[[str], None],
        on_error: Optional[Callable[[str], None]] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self.on_final = on_final
        self.on_error = on_error
        self.loop = loop or asyncio.get_event_loop()
        self._transcriber: Optional[aai.DictationTranscriber] = None
        self._session = None
        self._utterance_active = False
        self._config = aai.DictationConfig(
            sample_rate=AUDIO_SAMPLE_RATE,
            channels=1,
            keyterms_prompt=CLINICAL_KEYTERMS,
        )

    def connect(self):
        self._transcriber = aai.DictationTranscriber(api_key=ASSEMBLYAI_API_KEY)
        self._transcriber.__enter__()
        logger.info("AssemblyAI DictationTranscriber initialized")

    def start_utterance(self):
        """Open a new dictation session — called when VAD detects speech start."""
        if self._utterance_active:
            return
        if not self._transcriber:
            logger.warning("Transcriber not initialized")
            return
        try:
            self._session = self._transcriber.open_live(self._config)
            self._utterance_active = True
            logger.debug("Utterance session opened")
        except Exception as e:
            logger.error(f"Failed to open dictation session: {e}")

    def stream(self, audio_bytes: bytes):
        """Feed audio bytes into the active dictation session."""
        if self._session and self._utterance_active:
            try:
                self._session.write(audio_bytes)
            except Exception as e:
                logger.error(f"Error writing audio to dictation session: {e}")

    async def end_utterance(self):
        """Close session, await transcript, fire on_final — called when VAD detects silence."""
        if not self._utterance_active or not self._session:
            return
        self._utterance_active = False
        session = self._session
        self._session = None
        try:
            result = await asyncio.get_event_loop().run_in_executor(None, session.result)
            text = (result.final_text or "").strip() if result else ""
            if text:
                logger.info(f"Utterance transcript: {text!r}")
                await self.on_final(text)
            else:
                logger.debug("Empty utterance — skipping LLM")
        except Exception as e:
            logger.error(f"Dictation result error: {e}")
            if self.on_error:
                await self.on_error(f"Transcription error: {e}")

    def close(self):
        if self._session and not self._session.closed:
            try:
                self._session.abort()
            except Exception:
                pass
        self._session = None
        self._utterance_active = False
        if self._transcriber:
            try:
                self._transcriber.__exit__(None, None, None)
            except Exception:
                pass
            self._transcriber = None
        logger.info("AssemblyAI DictationTranscriber closed")

    @property
    def is_connected(self) -> bool:
        return self._transcriber is not None


class TTSHandler:
    def __init__(self):
        self._elevenlabs_available = False
        self._client = None
        self._voice_id = None
        self._setup_elevenlabs()

    def _setup_elevenlabs(self):
        from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
        if ELEVENLABS_API_KEY:
            try:
                from elevenlabs import ElevenLabs
                self._client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
                self._voice_id = ELEVENLABS_VOICE_ID
                self._elevenlabs_available = True
                logger.info("ElevenLabs TTS initialized")
            except ImportError:
                logger.warning("ElevenLabs package not installed — using browser TTS fallback")
            except Exception as e:
                logger.warning(f"ElevenLabs init failed: {e} — using browser TTS fallback")
        else:
            logger.info("No ElevenLabs API key — browser TTS will be used on frontend")

    def synthesize(self, text: str) -> Optional[str]:
        if not self._elevenlabs_available or not self._client:
            return None
        try:
            audio_generator = self._client.text_to_speech.convert(
                voice_id=self._voice_id,
                text=text,
                model_id="eleven_turbo_v2_5",
                output_format="mp3_44100_128",
            )
            audio_bytes = b"".join(audio_generator)
            return base64.b64encode(audio_bytes).decode("utf-8")
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            return None

    @property
    def has_tts(self) -> bool:
        return self._elevenlabs_available


_tts_handler: Optional[TTSHandler] = None


def get_tts_handler() -> TTSHandler:
    global _tts_handler
    if _tts_handler is None:
        _tts_handler = TTSHandler()
    return _tts_handler
