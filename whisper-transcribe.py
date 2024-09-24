import queue
import signal
import tempfile
import threading
import warnings

import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import whisper
from pynput.keyboard import Controller

warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)

# Global flag used to signal the recording thread to stop
stop_recording_flag = threading.Event()


# Signal handler for stopping the recording
def stop_recording(signalNumber, frame):
    stop_recording_flag.set()


# Register the signal handler for SIGUSR1
signal.signal(signal.SIGUSR1, stop_recording)


def record_audio(frames_queue, sample_rate=44100, channels=1, dtype="int16"):
    def callback(indata, frames, time, status):
        frames.put(indata.copy())

    with sd.InputStream(
        callback=lambda indata, frame_count, time_info, status: callback(
            indata, frames_queue, time_info, status
        ),
        samplerate=sample_rate,
        channels=channels,
        dtype=dtype,
    ):
        while not stop_recording_flag.is_set():
            sd.sleep(100)


def transcribe_audio(audio_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmpfile:
        wavfile.write(tmpfile.name, 44100, audio_data)
        model = whisper.load_model("small.en")
        result = model.transcribe(tmpfile.name, language="en")
        return result["text"]


def main():
    tone = np.sin(2 * np.pi * 440.0 * np.arange(44100 * 0.5) / 44100) * 0.10
    sd.play(tone, samplerate=44100)
    sd.wait()

    frames_queue = queue.Queue()
    recording_thread = threading.Thread(
        target=record_audio, args=(frames_queue,), daemon=True
    )
    recording_thread.start()

    # Wait indefinitely until the recording is stopped by the signal
    recording_thread.join()

    # Collect frames from the queue and concatenate them into a single numpy array
    frames = list(frames_queue.queue)
    recording = np.concatenate(frames, axis=0)

    transcription = transcribe_audio(recording)

    # Initialize keyboard controller
    keyboard = Controller()
    # Type out the transcription
    keyboard.type(transcription)


if __name__ == "__main__":
    main()
