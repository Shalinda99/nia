import { useCallback, useEffect, useRef } from 'react';
import { AlertCircle, Trash2, Info, Zap } from 'lucide-react';
import Header from './components/Header';
import VoiceOrb from './components/VoiceOrb';
import TranscriptPanel from './components/TranscriptPanel';
import PatientPanel from './components/PatientPanel';
import QuickActions from './components/QuickActions';
import { useVoiceAgent, AgentStatus } from './hooks/useVoiceAgent';

function ErrorBanner({ message, onDismiss }) {
  if (!message) return null;
  return (
    <div className="mx-4 mt-2 flex items-center gap-2 px-4 py-2.5 rounded-xl bg-red-950/60 border border-red-800/50 text-red-300 text-sm">
      <AlertCircle size={16} className="flex-shrink-0" />
      <span className="flex-1">{message}</span>
      <button onClick={onDismiss} className="text-red-500 hover:text-red-300 text-xs underline">
        Dismiss
      </button>
    </div>
  );
}

function ToolActivity({ toolsUsed }) {
  if (!toolsUsed || toolsUsed.length === 0) return null;
  const toolNames = {
    get_patient_info: 'Patient Info',
    get_vital_signs: 'Vitals',
    get_medications: 'Medications',
    get_lab_results: 'Lab Results',
    get_upcoming_medications: 'Upcoming Meds',
    get_pending_orders: 'Orders',
    add_nursing_note: 'Adding Note',
    search_clinical_protocols: 'Protocols',
    list_all_patients: 'Patient List',
  };
  return (
    <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-purple-950/40 border border-purple-800/30">
      <Zap size={11} className="text-purple-400" />
      <span className="text-[10px] text-purple-300">
        {toolsUsed.map(t => toolNames[t.tool] || t.tool).join(' → ')}
      </span>
    </div>
  );
}

export default function App() {
  const {
    status,
    isActive,
    isCapturing,
    partialTranscript,
    messages,
    currentPatient,
    toolsUsed,
    volume,
    error,
    sessionId,
    activate,
    deactivate,
    clearHistory,
    sendWs,
  } = useVoiceAgent();

  const transcriptEndRef = useRef(null);

  useEffect(() => {
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, partialTranscript]);

  const handleQuickPrompt = useCallback((prompt) => {
    if (!isActive) return;
    sendWs({ type: 'text_input', text: prompt });
  }, [isActive, sendWs]);

  const isProcessingOrSpeaking = status === AgentStatus.PROCESSING || status === AgentStatus.SPEAKING;

  return (
    <div className="flex flex-col h-screen bg-slate-950 overflow-hidden">
      <Header status={status} sessionId={sessionId} isActive={isActive} />

      <ErrorBanner message={error} onDismiss={() => {}} />

      <div className="flex flex-1 overflow-hidden gap-0">
        <aside className="w-72 flex-shrink-0 border-r border-slate-700/40 flex flex-col overflow-hidden bg-slate-950/50">
          <div className="flex-shrink-0 p-4 border-b border-slate-700/30">
            <VoiceOrb
              status={status}
              isActive={isActive}
              volume={volume}
              onActivate={activate}
              onDeactivate={deactivate}
            />
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <QuickActions
              onPrompt={handleQuickPrompt}
              disabled={!isActive || isProcessingOrSpeaking}
            />

            {toolsUsed.length > 0 && (
              <div className="space-y-1.5">
                <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Tools</p>
                <ToolActivity toolsUsed={toolsUsed} />
              </div>
            )}

            <div className="mt-2 rounded-xl border border-slate-700/30 bg-slate-900/40 p-3 space-y-2">
              <div className="flex items-center gap-1.5 mb-1">
                <Info size={11} className="text-slate-500" />
                <span className="text-[10px] text-slate-500 uppercase font-semibold tracking-wider">Example Commands</span>
              </div>
              {[
                '"What are John Smith\'s vitals?"',
                '"List medications due in the next hour"',
                '"What\'s the sepsis protocol?"',
                '"Add a note: patient tolerated lunch well"',
                '"What are Garcia\'s critical labs?"',
              ].map((ex, i) => (
                <p key={i} className="text-[11px] text-slate-600 leading-relaxed">
                  {ex}
                </p>
              ))}
            </div>
          </div>
        </aside>

        <main className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-y-auto p-5" ref={transcriptEndRef}>
            <TranscriptPanel
              messages={messages}
              status={status}
            />
          </div>

          <div className="flex-shrink-0 px-5 py-3 border-t border-slate-700/30 flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <span>Powered by</span>
              <span className="font-semibold text-slate-500">AssemblyAI</span>
              <span className="text-slate-700">×</span>
              <span className="font-semibold text-slate-500">Groq</span>
            </div>
            {messages.length > 0 && (
              <button
                onClick={clearHistory}
                className="flex items-center gap-1.5 text-xs text-slate-600 hover:text-red-400 transition-colors"
              >
                <Trash2 size={12} />
                Clear
              </button>
            )}
          </div>
        </main>

        <aside className="w-72 flex-shrink-0 border-l border-slate-700/40 flex flex-col overflow-hidden bg-slate-950/50">
          <div className="flex-shrink-0 px-4 py-3 border-b border-slate-700/30">
            <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Patient Context</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            <PatientPanel patient={currentPatient} />
          </div>

          {isActive && (
            <div className="flex-shrink-0 p-4 border-t border-slate-700/30 space-y-2">
              <div className="rounded-lg bg-emerald-950/40 border border-emerald-800/30 p-3">
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-semibold text-emerald-400">Session Active</span>
                </div>
                <p className="text-[11px] text-slate-500">
                  Hands-free mode enabled. Speak naturally and Nia will respond.
                </p>
              </div>
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}
