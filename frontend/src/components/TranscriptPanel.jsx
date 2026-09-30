import { MessageSquare, Mic } from 'lucide-react';
import { AgentStatus } from '../hooks/useVoiceAgent';

export default function TranscriptPanel({ messages, partialTranscript, status }) {
  const isListening = status === AgentStatus.LISTENING;
  const isProcessing = status === AgentStatus.PROCESSING;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 mb-3">
        <MessageSquare size={14} className="text-slate-400" />
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Conversation</span>
        {messages.length > 0 && (
          <span className="ml-auto text-xs text-slate-600">{messages.length} messages</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {messages.length === 0 && !isListening && (
          <div className="flex flex-col items-center justify-center h-full text-center py-8">
            <Mic size={28} className="text-slate-700 mb-3" />
            <p className="text-slate-600 text-sm">No conversation yet.</p>
            <p className="text-slate-700 text-xs mt-1">Activate the agent and start speaking.</p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600/30 border border-blue-500/30 text-blue-100 rounded-tr-sm'
                  : 'bg-slate-800/60 border border-slate-700/40 text-slate-200 rounded-tl-sm'
              }`}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-[10px] font-semibold uppercase tracking-wide ${
                  msg.role === 'user' ? 'text-blue-400' : 'text-clinical-400'
                }`}>
                  {msg.role === 'user' ? 'Nurse' : 'Nia AI'}
                </span>
                {msg.tools && msg.tools.length > 0 && (
                  <span className="text-[10px] text-purple-400 font-medium">
                    [{msg.tools.map(t => t.tool).join(', ')}]
                  </span>
                )}
              </div>
              <p>{msg.text}</p>
            </div>
          </div>
        ))}

        {isListening && (
          <div className="flex justify-end">
            <div className="rounded-2xl rounded-tr-sm px-4 py-2.5 bg-blue-600/20 border border-blue-500/20 border-dashed">
              <div className="text-[10px] font-semibold uppercase tracking-wide text-blue-500 mb-1.5">Nurse (speaking)</div>
              <div className="flex gap-1 items-end h-5">
                {[0.4, 0.7, 1, 0.7, 0.4, 0.6, 0.9, 0.5].map((h, i) => (
                  <div
                    key={i}
                    className="w-1 rounded-full bg-blue-400 bar-wave"
                    style={{ height: `${h * 100}%`, animationDelay: `${i * 0.1}s` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {isProcessing && (
          <div className="flex justify-start">
            <div className="rounded-2xl rounded-tl-sm px-4 py-2.5 bg-purple-900/30 border border-purple-700/30">
              <div className="text-[10px] font-semibold uppercase tracking-wide text-purple-400 mb-1.5">Nia AI</div>
              <div className="flex gap-1.5 items-center">
                {[0, 0.2, 0.4].map((delay, i) => (
                  <div
                    key={i}
                    className="w-2 h-2 rounded-full bg-purple-400 animate-bounce"
                    style={{ animationDelay: `${delay}s` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
