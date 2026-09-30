import { User, AlertTriangle, ShieldAlert, MapPin, Stethoscope, UserCheck, ChevronRight } from 'lucide-react';

function AllergyBadge({ drug, reaction }) {
  return (
    <span
      title={`Reaction: ${reaction}`}
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-red-500/15 text-red-300 border border-red-500/25"
    >
      <AlertTriangle size={10} />
      {drug}
    </span>
  );
}

function InfoRow({ label, value, highlight }) {
  return (
    <div className="flex justify-between items-start gap-2 py-1.5 border-b border-slate-700/30 last:border-0">
      <span className="text-xs text-slate-500 flex-shrink-0">{label}</span>
      <span className={`text-xs font-medium text-right ${highlight ? 'text-red-300' : 'text-slate-200'}`}>
        {value}
      </span>
    </div>
  );
}

const CODE_STATUS_COLOR = {
  'Full Code': 'badge-green',
  'DNR/DNI': 'badge-red',
  'DNR': 'badge-red',
  'Comfort Care': 'badge-yellow',
};

const FALL_RISK_COLOR = {
  'High': 'badge-red',
  'Medium': 'badge-yellow',
  'Low': 'badge-green',
};

export default function PatientPanel({ patient }) {
  if (!patient) {
    return (
      <div className="flex flex-col items-center justify-center h-full py-10 text-center">
        <User size={32} className="text-slate-700 mb-3" />
        <p className="text-slate-600 text-sm">No patient selected</p>
        <p className="text-slate-700 text-xs mt-1">
          Ask about a patient by name or ID
        </p>
      </div>
    );
  }

  const codeClass = CODE_STATUS_COLOR[patient.code_status] || 'badge-blue';
  const fallClass = FALL_RISK_COLOR[patient.fall_risk] || 'badge-blue';

  return (
    <div className="space-y-4">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-600 to-slate-800 flex items-center justify-center flex-shrink-0">
          <User size={18} className="text-slate-300" />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-white font-semibold text-base leading-tight truncate">{patient.name}</h3>
          <div className="flex items-center gap-2 mt-0.5">
            <MapPin size={11} className="text-slate-500" />
            <span className="text-slate-400 text-xs">Room {patient.room}</span>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        <span className={codeClass}>{patient.code_status}</span>
        <span className={fallClass}>
          <AlertTriangle size={10} />
          Fall: {patient.fall_risk}
        </span>
        {patient.isolation && patient.isolation !== 'None' && (
          <span className="badge-red">
            <ShieldAlert size={10} />
            {patient.isolation.split(' ')[0]}
          </span>
        )}
      </div>

      <div className="glass-card-light p-3 space-y-0">
        <InfoRow label="MRN" value={patient.id} />
        <InfoRow label="Attending" value={patient.attending?.replace('Dr. ', '') || '—'} />
        <div className="py-1.5 border-b border-slate-700/30">
          <span className="text-xs text-slate-500 block mb-1">Diagnosis</span>
          <span className="text-xs font-medium text-slate-200 leading-relaxed block">
            {patient.diagnosis}
          </span>
        </div>
        {patient.isolation && patient.isolation !== 'None' && (
          <InfoRow label="Isolation" value={patient.isolation} highlight />
        )}
      </div>

      {patient.allergies && patient.allergies.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 mb-2">
            <AlertTriangle size={12} className="text-red-400" />
            <span className="text-xs font-semibold text-red-400 uppercase tracking-wide">Allergies</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {patient.allergies.map((a, i) => (
              <AllergyBadge key={i} drug={a.drug} reaction={a.reaction} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
