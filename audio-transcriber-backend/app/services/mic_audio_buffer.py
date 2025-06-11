import os
import numpy as np
import sounddevice as sd
import logging
from scipy.io.wavfile import write
from collections import deque
from typing import Deque, Optional
from app.services.vad_handler import is_speech


class MicAudioBuffer:
    def __init__(self, config: dict, stop_event):
        self.sample_rate = config["sample_rate"]
        self.frame_duration_ms = config["frame_duration_ms"]
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)
        self.audio_dir = config["path_audio"]
        self.device_index = config["device_index"]
        self.name = config["name"]
        self.stop_event = stop_event

        os.makedirs(self.audio_dir, exist_ok=True)

        # VAD parameters
        self.silence_frames_to_stop = 2
        self.pre_speech_frames = 2
        self.tail_padding_frames = 2
        self.vad_window_size = 1

        self.recording = False
        self.speech_buffer: list[np.ndarray] = []
        self.recent_frames: Deque[np.ndarray] = deque(maxlen=self.pre_speech_frames)
        self.silence_counter = 0
        self.vad_window: Deque[int] = deque(maxlen=self.vad_window_size)

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.name)

    def save_recording(self, data: np.ndarray):
        index = len([f for f in os.listdir(self.audio_dir) if f.endswith(".wav")])
        filename = os.path.join(self.audio_dir, f"{self.name}_chunk_{index:04d}.wav")
        write(filename, self.sample_rate, data.astype(np.int16))
        self.logger.info(f"Saved: {filename}")

    def audio_callback(self, indata, frames, time_info, status):
        frame = indata[:, 0].copy().astype(np.int16)
        self.recent_frames.append(frame)

        vad_result = is_speech(frame)
        self.vad_window.append(1 if vad_result else 0)
        is_talking = sum(self.vad_window) >= (self.vad_window_size // 2 + 1)

        if is_talking:
            if not self.recording:
                self.recording = True
                self.speech_buffer = list(self.recent_frames)[:-1]
                self.logger.info("Speech detected")
                self.vad_window.clear()
                self.silence_counter = 0

            self.speech_buffer.append(frame)
            self.silence_counter = 0

        elif self.recording:
            self.speech_buffer.append(frame)
            self.silence_counter += 1

            if self.silence_counter >= self.silence_frames_to_stop:
                for _ in range(self.tail_padding_frames):
                    self.speech_buffer.append(np.zeros(self.frame_size, dtype=np.int16))
                full_chunk = np.concatenate(self.speech_buffer)
                self.save_recording(full_chunk)

                self.recording = False
                self.speech_buffer.clear()
                self.silence_counter = 0
                self.vad_window.clear()
                self.recent_frames.clear()

    def run(self):
        self.logger.info(f"Starting mic VAD stream on device {self.device_index}...")
        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16',
                callback=self.audio_callback,
                blocksize=self.frame_size,
                device=self.device_index
            ):
                while not self.stop_event.is_set():
                    sd.sleep(100)
        except KeyboardInterrupt:
            self.logger.info("Stream interrupted by user. Exiting.")
