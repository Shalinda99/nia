import { useRef, useState, useCallback } from 'react';

const SAMPLE_RATE = 16000;
const VAD_THRESHOLD = 0.008;
const VAD_SILENCE_FRAMES = 25;  // ~650ms of silence before utterance ends

export function useAudioCapture({
  onAudioChunk,
  onVolumeChange,
  onUtteranceStart,
  onUtteranceEnd,
}) {
  const [isCapturing, setIsCapturing] = useState(false);
  const [error, setError] = useState(null);

  const audioContextRef = useRef(null);
  const streamRef = useRef(null);
  const workletNodeRef = useRef(null);
  const sourceNodeRef = useRef(null);
  const silenceCountRef = useRef(0);
  const isSpeakingRef = useRef(false);

  const start = useCallback(async () => {
    if (isCapturing) return;
    setError(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: SAMPLE_RATE,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      streamRef.current = stream;

      const ctx = new AudioContext({ sampleRate: SAMPLE_RATE });
      audioContextRef.current = ctx;

      await ctx.audioWorklet.addModule('/audio-processor.worklet.js');

      const source = ctx.createMediaStreamSource(stream);
      sourceNodeRef.current = source;

      const worklet = new AudioWorkletNode(ctx, 'audio-processor');
      workletNodeRef.current = worklet;

      worklet.port.onmessage = (event) => {
        const { pcm16, rms } = event.data;

        if (onVolumeChange) onVolumeChange(rms);

        const wasSpeaking = isSpeakingRef.current;

        if (rms > VAD_THRESHOLD) {
          silenceCountRef.current = 0;
          if (!isSpeakingRef.current) {
            isSpeakingRef.current = true;
            if (!wasSpeaking && onUtteranceStart) {
              onUtteranceStart();
            }
          }
        } else {
          silenceCountRef.current += 1;
          if (isSpeakingRef.current && silenceCountRef.current >= VAD_SILENCE_FRAMES) {
            isSpeakingRef.current = false;
            if (onUtteranceEnd) {
              onUtteranceEnd();
            }
          }
        }

        if (isSpeakingRef.current && onAudioChunk && pcm16) {
          onAudioChunk(pcm16);
        }
      };

      source.connect(worklet);
      setIsCapturing(true);
    } catch (err) {
      const msg = err.name === 'NotAllowedError'
        ? 'Microphone access denied. Please allow microphone access in your browser settings.'
        : `Microphone error: ${err.message}`;
      setError(msg);
      console.error('Audio capture error:', err);
    }
  }, [isCapturing, onAudioChunk, onVolumeChange, onUtteranceStart, onUtteranceEnd]);

  const stop = useCallback(() => {
    if (workletNodeRef.current) {
      workletNodeRef.current.disconnect();
      workletNodeRef.current = null;
    }
    if (sourceNodeRef.current) {
      sourceNodeRef.current.disconnect();
      sourceNodeRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    silenceCountRef.current = 0;
    isSpeakingRef.current = false;
    setIsCapturing(false);
  }, []);

  return { isCapturing, error, start, stop };
}
