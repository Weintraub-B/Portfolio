# stream_config.py

MIC_CONFIG = {
    "name": "mic",
    "device_index": None,  # Will be set to actual device index at runtime
    "sample_rate": 16000,
    "frame_duration_ms": 512,
    "path_audio": "data/mic/audio",
    "path_transcripts": "data/mic/transcripts"
}

REMOTE_CONFIG = {
    "name": "remote",
    "device_index": None,  # Will be set via WASAPI device selector
    "sample_rate": 44100,
    "frame_duration_ms": 512,
    "path_audio": "data/remote/audio",
    "path_transcripts": "data/remote/transcripts"
}
