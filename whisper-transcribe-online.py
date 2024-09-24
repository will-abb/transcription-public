import argparse
import asyncio
import logging
import os
import tempfile

import openai
import scipy.io.wavfile as wavfile
import sounddevice as sd

logging.basicConfig(level=logging.INFO)
openai.api_key = os.getenv("OPENAI_API_KEY")


async def record_audio(duration, sample_rate=44100):
    logging.info("Recording...")
    recording = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16"
    )
    sd.wait()
    logging.info("Recording finished.")
    return recording


def transcribe_audio(audio_path):
    with open(audio_path, "rb") as f:
        response = openai.audio.transcriptions.create(
            model="whisper-1", file=f, response_format="text"
        )
    return response


async def main(duration):
    recording = await record_audio(duration)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wavfile.write(tmpfile.name, 44100, recording)
        tmpfile_path = tmpfile.name  # Store the file name to use after closing
    transcription = transcribe_audio(tmpfile_path)
    print("Transcription:")
    print(transcription)
    os.remove(tmpfile_path)  # Manually delete the file after transcription


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Record and transcribe audio using OpenAI's Whisper model via API."
    )
    parser.add_argument("duration", type=int, help="Duration to record in seconds.")
    args = parser.parse_args()
    asyncio.run(main(args.duration))
