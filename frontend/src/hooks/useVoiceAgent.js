import { useRef, useState, useCallback, useEffect } from 'react';
import { useAudioCapture } from './useAudioCapture';
import { playBase64Audio, speakText, stopCurrentAudio } from '../services/ttsService';

const WS_URL = '/ws/voice';

export const AgentStatus = {
  IDLE: 'idle',
  CONNECTING: 'connecting',
  READY: 'ready',
  LISTENING: 'listening',
  PROCESSING: 'processing',
  SPEAKING: 'speaking',
  ERROR: 'error',
  DISCONNECTED: 'disconnected',
};

export function useVoiceAgent() {
  const [status, setStatus] = useState(AgentStatus.IDLE);
  const [isActive, setIsActive] = useState(false);
  const [partialTranscript, setPartialTranscript] = useState('');
  const [messages, setMessages] = useState([]);
  const [currentPatient, setCurrentPatient] = useState(null);
  const [toolsUsed, setToolsUsed] = useState([]);
  const [volume, setVolume] = useState(0);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  const wsRef = useRef(null);
  const reconnectTimerRef = useRef(null);
  const pingTimerRef = useRef(null);
  const statusRef = useRef(status);
  statusRef.current = status;

  const sendWs = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  const handleWsMessage = useCallback((event) => {
    let data;
    try {
      data = JSON.parse(event.data);
    } catch {
      return;
    }

    switch (data.type) {
      case 'session_started':
        setSessionId(data.session_id);
        setStatus(AgentStatus.READY);
        break;

      case 'listening':
        if (statusRef.current === AgentStatus.READY) {
          setStatus(AgentStatus.LISTENING);
        }
        break;

      case 'transcript_final':
        setPartialTranscript('');
        if (data.text) {
          setMessages((prev) => [...prev, { role: 'user', text: data.text, timestamp: Date.now() }]);
        }
        break;

      case 'processing':
        setStatus(AgentStatus.PROCESSING);
        setToolsUsed([]);
        break;

      case 'tool_called':
        setToolsUsed((prev) => [...prev, { tool: data.tool, args: data.args }]);
        break;

      case 'agent_response':
        setStatus(AgentStatus.SPEAKING);
        const responseText = data.text || '';
        setMessages((prev) => [
          ...prev,
          { role: 'agent', text: responseText, tools: data.tools_used || [], timestamp: Date.now() },
        ]);

        const onSpeakEnd = () => setStatus(AgentStatus.READY);

        if (data.audio) {
          playBase64Audio(data.audio, onSpeakEnd).catch(() => {
            speakText(responseText, onSpeakEnd);
          });
        } else {
          speakText(responseText, onSpeakEnd);
        }
        break;

      case 'patient_updated':
        setCurrentPatient(data.patient);
        break;

      case 'patients_list':
        break;

      case 'history_cleared':
        setMessages([]);
        break;

      case 'error':
        setError(data.message);
        break;

      case 'pong':
        break;

      default:
        break;
    }
  }, []);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setStatus(AgentStatus.CONNECTING);
    setError(null);

    const ws = new WebSocket(WS_URL);
    ws.binaryType = 'arraybuffer';
    wsRef.current = ws;

    ws.onopen = () => {
      pingTimerRef.current = setInterval(() => {
        sendWs({ type: 'ping' });
      }, 30000);
    };

    ws.onmessage = handleWsMessage;

    ws.onerror = (e) => {
      console.error('WebSocket error:', e);
      setError('Connection error. Make sure the backend is running.');
      setStatus(AgentStatus.ERROR);
    };

    ws.onclose = () => {
      clearInterval(pingTimerRef.current);
      setStatus(AgentStatus.DISCONNECTED);
      if (isActive) {
        reconnectTimerRef.current = setTimeout(connect, 3000);
      }
    };
  }, [handleWsMessage, sendWs, isActive]);

  const disconnect = useCallback(() => {
    clearTimeout(reconnectTimerRef.current);
    clearInterval(pingTimerRef.current);
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setStatus(AgentStatus.IDLE);
  }, []);

  const onAudioChunk = useCallback((pcm16Buffer) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(pcm16Buffer);
    }
  }, []);

  const onVolumeChange = useCallback((rms) => {
    setVolume(Math.min(1, rms * 20));
  }, []);

  const onUtteranceStart = useCallback(() => {
    const st = statusRef.current;
    if (st === AgentStatus.READY || st === AgentStatus.LISTENING) {
      sendWs({ type: 'utterance_start' });
      setStatus(AgentStatus.LISTENING);
    }
  }, [sendWs]);

  const onUtteranceEnd = useCallback(() => {
    const st = statusRef.current;
    if (st === AgentStatus.LISTENING) {
      sendWs({ type: 'utterance_end' });
      setVolume(0);
    }
  }, [sendWs]);

  const { isCapturing, error: captureError, start: startCapture, stop: stopCapture } = useAudioCapture({
    onAudioChunk,
    onVolumeChange,
    onUtteranceStart,
    onUtteranceEnd,
  });

  const activate = useCallback(async () => {
    setIsActive(true);
    connect();
    await startCapture();
  }, [connect, startCapture]);

  const deactivate = useCallback(() => {
    stopCurrentAudio();
    stopCapture();
    disconnect();
    setIsActive(false);
    setPartialTranscript('');
    setVolume(0);
    setStatus(AgentStatus.IDLE);
  }, [stopCapture, disconnect]);

  const clearHistory = useCallback(() => {
    sendWs({ type: 'clear_history' });
    setMessages([]);
    setCurrentPatient(null);
    setToolsUsed([]);
  }, [sendWs]);

  useEffect(() => {
    if (captureError) setError(captureError);
  }, [captureError]);

  useEffect(() => {
    return () => {
      clearTimeout(reconnectTimerRef.current);
      clearInterval(pingTimerRef.current);
    };
  }, []);

  return {
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
  };
}
