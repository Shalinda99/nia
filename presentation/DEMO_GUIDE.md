# Nia Demo Guide

## Pre-Demo Checklist
- [ ] Backend running: `cd backend && uvicorn main:app --reload`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Browser open at `http://localhost:5173`
- [ ] Microphone permission granted in browser
- [ ] Speaker/headphone connected for TTS output
- [ ] Browser tab audio unmuted

---

## Demo Flow (10 minutes)

### Opening (1 min)
> "Imagine you're a nurse at 2am. Three critical patients. You need vitals, lab results, and you have to document everything — all while wearing gloves, moving between rooms. That's the reality today.
>
> Nia changes that. Completely hands-free, powered by AssemblyAI."

**[Click the green orb to activate]**

---

### Scene 1: Patient Lookup (2 min)

**Say:** *"Who are my patients on the unit right now?"*
> Agent lists all 5 patients with rooms and diagnoses

**Say:** *"Tell me about John Smith in room 204A"*
> Agent returns demographics, diagnosis, allergies, code status

**Say:** *"What are his latest vital signs?"*
> Agent returns trending vitals, notes improving SpO2

**[Point to the Patient Context panel updating in real-time]**

---

### Scene 2: Critical Lab Alert (2 min)

**Say:** *"Show me Maria Garcia's lab results"*
> Agent flags: CRITICAL LACTATE 3.2, CRITICAL GLUCOSE 312, HIGH WBC 18.4

**Say:** *"Based on her labs, what should I do for suspected sepsis?"*
> Agent recalls the Surviving Sepsis protocol via RAG:
> - Blood cultures x2 before antibiotics
> - 30mL/kg IV bolus
> - Broad-spectrum antibiotics within 1 hour
> - Lactate trending

**[Highlight: real-time tool call display showing which tools were used]**

---

### Scene 3: Medication Safety (2 min)

**Say:** *"What medications does John Smith have due in the next 2 hours?"*
> Agent lists upcoming meds with times, also notes allergies (Penicillin, Aspirin)

**Say:** *"He's allergic to Penicillin — is any of his current medication a problem?"*
> Agent reviews med list and confirms no penicillin-class drugs are prescribed

**Say:** *"What do I need to know about furosemide?"*
> Agent pulls from medication guidelines RAG: monitoring K+, slow IV push rate, ototoxicity risk

---

### Scene 4: Voice Documentation (1 min)

**Say:** *"Add a note to Thomas Brown's chart: Patient tolerated physical therapy session well. Ambulated 30 feet with walker and minimal assistance. Hip precautions maintained."*
> Agent confirms: "Note added to Thomas Brown's chart at [time]."

**[Show the note added to the patient record]**

---

### Scene 5: Emergency Protocol (1 min)

**Say:** *"A patient has no pulse. What do I do right now?"*
> Agent immediately:
> 1. "CALL A CODE — activate code blue now"
> 2. Provides BLS steps: Start CPR 30:2, get AED, assign roles
> 3. Gives ACLS algorithm overview

---

### Closing (1 min)

> "With Nia, nurses can retrieve any patient information in under 3 seconds — completely hands-free.
>
> This is built on AssemblyAI's Realtime STT for sub-second transcription, Groq's llama-3.3-70b for clinical reasoning, and a RAG knowledge base of clinical protocols.
>
> The next step is FHIR integration with Epic and Cerner — bringing this to real hospitals."

---

## Sample Prompts Reference

| Category | What to Say |
|----------|-------------|
| Patient | "Tell me about patient P002" |
| Vitals | "What are Dorothy Williams' vitals?" |
| Meds | "What meds does Brown have due now?" |
| Labs | "Show Garcia's critical labs" |
| Protocol | "What's the sepsis protocol?" |
| Protocol | "How do I prevent pressure injuries?" |
| Protocol | "Walk me through SBAR" |
| Drug Info | "Tell me about vancomycin" |
| Document | "Add a note to Smith: BP improving, patient resting" |
| Orders | "What are the pending orders for Johnson?" |
| Emergency | "Code blue — what do I do?" |
| Overview | "List all patients on the unit" |

---

## Troubleshooting

**"No audio being captured"**
- Allow microphone permission in browser (address bar lock icon)
- Check that no other app is using the microphone

**"Connection error"**
- Verify backend is running: `curl http://localhost:8000/health`
- Check `.env` file has valid `ASSEMBLYAI_API_KEY` and `GROQ_API_KEY`

**"Agent not responding to voice"**
- Speak clearly, close to the microphone
- Wait for "Ready" status (green orb) before speaking
- Check the partial transcript is appearing (if yes, STT works — issue may be LLM)

**"Browser TTS sounds robotic"**
- Add `ELEVENLABS_API_KEY` to `.env` for natural voice output
- Or adjust browser TTS voice in system settings
