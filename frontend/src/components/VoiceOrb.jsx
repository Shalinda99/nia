import { Mic, MicOff, Loader2, Volume2 } from 'lucide-react';
import { AgentStatus } from '../hooks/useVoiceAgent';

const BARS = 12;

function WaveformBars({ volume, active }) {
  return (
    <div className="flex items-center justify-center gap-[3px] h-8">
      {Array.from({ length: BARS }).map((_, i) => {
        const delay = (i / BARS) * 0.8;
        const height = active ? Math.max(0.15, volume * (0.5 + 0.5 * Math.sin((i / BARS) * Math.PI))) : 0.15;
        return (
          <div
            key={i}
            className="w-[3px] rounded-full bg-blue-400 transition-all duration-75"
            style={{
              height: `${height * 100}%`,
              opacity: active ? 0.7 + 0.3 * height : 0.3,
              animationDelay: `${delay}s`,
              ...(active && volume > 0.05 ? { animation: `barWave ${0.6 + i * 0.05}s ease-in-out infinite`, animationDelay: `${delay}s` } : {}),
            }}
          />
        );
      })}
    </div>
  );
}

const ORB_CONFIG = {
  [AgentStatus.IDLE]: {
    bg: 'from-slate-700 to-slate-800',
    ring: 'ring-slate-600/30',
    glow: '',
    icon: MicOff,
    iconColor: 'text-slate-400',
    label: 'Tap to activate',
    pulse: false,
  },
  [AgentStatus.CONNECTING]: {
    bg: 'from-yellow-600 to-yellow-800',
    ring: 'ring-yellow-500/30',
    glow: 'shadow-yellow-500/20',
    icon: Loader2,
    iconColor: 'text-yellow-200 animate-spin',
    label: 'Connecting…',
    pulse: false,
  },
  [AgentStatus.READY]: {
    bg: 'from-emerald-600 to-emerald-800',
    ring: 'ring-emerald-400/40',
    glow: 'shadow-emerald-500/30',
    icon: Mic,
    iconColor: 'text-emerald-100',
    label: 'Say something…',
    pulse: true,
  },
  [AgentStatus.LISTENING]: {
    bg: 'from-blue-500 to-blue-700',
    ring: 'ring-blue-400/50',
    glow: 'shadow-blue-500/40',
    icon: Mic,
    iconColor: 'text-white',
    label: 'Listening…',
    pulse: true,
  },
  [AgentStatus.PROCESSING]: {
    bg: 'from-purple-600 to-purple-800',
    ring: 'ring-purple-400/40',
    glow: 'shadow-purple-500/30',
    icon: Loader2,
    iconColor: 'text-purple-200 animate-spin',
    label: 'Processing…',
    pulse: false,
  },
  [AgentStatus.SPEAKING]: {
    bg: 'from-clinical-600 to-clinical-800',
    ring: 'ring-clinical-400/40',
    glow: 'shadow-clinical-500/30',
    icon: Volume2,
    iconColor: 'text-white',
    label: 'Speaking…',
    pulse: true,
  },
  [AgentStatus.ERROR]: {
    bg: 'from-red-600 to-red-800',
    ring: 'ring-red-400/40',
    glow: 'shadow-red-500/30',
    icon: MicOff,
    iconColor: 'text-red-200',
    label: 'Error — tap to retry',
    pulse: false,
  },
  [AgentStatus.DISCONNECTED]: {
    bg: 'from-orange-600 to-orange-800',
    ring: 'ring-orange-400/40',
    glow: 'shadow-orange-500/30',
    icon: Loader2,
    iconColor: 'text-orange-200 animate-spin',
    label: 'Reconnecting…',
    pulse: false,
  },
};

export default function VoiceOrb({ status, isActive, volume, onActivate, onDeactivate }) {
  const cfg = ORB_CONFIG[status] || ORB_CONFIG[AgentStatus.IDLE];
  const Icon = cfg.icon;
  const isListening = status === AgentStatus.LISTENING;

  const handleClick = () => {
    if (isActive) {
      onDeactivate();
    } else {
      onActivate();
    }
  };

  return (
    <div className="flex flex-col items-center gap-6 py-6">
      <div className="relative flex items-center justify-center">
        {cfg.pulse && (
          <>
            <div className={`absolute w-36 h-36 rounded-full bg-gradient-to-br ${cfg.bg} opacity-10 animate-ripple`} />
            <div className={`absolute w-36 h-36 rounded-full bg-gradient-to-br ${cfg.bg} opacity-10 animate-ripple-delay`} />
          </>
        )}

        {isListening && volume > 0.05 && (
          <div
            className={`absolute rounded-full bg-gradient-to-br ${cfg.bg} opacity-20 transition-all duration-75`}
            style={{
              width: `${140 + volume * 60}px`,
              height: `${140 + volume * 60}px`,
            }}
          />
        )}

        <button
          onClick={handleClick}
          className={`
            relative z-10 w-28 h-28 rounded-full
            bg-gradient-to-br ${cfg.bg}
            ring-4 ${cfg.ring}
            shadow-2xl ${cfg.glow}
            flex items-center justify-center
            transition-all duration-300
            hover:scale-105 active:scale-95
            focus:outline-none focus:ring-4 focus:ring-white/20
            cursor-pointer
          `}
          aria-label={isActive ? 'Deactivate voice agent' : 'Activate voice agent'}
        >
          <Icon size={40} className={cfg.iconColor} strokeWidth={1.5} />
        </button>
      </div>

      <div className="flex flex-col items-center gap-3">
        <p className="text-sm font-medium text-slate-300">{cfg.label}</p>

        {isListening && (
          <div className="w-40">
            <WaveformBars volume={volume} active={isListening} />
          </div>
        )}

        {isActive && (
          <button
            onClick={onDeactivate}
            className="text-xs text-slate-500 hover:text-red-400 transition-colors underline underline-offset-2"
          >
            Stop session
          </button>
        )}
      </div>
    </div>
  );
}
