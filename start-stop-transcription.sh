#!/bin/bash

# Set AWS profile
export AWS_PROFILE=TranscriptUser

# Load additional environment variables if needed
# source ~/path/to/your/env/file

# Path to store the PID file
PID_FILE="/tmp/aws_transcribe_me.pid"

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
source ~/virtual_environments/speech/bin/activate

# Check if the script is running and act accordingly
if check_pid; then
    kill $(cat $PID_FILE)
    rm $PID_FILE
else
    python3 ~/personal-repos/transcription/aws_transcribe_me.py --vocabulary_name custom_cs_vocab &
    echo $! > $PID_FILE
fi
