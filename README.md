# AWS Transcription Service README

## Introduction

This repository contains scripts for real-time speech-to-text transcription using AWS Transcribe. The repository includes:

1. A Bash script for managing the transcription process.
2. A Python script that performs the transcription using AWS Transcribe.
3. Terraform files for AWS user creation with required permissions.
4. File `requirements.txt` to install python packages.
5. `rules.txt` that contains the rules for creating custom vocabularies.
6. `custom_cs_vocab.txt` for custom vocabularies specifically tailored for Computer Science and DevOps terminology.

### New Features

- Auditory beeping: An optional feature that allows the system to beep every 30 seconds during the transcription process.
- Custom Vocabulary: A new feature that allows you to use custom vocabulary files to improve transcription accuracy. These vocabularies are defined in `custom_cs_vocab.txt`.

## Pre-requisites

### AWS IAM User Configuration

The solution uses an AWS IAM User called `TranscriptUser` with the `AmazonTranscribeFullAccess` policy.

**Note**: Single Sign-On (SSO) will **NOT** work with this solution. You must create an AWS IAM User.

You can use the included Terraform scripts to create the user and attach the necessary permissions:

Navigate to the Terraform folder and run the following commands:

```bash
terraform init
terraform apply
```

### AWS CLI and Configuration

Make sure you have AWS CLI installed and configure it with the newly created `TranscriptUser` credentials.

In your `~/.aws/credentials` and `~/.aws/config`, add an entry for `TranscriptUser` like so:

```ini
# ~/.aws/credentials
[TranscriptUser]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

```ini
# ~/.aws/config
[profile TranscriptUser]
region = YOUR_PREFERRED_REGION
```

### Custom Vocabulary

To update the custom vocabulary used for transcription, use the `update_vocabulary.py` script:

```bash
python3 update_vocabulary.py --file_name custom_cs_vocab.txt --bucket my-transcribe-custom-cs-vocab-bucket --vocabulary_name custom_cs_vocab --language_code en-US
```

### Python Environment

Ensure Python 3.x and required libraries are installed.

1. Create a Python virtual environment:

    ```bash
    python3 -m venv ~/virtual_environments/speech
    ```

2. Activate the virtual environment:

    ```bash
    source ~/virtual_environments/speech/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip3 install -r requirements.txt
    ```
>**Note** if you have issues with PortAudio library when running script just install via apt instead:
``` bash
sudo apt-get --reinstall install libportaudio2
```

### Running the Solution

#### Bash Script

The Bash script `start_stop_transcription.sh` controls the transcription process. It starts or stops the Python script.

You can run the script like this:

```bash
bash ~/personal-repos/transcription/start_stop_transcription.sh
```

Or, to explicitly set the AWS Profile, use:

```bash
gnome-terminal -- bash -c "export AWS_PROFILE=TranscriptUser; bash ~/personal-repos/transcription/start_stop_transcription.sh; exec bash"
```

#### Python Script

The Python script `aws_transcribe_me.py` performs real-time transcription using AWS Transcribe. It requires Python 3.x and the AWS SDK for Python (`boto3`).

To specify the AWS region and use the custom vocabulary, use the following command:

```bash
python3 ~/personal-repos/transcription/aws_transcribe_me.py --vocabulary_name custom_cs_vocab &
```

### Troubleshooting

The Python script verifies your AWS identity. If you encounter issues related to AWS credentials, make sure your AWS CLI is correctly configured and the `TranscriptUser` IAM user has the necessary permissions.

### Known Issues

- The solution does not support AWS SSO. You must create an IAM user.

### Contributing

Feel free to contribute by opening issues or submitting pull requests.

---
