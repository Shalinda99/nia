# Nia — Technical Architecture

## Stack Overview

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + Vite | UI, audio capture, TTS playback |
| Styling | TailwindCSS | Clinical dark-mode UI |
| Backend | FastAPI (Python) | Async WebSocket server, session mgmt |
| STT | **AssemblyAI Realtime API** | Real-time speech → text |
| LLM | **Groq** (llama-3.3-70b) | Clinical reasoning + tool calling |
| RAG | BM25Okapi (rank_bm25) | Clinical protocol retrieval |
| TTS | ElevenLabs / Browser | Text → speech |
| Transport | WebSocket (binary + JSON) | Low-latency audio streaming |

---

## Data Flow

```
1. AUDIO CAPTURE
   Browser AudioWorklet
   → Float32 samples at 16kHz
   → Convert to PCM16 (Int16)
   → VAD filter (RMS threshold)
   → Binary WebSocket frame

2. STT PIPELINE
   FastAPI WebSocket receives binary audio
   → AssemblyAI RealtimeTranscriber.stream(bytes)
   → Partial transcripts → Frontend (display only)
   → Final transcript → LLM pipeline

3. LLM PIPELINE (async)
   Build messages: [system_prompt + conversation_history + user_query]
   → Groq API (tool_choice="auto")
   → If tool_calls: execute tools, append results, re-call LLM
   → Max 5 tool iterations (prevents infinite loops)
   → Final text response

4. TOOL EXECUTION
   Tool name + JSON args
   → clinical_tools.execute_tool()
   → database.find_patient() + relevant data retrieval
   → OR rag_engine.search() for protocols
   → JSON string result → appended to messages

5. TTS + RESPONSE
   Response text
   → ElevenLabs TTS (eleven_turbo_v2_5) → base64 MP3
   → OR browser speechSynthesis fallback
   → WebSocket JSON: {type: "agent_response", text, audio}
   → Frontend: AudioContext.decodeAudioData() → playback

6. PATIENT CONTEXT UPDATE
   When patient-related tool is called:
   → Frontend receives {type: "patient_updated", patient: {...}}
   → PatientPanel updates in real-time
```

---

## WebSocket Protocol

### Client → Server

| Message | Format | Description |
|---------|--------|-------------|
| Audio chunk | Binary (ArrayBuffer) | PCM16 audio at 16kHz |
| Ping | `{type: "ping"}` | Keepalive |
| Clear history | `{type: "clear_history"}` | Reset conversation |
| Switch patient | `{type: "switch_patient", patient_id}` | Manual patient select |
| Get patients | `{type: "get_patients"}` | List all patients |

### Server → Client

| Message | Description |
|---------|-------------|
| `session_started` | Session ID confirmed, AssemblyAI connected |
| `transcript_partial` | Live partial transcription |
| `transcript_final` | Committed final transcript |
| `processing` | LLM started processing |
| `tool_called` | Which tool was invoked (for UI display) |
| `agent_response` | Final response text + optional base64 audio |
| `patient_updated` | Patient data to display in sidebar |
| `error` | Error message |
| `pong` | Keepalive response |

---

## RAG Architecture

```
Clinical Documents (3 files, ~10,000 tokens)
    ├── clinical_protocols.txt   → Sepsis, Fall Prevention, Code Blue, Pain, Meds
    ├── medication_guidelines.txt → Cardiac, Antibiotics, Insulin, Vasopressors, Respiratory
    └── nursing_procedures.txt   → Vitals, IV Care, Glucose, Foley, Wound Care, SBAR

       ↓ load at startup
Section splitting (by ===== headers)
       ↓
Paragraph chunking (max 1200 chars)
       ↓
BM25Okapi index (tokenized, lowercased)

At query time:
    query string
       ↓ tokenize
    BM25 score all chunks
       ↓ top-3 by score
    Concatenate with [Source] labels
       ↓
    Append to LLM context
```

**Why BM25 over vector embeddings?**
- Zero dependencies on external embedding models or vector DBs
- Instant startup (no model download)
- Highly effective for keyword-rich clinical text
- Deterministic results (reproducible for demos)

---

## Security Considerations

- API keys stored in `.env` file (never committed to git)
- WebSocket connections session-isolated (no cross-session data leakage)
- Patient data is mock only — real deployment requires HIPAA BAA
- HTTPS/WSS required for production (TLS termination at load balancer)
- Rate limiting should be added at the API gateway layer
- Conversation history capped at 40 messages per session

---

## Scalability Path

```
Current (Hackathon):          Production:
SQLite mock data         →    FHIR R4 API (Epic, Cerner)
Single FastAPI process   →    Kubernetes + horizontal scaling
In-memory RAG            →    Pinecone / Weaviate vector DB
BM25 retrieval           →    Hybrid BM25 + dense vector search
ElevenLabs batch TTS     →    ElevenLabs streaming TTS
Browser VAD              →    Silero VAD (on-device ML)
```
