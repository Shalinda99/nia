class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._buffer = [];
    this._bufferSize = 4096;
  }

  process(inputs) {
    const input = inputs[0];
    if (!input || !input[0]) return true;

    const float32 = input[0];

    for (let i = 0; i < float32.length; i++) {
      this._buffer.push(float32[i]);
    }

    while (this._buffer.length >= this._bufferSize) {
      const chunk = this._buffer.splice(0, this._bufferSize);
      const int16 = new Int16Array(chunk.length);
      for (let i = 0; i < chunk.length; i++) {
        const s = Math.max(-1, Math.min(1, chunk[i]));
        int16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
      }

      const rms = Math.sqrt(chunk.reduce((sum, s) => sum + s * s, 0) / chunk.length);

      this.port.postMessage(
        { pcm16: int16.buffer, rms },
        [int16.buffer]
      );
    }

    return true;
  }
}

registerProcessor('audio-processor', AudioProcessor);
