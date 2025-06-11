# audio_stream.py

from app.services.mic_audio_buffer import MicAudioBuffer
from app.services.remote_audio_buffer import RemoteAudioBuffer

def run_vad_stream(config, stop_event):
    if config["name"] == "remote":
        buffer = RemoteAudioBuffer(config, stop_event)
    else:
        buffer = MicAudioBuffer(config, stop_event)

    buffer.run()
