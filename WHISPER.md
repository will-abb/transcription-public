# Audio Transcriber README

## Overview

This Python script offers a straightforward solution for recording audio through the system's microphone and transcribing it into text. It utilizes libraries like `numpy`, `scipy`, `sounddevice`, and `whisper` for audio processing and speech recognition. The script is designed to record until silence is detected for a specified duration after which it will automatically transcribe the recorded audio into text.

## Features

- **Audio Recording**: Records mono audio at a sample rate of 44100 Hz.
- **Silence Detection**: Stops recording when silence is detected for a user-defined duration, making it efficient for capturing speech.
- **Audio Transcription**: Uses OpenAI's Whisper model for accurately transcribing the recorded audio into text.

## Requirements

- Python 3.x
- `numpy`
- `scipy`
- `sounddevice`
- `whisper`

Ensure you have the latest versions of these packages. Use pip to install or upgrade them:

```sh
pip install numpy scipy sounddevice whisper --upgrade
```

## Usage

1. **Set Up**: Make sure you have all the required packages installed. Check the 'Requirements' section for installation commands.

2. **Run the Script**: Execute the script in your terminal or command prompt.

   ```
   python audio_transcriber.py
   ```

3. **Recording**: Speak into the microphone. Recording starts automatically when sound is detected and stops when silence is sustained for the user-defined duration.

4. **Transcription Output**: After the recording stops, the script will transcribe the audio to text and display the transcription in the console.

## Configuration

You can adjust the following settings according to your needs:

- **`sample_rate`**: The sample rate of the recording. Default is 44100 Hz.
- **`silence_threshold`**: The volume level below which is considered silence. Default is 10.
- **`silence_duration`**: The duration of silence (in seconds) after which recording stops. Default is 6 seconds.

These settings can be adjusted directly in the script.

## Limitations

- This script only records in mono and at a fixed sample rate.
- It requires an internet connection to download the `whisper` model upon first use.
- The accuracy of transcription might vary depending on the clarity of the recorded audio.

## License

