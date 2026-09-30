import { Activity, Clock, Wifi, WifiOff, Mic } from 'lucide-react';
import { AgentStatus } from '../hooks/useVoiceAgent';

const STATUS_CONFIG = {
  [AgentStatus.IDLE]:         { label: 'Offline',      color: 'text-slate-400', dot: 'bg-slate-500' },
  [AgentStatus.CONNECTING]:   { label: 'Connecting…',  color: 'text-yellow-400', dot: 'bg-yellow-400 animate-pulse' },
  [AgentStatus.READY]:        { label: 'Ready',        color: 'text-green-400',  dot: 'bg-green-400' },
  [AgentStatus.LISTENING]:    { label: 'Listening',    color: 'text-blue-400',   dot: 'bg-blue-400 animate-pulse' },
  [AgentStatus.PROCESSING]:   { label: 'Processing…',  color: 'text-purple-400', dot: 'bg-purple-400 animate-pulse' },
  [AgentStatus.SPEAKING]:     { label: 'Speaking',     color: 'text-clinical-400', dot: 'bg-clinical-400 animate-pulse' },
  [AgentStatus.ERROR]:        { label: 'Error',        color: 'text-red-400',    dot: 'bg-red-400' },
  [AgentStatus.DISCONNECTED]: { label: 'Disconnected', color: 'text-orange-400', dot: 'bg-orange-400' },
};

export default function Header({ status, sessionId, isActive }) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG[AgentStatus.IDLE];
  const now = new Date();
  const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  const dateStr = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });

  return (
    <header className="flex items-center justify-between px-6 py-3 border-b border-slate-700/50 bg-slate-950/80 backdrop-blur-md flex-shrink-0">
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-clinical-600 to-clinical-800 shadow-lg shadow-clinical-900/50">
          <Mic size={18} className="text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-white font-bold text-lg tracking-tight">Nia</span>
            <span className="text-xs font-medium px-1.5 py-0.5 rounded bg-clinical-800/60 text-clinical-300 border border-clinical-700/40">AI</span>
          </div>
          <p className="text-xs text-slate-500 -mt-0.5">Clinical Nursing Assistant</p>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-1.5">
            <span className={`status-dot ${cfg.dot}`} />
            <span className={`font-medium text-xs ${cfg.color}`}>{cfg.label}</span>
          </div>
          {sessionId && (
            <span className="text-slate-600 font-mono text-xs">#{sessionId}</span>
          )}
        </div>

        <div className="hidden md:flex items-center gap-2 text-slate-400">
          <Clock size={14} />
          <span className="text-xs font-medium">{timeStr}</span>
          <span className="text-slate-600">|</span>
          <span className="text-xs">{dateStr}</span>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-800/60 border border-slate-700/40">
            <Activity size={14} className="text-emerald-400" />
            <span className="text-xs text-slate-300 font-medium">ICU Floor 2</span>
          </div>
          {isActive ? (
            <Wifi size={16} className="text-green-400" />
          ) : (
            <WifiOff size={16} className="text-slate-600" />
          )}
        </div>
      </div>
    </header>
  );
}
