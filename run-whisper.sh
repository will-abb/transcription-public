#!/bin/bash

# Path to store the PID file
PID_FILE="/tmp/whisper_transcribe.pid"

# Function to check if a process is running
check_pid() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if [ -e /proc/$PID ]; then
            return 0
        else
            rm $PID_FILE
            return 1
        fi
    else
        return 1
    fi
}

# Activate the virtual environment
source ~/virtual_environments/whisper/bin/activate

# Check if the script is running and act accordingly
if check_pid; then
    # Signal the Python script to stop recording
    kill -SIGUSR1 $(cat $PID_FILE)
else
    # Run the Python script and store its PID
    ~/virtual_environments/whisper/bin/python ~/repositories/bitbucket/williseed1/transcription/whisper-transcribe.py &
    echo $! >$PID_FILE
fi
