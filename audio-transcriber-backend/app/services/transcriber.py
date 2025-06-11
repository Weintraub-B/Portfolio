import os
import json
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from faster_whisper import WhisperModel
from app.stream_config import MIC_CONFIG, REMOTE_CONFIG

WATCH_DIRS = [
    (MIC_CONFIG["path_audio"], MIC_CONFIG["path_transcripts"], MIC_CONFIG["name"]),
    (REMOTE_CONFIG["path_audio"], REMOTE_CONFIG["path_transcripts"], REMOTE_CONFIG["name"]),
]

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"
model = WhisperModel("medium.en", device=device, compute_type=compute_type)

class TranscriptionHandler(FileSystemEventHandler):
    def __init__(self, input_dir, output_dir, label):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.label = label
        os.makedirs(self.output_dir, exist_ok=True)

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".wav"):
            return

        filepath = event.src_path
        fname = os.path.basename(filepath)
        print(f"[transcriber] Detected new ({self.label}) audio: {fname}")

        time.sleep(0.3)

        try:
            segments, info = model.transcribe(filepath, beam_size=5)
            full_text = []
            segment_list = []

            for seg in segments:
                segment_list.append({
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip()
                })
                full_text.append(seg.text.strip())

            result = {
                "filename": fname,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "text": " ".join(full_text),
                "segments": segment_list,
                "language": info.language,
                "duration": info.duration,
                "source": self.label
            }

            outname = fname.replace(".wav", ".json")
            outpath = os.path.join(self.output_dir, outname)
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            print(f"[transcriber] Transcribed ({self.label}): {outname}")

        except Exception as e:
            print(f"[transcriber] Error processing {fname}: {e}")

def run_transcription_loop(stop_event):
    print("[transcriber] Starting watchdog for mic and remote folders...")
    observer = Observer()

    for input_dir, output_dir, label in WATCH_DIRS:
        handler = TranscriptionHandler(input_dir, output_dir, label)
        observer.schedule(handler, input_dir, recursive=False)

    observer.start()
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("[transcriber] Interrupted by user. Stopping observer.")
        observer.stop()
    observer.join()
