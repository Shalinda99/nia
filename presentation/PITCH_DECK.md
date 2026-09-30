# Nia — AI Clinical Nursing Assistant
### Hackathon Pitch Deck | lablab.ai × AssemblyAI Challenge

---

## 🏥 The Problem

**Nurses are drowning in information retrieval tasks while patients need hands-on care.**

- Nurses spend **35% of their shift** on documentation and data lookup — not patient care
- Clinical environments are loud, fast-paced, and hands-contaminated (gloves, patient contact)
- Accessing EHR systems requires multiple clicks, logins, and screen interactions
- Critical information (allergies, drug interactions, protocols) takes too long to surface
- Nurse burnout is at an all-time high — **40% plan to leave** the profession

---

## 💡 The Solution: Nia

**A hands-free, real-time AI voice assistant built for nurses at the bedside.**

Nurses activate Nia and simply *speak* — the AI handles everything:

```
Nurse says: "What are Smith's latest vitals and any critical labs?"

Nia responds (in 2 seconds):
"John Smith in room 204A — latest BP is 140 over 82, heart rate 80,
SpO2 97%. Labs from 6 AM show potassium 3.4, mildly low.
BNP is 1,240 — still elevated but trending down. No critical values."
```

**Zero typing. Zero clicking. Zero screen touching.**

---

## 🎯 Key Features

### 🎤 Real-Time Voice Interaction
- Continuous hands-free listening with VAD (Voice Activity Detection)
- Sub-second transcription via **AssemblyAI Universal-3 Pro**
- Natural turn-taking — speaks when nurse finishes talking

### 🧠 Intelligent Clinical Understanding
- **Groq LLM (llama-3.3-70b)** for fast clinical reasoning
- Understands clinical terminology, abbreviations, patient names
- Multi-turn conversation with full context memory

### 🔧 Clinical Tool Calling (9 Tools)
| Tool | Description |
|------|-------------|
| `get_patient_info` | Demographics, diagnosis, allergies, code status |
| `get_vital_signs` | Recent BP, HR, RR, Temp, SpO2 with trend |
| `get_medications` | MAR with next due times and last given |
| `get_lab_results` | Labs with critical value flagging |
| `get_upcoming_medications` | Meds due in next 1-2 hours |
| `get_pending_orders` | Active and pending physician orders |
| `add_nursing_note` | Voice-to-chart documentation |
| `search_clinical_protocols` | RAG over clinical guidelines |
| `list_all_patients` | Unit-wide patient overview |

### 📚 Clinical RAG Knowledge Base
- Sepsis protocol (Surviving Sepsis Campaign)
- Fall prevention & Braden/Morse scales
- Pressure injury staging (NPUAP)
- Code Blue / Rapid Response protocol
- Pain assessment & opioid safety
- Medication administration (5 rights)
- Common medication reference (cardiac, antibiotics, insulin)
- Nursing procedures (IV care, CAUTI bundle, SBAR)

### 🔊 Voice Output
- **ElevenLabs TTS** for natural clinical-grade speech
- Automatic browser TTS fallback (no API key required)
- Optimized for clinical clarity

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NURSE (Bedside)                          │
│                         │                                   │
│              🎤 Speaks naturally                            │
└─────────────────────────│───────────────────────────────────┘
                          │ Audio (PCM16, 16kHz)
                          ▼ WebSocket
┌─────────────────────────────────────────────────────────────┐
│               React Frontend (Vite + TailwindCSS)           │
│  • AudioWorklet → PCM16 conversion                         │
│  • VAD (Voice Activity Detection)                           │
│  • Real-time transcript display                             │
│  • Patient context panel                                    │
│  • TTS playback (ElevenLabs or browser)                    │
└─────────────────────────│───────────────────────────────────┘
                          │ Binary WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Python)                      │
│  • WebSocket session manager                               │
│  • Async LLM processing pipeline                           │
│  • Tool execution engine                                    │
│  • Conversation history per session                        │
└──────┬─────────────────┬────────────────────────────────────┘
       │                 │                    │
       ▼                 ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
│  AssemblyAI  │  │  Groq LLM    │  │   ElevenLabs TTS     │
│  Realtime    │  │  llama-3.3   │  │   (eleven_turbo_v2)  │
│  STT (U-3)   │  │  70b-versatile│  │                      │
└──────────────┘  └──────┬───────┘  └──────────────────────┘
                         │ Tool Calls
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Clinical Data Layer                        │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  Patient Database │  │  BM25 RAG Engine                 │ │
│  │  (5 patients with │  │  • Clinical protocols            │ │
│  │  full mock EHR)   │  │  • Medication guidelines         │ │
│  │                   │  │  • Nursing procedures            │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎬 Demo Scenarios

### Scenario 1: Critical Lab Alert
> "What are Maria Garcia's lab results?"
→ AI identifies CRITICAL lactate 3.2 and flags it immediately

### Scenario 2: Medication Management
> "What medications does John Smith have due in the next 2 hours?"
→ Returns upcoming meds with times, checking against allergy list

### Scenario 3: Clinical Protocol
> "Walk me through the sepsis 1-hour bundle"
→ RAG retrieves Surviving Sepsis Campaign protocol, AI speaks it concisely

### Scenario 4: Voice Documentation
> "Add a note for Thomas Brown: patient tolerated PT session well, ambulated 30 feet"
→ Note added to patient chart, confirmed verbally

### Scenario 5: Code Blue
> "What do I do for a code blue?"
→ AI immediately provides BLS/ACLS steps in priority order

---

## 📊 Impact Metrics (Estimated)

| Metric | Before Nia | With Nia |
|--------|-----------------|----------------|
| Time to retrieve patient vitals | 45-90 seconds | **< 5 seconds** |
| Protocol lookup time | 3-5 minutes | **< 10 seconds** |
| Documentation time per note | 4-6 minutes | **< 60 seconds** |
| Hands touching screen/keyboard | Multiple times/hour | **Zero** |
| Medication error risk | Baseline | **Reduced** (allergy check) |

---

## 🚀 Why Nia Wins

1. **Real clinical use case** — addresses a proven pain point in healthcare
2. **AssemblyAI-native** — uses Realtime STT as core voice infrastructure
3. **Production-ready** — full async WebSocket pipeline, session management, error handling
4. **Extensible** — plug into real EHR systems (Epic, Cerner) via FHIR API
5. **Safe by design** — critical value alerts, allergy checks, "verify with physician" guardrails
6. **Hands-free** — VAD enables truly touchless operation for sterile environments

---

## 🔮 Roadmap

- **Phase 1** (now): Voice agent with mock EHR data
- **Phase 2**: FHIR API integration with real hospital EHR systems
- **Phase 3**: Wake word detection ("Hey Nia")
- **Phase 4**: HIPAA-compliant cloud deployment with AES-256 encryption
- **Phase 5**: Multi-nurse unit dashboard, escalation alerts, shift handoff summaries

---

## 👥 Team

Built for **lablab.ai × AssemblyAI Hackathon 2026**

*"Give nurses their hands back. Let them focus on patients, not screens."*
