import torch
import numpy as np

SAMPLE_RATE = 16000

# Load Silero VAD model from torch.hub
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils

def is_speech(audio_chunk: np.ndarray) -> bool:
    """
    Check if the given audio chunk contains speech using Silero VAD.
    """
    if audio_chunk.ndim > 1:
        audio_chunk = audio_chunk[:, 0]

    audio_tensor = torch.from_numpy(audio_chunk.astype(np.float32)) / 32768.0
    speech_ts = get_speech_timestamps(audio_tensor, model, sampling_rate=SAMPLE_RATE)
    return bool(speech_ts)
