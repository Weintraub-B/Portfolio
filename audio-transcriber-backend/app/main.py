import os
import sys
import threading
from sounddevice import check_input_settings
from app.services.audio_stream import run_vad_stream
from app.services.transcriber import run_transcription_loop
from app.stream_config import MIC_CONFIG, REMOTE_CONFIG
from app.audio_devices import select_input_device, select_wasapi_loopback_device

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

stop_event = threading.Event()

def find_supported_sample_rate(device_index, rates=(48000, 44100, 32000, 16000)):
    for rate in rates:
        try:
            check_input_settings(device=device_index, samplerate=rate)
            print(f"[main] Sample rate {rate} is supported by device {device_index}")
            return rate
        except Exception as e:
            print(f"[main] Sample rate {rate} not supported: {e}")
    raise RuntimeError(f"No supported sample rate found for device {device_index}")

if __name__ == "__main__":
    print("[main] Starting audio system...")

    mic_device_index = select_input_device()
    MIC_CONFIG["device_index"] = mic_device_index
    print(f"[main] Selected mic device index: {mic_device_index}")

    remote_device_index = select_wasapi_loopback_device()
    if remote_device_index is not None:
        REMOTE_CONFIG["device_index"] = remote_device_index
        REMOTE_CONFIG["sample_rate"] = find_supported_sample_rate(remote_device_index)
        print(f"[main] Selected remote device index: {remote_device_index}")
    else:
        exit("[main] No suitable WASAPI loopback device found. Exiting.")

    mic_thread = threading.Thread(target=run_vad_stream, kwargs={"config": MIC_CONFIG, "stop_event": stop_event}, daemon=True)
    remote_thread = threading.Thread(target=run_vad_stream, kwargs={"config": REMOTE_CONFIG, "stop_event": stop_event}, daemon=True)
    transcriber_thread = threading.Thread(target=run_transcription_loop, kwargs={"stop_event": stop_event}, daemon=True)

    mic_thread.start()
    remote_thread.start()
    transcriber_thread.start()

    print("[main] All threads started. Press Ctrl+C to stop.")

    try:
        while not stop_event.is_set():
            mic_thread.join(timeout=0.5)
            remote_thread.join(timeout=0.5)
            transcriber_thread.join(timeout=0.5)
            if not (mic_thread.is_alive() or remote_thread.is_alive() or transcriber_thread.is_alive()):
                break
    except KeyboardInterrupt:
        print("[main] Ctrl+C detected. Stopping threads...")
        stop_event.set()
        mic_thread.join()
        remote_thread.join()
        transcriber_thread.join()

    print("[main] All threads stopped. Exiting.")