# 🏥 Nia — Clinical AI Nursing Assistant

> **Hands-free, real-time AI voice agent for nurses built on AssemblyAI**
> 
> lablab.ai × AssemblyAI Hackathon 2026

[![AssemblyAI](https://img.shields.io/badge/Powered%20by-AssemblyAI-purple)](https://www.assemblyai.com)
[![Groq](https://img.shields.io/badge/LLM-Groq%20llama--3.3--70b-orange)](https://groq.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB)](https://react.dev)

---

## 🎯 What is Nia?

Nia is a **hands-free AI voice agent** that lets nurses query patient data, retrieve clinical protocols, and document notes — all by speaking naturally, without touching a screen.

**Voice flow:** `Speak → AssemblyAI STT → Groq LLM + Tools + RAG → ElevenLabs TTS → Nurse hears response`

### Example interactions:
- *"What are Maria Garcia's critical lab values?"* → Flags CRITICAL lactate 3.2
- *"List John Smith's medications due in the next hour"* → Returns upcoming MAR
- *"Walk me through the sepsis 1-hour bundle"* → RAG retrieves Surviving Sepsis protocol  
- *"Add a note to Brown's chart: patient tolerated PT well"* → Adds note, confirms verbally

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Microphone-enabled device with a modern browser (Chrome recommended)

### 1. Get API Keys

| Service | URL | Required |
|---------|-----|----------|
| AssemblyAI | https://www.assemblyai.com/dashboard | ✅ Yes |
| Groq | https://console.groq.com | ✅ Yes (free) |
| ElevenLabs | https://elevenlabs.io | ⬜ Optional (TTS quality) |

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run the backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend API will be at `http://localhost:8000`  
Health check: `http://localhost:8000/health`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be at `http://localhost:5173`

### 4. Use Nia

1. Open `http://localhost:5173` in Chrome
2. Click the **green orb** to activate
3. Allow microphone access when prompted
4. Start speaking naturally!

---

## 🏗️ Project Structure

```
lablab_AI/
├── backend/
│   ├── main.py               # FastAPI server + WebSocket endpoint
│   ├── voice_handler.py      # AssemblyAI Realtime STT + ElevenLabs TTS
│   ├── llm_handler.py        # Groq LLM with tool calling (max 5 iterations)
│   ├── clinical_tools.py     # 9 clinical tool definitions + execution
│   ├── rag_engine.py         # BM25 RAG over clinical documents
│   ├── database.py           # Mock EHR (5 patients with full clinical data)
│   ├── config.py             # Environment configuration
│   ├── requirements.txt
│   ├── .env.example
│   └── data/
│       ├── clinical_protocols.txt    # Sepsis, Fall, Code Blue, Pain protocols
│       ├── medication_guidelines.txt # Cardiac, ABx, insulin, vasopressors
│       └── nursing_procedures.txt    # IV care, vitals, SBAR, wound care
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                      # Main layout (3-panel)
│   │   ├── components/
│   │   │   ├── Header.jsx               # Status bar + session info
│   │   │   ├── VoiceOrb.jsx             # Animated mic button + waveform
│   │   │   ├── TranscriptPanel.jsx      # Real-time conversation display
│   │   │   ├── PatientPanel.jsx         # Patient context sidebar
│   │   │   └── QuickActions.jsx         # One-tap common queries
│   │   ├── hooks/
│   │   │   ├── useVoiceAgent.js         # WebSocket + session state
│   │   │   └── useAudioCapture.js       # AudioWorklet + VAD
│   │   └── services/
│   │       └── ttsService.js            # ElevenLabs + browser TTS
│   └── public/
│       └── audio-processor.worklet.js  # PCM16 conversion + RMS VAD
│
└── presentation/
    ├── PITCH_DECK.md       # Full hackathon pitch
    ├── ARCHITECTURE.md     # Technical deep-dive
    └── DEMO_GUIDE.md       # Step-by-step demo script
```

---

## 🔧 Clinical Tools Available

| Tool | Description |
|------|-------------|
| `get_patient_info` | Demographics, diagnosis, allergies, code status |
| `get_vital_signs` | BP, HR, RR, Temp, SpO2, weight trending |
| `get_medications` | Full MAR with next-due times |
| `get_lab_results` | Labs with critical value detection |
| `get_upcoming_medications` | Meds due within N hours |
| `get_pending_orders` | Active physician orders |
| `add_nursing_note` | Voice-to-chart documentation |
| `search_clinical_protocols` | BM25 RAG over clinical guidelines |
| `list_all_patients` | Unit-wide patient summary |

---

## 🧪 Mock Patients

| ID | Name | Room | Diagnosis |
|----|------|------|-----------|
| P001 | John Smith | 204A | CHF Exacerbation |
| P002 | Maria Garcia | 312B | Sepsis (ESBL UTI) ⚠️ |
| P003 | Robert Johnson | 108C | Post-op L Hip Arthroplasty |
| P004 | Dorothy Williams | 515A | Ischemic Stroke (DNR/DNI) |
| P005 | Thomas Brown | 220B | COPD Exacerbation |

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

Services:
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

---

## 🔒 Environment Variables

```env
# Required
ASSEMBLYAI_API_KEY=your_key
GROQ_API_KEY=your_key

# Optional (browser TTS used as fallback)
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ws/voice` | WebSocket | Main voice agent connection |
| `/health` | GET | Health check + API key status |
| `/api/patients` | GET | List all mock patients |
| `/api/patients/{id}` | GET | Get specific patient data |

---

## 🏆 Hackathon Alignment

This project uses the **Realtime STT API** path:
- ✅ AssemblyAI Realtime STT (Universal-3 model) for sub-second transcription
- ✅ Clinical word boost for medical terminology accuracy
- ✅ Custom LLM orchestration (Groq) with tool calling
- ✅ Custom TTS (ElevenLabs) with browser fallback
- ✅ Real clinical use case with measurable patient safety impact

---

## 📜 License

MIT License — built for the lablab.ai × AssemblyAI Hackathon 2026
