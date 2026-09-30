let audioContext = null;
let currentSource = null;

function getAudioContext() {
  if (!audioContext || audioContext.state === 'closed') {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

export async function playBase64Audio(base64Mp3, onEnd) {
  try {
    stopCurrentAudio();
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') await ctx.resume();
    const binary = atob(base64Mp3);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    const buffer = await ctx.decodeAudioData(bytes.buffer);
    currentSource = ctx.createBufferSource();
    currentSource.buffer = buffer;
    currentSource.connect(ctx.destination);
    currentSource.onended = () => {
      currentSource = null;
      if (onEnd) onEnd();
    };
    currentSource.start(0);
    return true;
  } catch (err) {
    console.error('Audio playback error:', err);
    return false;
  }
}

export function speakText(text, onEnd) {
  if (!('speechSynthesis' in window)) {
    console.warn('Browser TTS not available');
    if (onEnd) onEnd();
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1.05;
  utterance.pitch = 1.0;
  utterance.volume = 1.0;

  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(
    (v) =>
      v.lang.startsWith('en') &&
      (v.name.toLowerCase().includes('female') ||
        v.name.toLowerCase().includes('samantha') ||
        v.name.toLowerCase().includes('zira') ||
        v.name.toLowerCase().includes('karen'))
  );
  if (preferred) utterance.voice = preferred;

  utterance.onend = () => { if (onEnd) onEnd(); };
  utterance.onerror = () => { if (onEnd) onEnd(); };
  window.speechSynthesis.speak(utterance);
}

export function stopCurrentAudio() {
  if (currentSource) {
    try { currentSource.stop(); } catch (_) {}
    currentSource = null;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

export function isSpeaking() {
  return (
    currentSource !== null ||
    ('speechSynthesis' in window && window.speechSynthesis.speaking)
  );
}
