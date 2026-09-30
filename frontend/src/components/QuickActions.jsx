import { Pill, Activity, FlaskConical, FileText, ClipboardList, Users } from 'lucide-react';

const ACTIONS = [
  { icon: Activity,      label: 'Vitals',      prompt: 'What are the latest vitals for this patient?' },
  { icon: Pill,          label: 'Meds',        prompt: 'What medications does this patient have due now?' },
  { icon: FlaskConical,  label: 'Labs',        prompt: 'Show me the latest lab results for this patient.' },
  { icon: ClipboardList, label: 'Orders',      prompt: 'What are the pending orders for this patient?' },
  { icon: FileText,      label: 'Sepsis',      prompt: 'What is the sepsis protocol?' },
  { icon: Users,         label: 'All Patients', prompt: 'List all patients on the unit.' },
];

export default function QuickActions({ onPrompt, disabled }) {
  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Quick Commands</p>
      <div className="grid grid-cols-3 gap-2">
        {ACTIONS.map(({ icon: Icon, label, prompt }) => (
          <button
            key={label}
            onClick={() => onPrompt && onPrompt(prompt)}
            disabled={disabled}
            className="flex flex-col items-center gap-1.5 p-2.5 rounded-xl
              bg-slate-800/50 border border-slate-700/40
              hover:bg-slate-700/50 hover:border-slate-600/50
              active:scale-95 transition-all duration-150
              disabled:opacity-40 disabled:cursor-not-allowed
              group"
          >
            <Icon size={16} className="text-slate-400 group-hover:text-clinical-400 transition-colors" />
            <span className="text-[10px] font-medium text-slate-500 group-hover:text-slate-300 transition-colors">
              {label}
            </span>
          </button>
        ))}
      </div>
      <p className="text-[10px] text-slate-700 text-center">
        Click a command or just speak naturally
      </p>
    </div>
  );
}
