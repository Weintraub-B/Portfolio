import os
import time
import numpy as np
import sounddevice as sd
import logging
import torch
from scipy.io.wavfile import write
from scipy.signal import resample
from collections import deque
from typing import Deque, Optional
from app.services.vad_handler import is_speech


class RemoteAudioBuffer:
    def __init__(self, config: dict, stop_event):
        self.sample_rate = config["sample_rate"]
        self.frame_duration_ms = config["frame_duration_ms"]
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)
        self.audio_dir = config["path_audio"]
        self.device_index = config["device_index"]
        self.name = config["name"]
        self.stop_event = stop_event

        os.makedirs(self.audio_dir, exist_ok=True)

        self.buffer_duration = 12.0
        self.overlap_duration = 0.25
        self.vad_sample_rate = 16000
        self.min_save_duration = 0.3
        self.min_silence_duration = 0.8
        self.max_segment_duration = 8.0
        self.pre_speech_padding = 0.5
        self.post_speech_padding = 0.5

        self.buffer_samples = int(self.buffer_duration * self.sample_rate)
        self.hybrid_buffer: Deque[float] = deque(maxlen=self.buffer_samples)
        self.last_overlap = np.array([], dtype=np.float32)
        self.last_overlap_len = 0

        self.speech_active = False
        self.speech_start_time: Optional[float] = None
        self.last_voice_time: Optional[float] = None

        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)  # Change to DEBUG for more verbosity
        self.logger = logging.getLogger(self.name)

        # Load VAD
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
        (
            self.get_speech_timestamps,
            _, _, _, _
        ) = utils

    def save_audio_segment(self, segment_data: np.ndarray):
        segment_int16 = (segment_data * 32767).astype(np.int16)
        index = len([f for f in os.listdir(self.audio_dir) if f.endswith(".wav")])
        filename = os.path.join(self.audio_dir, f"remote_chunk_{index:04d}.wav")
        write(filename, self.vad_sample_rate, segment_int16)
        self.logger.info(f"Saved: {filename}")

    def flush_audio_segment(self):
        samples = np.array(self.hybrid_buffer)
        pad_samples = int(self.pre_speech_padding * self.sample_rate)
        start = max(0, len(samples) - pad_samples - int(self.buffer_duration * self.sample_rate))
        padded_samples = samples[start:]

        padded_samples = np.concatenate((self.last_overlap, padded_samples))
        samples_resampled = resample(padded_samples, int(len(padded_samples) * self.vad_sample_rate / self.sample_rate))
        audio_tensor = torch.from_numpy(samples_resampled).float()

        speech_segments = self.get_speech_timestamps(audio_tensor, self.model, sampling_rate=self.vad_sample_rate)

        if not speech_segments:
            self.logger.info("Silero found no speech; saving full segment as fallback.")
            self.save_audio_segment(samples_resampled)
        else:
            for seg in speech_segments:
                start = max(0, seg['start'] - self.last_overlap_len)
                end = max(0, seg['end'] - self.last_overlap_len)
                end = min(end, len(samples_resampled))
                if start >= end:
                    continue
                chunk = samples_resampled[start:end]
                if len(chunk) < self.min_save_duration * self.vad_sample_rate:
                    continue
                self.save_audio_segment(chunk)

        overlap_samples = int(self.overlap_duration * self.vad_sample_rate)
        self.last_overlap = samples_resampled[-overlap_samples:] if len(samples_resampled) > overlap_samples else samples_resampled
        self.last_overlap_len = len(self.last_overlap)

    def audio_callback(self, indata, frames, time_info, status):
        if self.stop_event.is_set():
            raise sd.CallbackStop()

        frame = indata.mean(axis=1)
        self.hybrid_buffer.extend(frame)

        rms = np.sqrt(np.mean(frame ** 2))
        resampled = resample(frame, int(len(frame) * self.vad_sample_rate / self.sample_rate)).astype(np.int16)
        vad_result = is_speech(resampled)

        if not vad_result and rms > 0.025:
            # self.logger.debug("RMS override activated")
            vad_result = True

        # self.logger.debug(f"VAD: {vad_result} | RMS: {rms:.5f}")

        now = time.time()

        if vad_result:
            if not self.speech_active:
                self.speech_active = True
                self.speech_start_time = now
            self.last_voice_time = now

            if self.speech_start_time and (now - self.speech_start_time > self.max_segment_duration):
                self.logger.info("Max segment duration reached. Flushing audio.")
                self.flush_audio_segment()
                self.speech_active = True
                self.speech_start_time = now

        elif self.speech_active and self.last_voice_time and (now - self.last_voice_time > self.min_silence_duration):
            self.logger.info("Detected silence. Flushing audio.")
            self.flush_audio_segment()
            self.speech_active = False
            self.speech_start_time = None
            self.last_voice_time = None

    def run(self):
        device_info = sd.query_devices(self.device_index)
        input_channels = device_info["max_input_channels"]
        if input_channels < 1:
            raise ValueError(f"Device '{device_info['name']}' has no input channels.")

        self.logger.info(f"Starting remote buffered VAD stream on device {self.device_index} ({device_info['name']})...")
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=input_channels,
                dtype='float32',
                callback=self.audio_callback,
                blocksize=0,
                device=self.device_index
            ):
                while not self.stop_event.is_set():
                    sd.sleep(100)
        except KeyboardInterrupt:
            self.logger.info("Stream interrupted by user. Exiting.")
