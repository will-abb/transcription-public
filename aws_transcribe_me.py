import argparse
import asyncio
import logging
import sys

import numpy
import sounddevice
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.exceptions import BadRequestException
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
from pynput.keyboard import Controller

# Initialize logging for debugging and runtime information
logging.basicConfig(level=logging.INFO)

# Initialize keyboard controller to simulate keypresses
keyboard = Controller()


# Function to generate a beep sound every 30 seconds
async def beep_every_30_seconds():
    while True:
        sounddevice.play(
            numpy.sin(2 * numpy.pi * 440.0 * numpy.arange(44100 * 0.5) / 44100) * 0.10,
            samplerate=44100,
        )
        await asyncio.sleep(30)


# Custom event handler for transcript results
class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            if result.is_partial:
                continue
            for alt in result.alternatives:
                self._write(alt.transcript)

    # Function to simulate keypress for received transcript
    def _write(self, transcript: str):
        for char in transcript:
            keyboard.press(char)
            keyboard.release(char)


# Asynchronous generator function for the microphone stream
async def mic_stream():
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    # Callback function to put microphone data into a queue
    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Set the block size to allow sentence length.But remember that this increases latency.
    new_blocksize = int(16000)

    # Initialize sounddevice stream
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=new_blocksize,
        dtype="int16",
    )

    # Yield microphone data from the queue
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


# Function to write audio chunks to AWS Transcribe
async def write_chunks(stream, task):
    try:
        async for chunk, status in mic_stream():
            if task.done():
                return
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
        await stream.input_stream.end_stream()
    except asyncio.CancelledError:
        logging.info("Transcription time limit reached. Stopping now.")
        sys.exit(0)


# Main transcription function
async def basic_transcribe(region, vocabulary_name):
    client = TranscribeStreamingClient(region=region)
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
        vocabulary_name=vocabulary_name,  # Added for custom vocabulary
    )

    handler = MyEventHandler(stream.output_stream)
    task = asyncio.create_task(write_chunks(stream, asyncio.current_task()))

    # Add a timeout for the transcription
    loop = asyncio.get_event_loop()
    loop.call_later(120, task.cancel)

    try:
        await asyncio.gather(task, handler.handle_events())
    except asyncio.CancelledError:
        logging.info("Transcription terminated as per the time limit.")
        sys.exit(0)
    except BadRequestException:
        logging.error(
            "Your request timed out because no new audio was received for 15 seconds."
        )
        sys.exit(1)


# Entry point
def main():
    parser = argparse.ArgumentParser(
        description="Real-time speech-to-text transcription."
    )
    parser.add_argument(
        "--region",
        type=str,
        default="us-west-2",
        help="AWS region for the Transcribe service.",
    )
    parser.add_argument(
        "--vocabulary_name",
        type=str,
        default=None,
        help="Name of the custom vocabulary to use.",
    )
    args = parser.parse_args()

    # Validating the AWS region could be added here

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            basic_transcribe(args.region, args.vocabulary_name), beep_every_30_seconds()
        )
    )


if __name__ == "__main__":
    main()
