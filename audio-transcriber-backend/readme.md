# Real-Time Audio Chunker and Transcriber Backend

## Overview

This project is a Python-based backend service designed to capture audio input from both a user's microphone and system audio (e.g. virtual meetings). It segments speech in real time using voice activity detection (VAD), transcribes it using Whisper-compatible models, and outputs structured files for downstream use with LLM or retrieval-augmented generation (RAG) pipelines such as PipeCat or Ollama.

## Features

- Real-time voice activity detection using Silero VAD
- Dual-source audio capture: microphone and system loopback
- Automatic segmentation and padding for natural audio chunks
- Background transcription using FasterWhisper (optional)
- Configurable audio parameters and device selection
- Modular, class-based architecture for testing and reuse

## Project Structure

```
audio-transcriber-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── audio_devices.py
│   ├── stream_config.py
│   └── services/
│       ├── __init__.py
│       ├── mic_audio_buffer.py
│       ├── remote_audio_buffer.py
│       ├── transcriber.py
│       ├── vad_handler.py
│       └── audio_stream.py
├── data/
│   ├── mic/
│   └── remote/
├── requirements.txt
├── .gitignore
├── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- For system audio capture:
  - On Windows, tools such as **ASIO Bridge** (from VB-Audio) may be required to route system audio into a virtual device.
  - Note: ASIO Bridge may require a license for full commercial use. You are responsible for obtaining and configuring it if needed.

### Running the App

From the project root:

```bash
python -m app.main
```

- Select the microphone and system loopback devices when prompted
- Audio chunks will be saved under `data/mic/` and `data/remote/`
- If transcription is enabled, results will appear as `.json` files

## Output Example

```text
data/
├── remote/
│   ├── remote_chunk_0001.wav
│   └── transcripts/
│       └── remote_chunk_0001.json
```

**Sample Transcript JSON**

```json
{
  "text": "Hello, welcome to the meeting.",
  "segments": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello, welcome to the meeting."
    }
  ],
  "language": "en"
}
```

**Sample Audio Segment Description**

- File: `remote_chunk_0001.wav`
- Format: Mono WAV, 16 kHz
- Duration: \~2.5 seconds
- Captured automatically after detecting live speech

## Use Cases

- Meeting summarization and live capture
- Game narration via LLMs (e.g. D&D assistants)
- Input for real-time Q&A pipelines
- Preprocessing for RAG systems like PipeCat or LangChain

## Testing

Basic tests can be run using `pytest`. Example test coverage includes verifying configurations and component wiring.

Example:

```python
# tests/test_config.py

def test_config_constants():
    from app.stream_config import MIC_CONFIG
    assert "sample_rate" in MIC_CONFIG
```

## Tech Stack

- Python 3.10
- PyTorch with Silero VAD
- SoundDevice, SciPy for audio I/O
- FasterWhisper for transcription

## License

This project is released under the MIT License.

## Acknowledgments

- [Silero VAD](https://github.com/snakers4/silero-vad)
- [FasterWhisper](https://github.com/guillaumekln/faster-whisper)
- [Ollama](https://ollama.ai/) for LLM integration
- [VB-Audio ASIO Bridge](https://vb-audio.com/Cable/) for system audio routing (optional)

