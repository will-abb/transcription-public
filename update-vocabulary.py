import argparse
import os

import boto3
from botocore.exceptions import ClientError

"""➜  ~ python3 update_vocabulary.py --file_name custom_cs_vocab.txt --bucket my-transcribe-custom-cs-vocab-bucket --vocabulary_name custom_cs_vocab --language_code en-US
"""


def upload_file_to_s3(file_name, bucket):
    try:
        s3.upload_file(file_name, bucket, file_name)
        print(f"Successfully uploaded {file_name} to {bucket}.")
    except Exception as e:
        print(f"An error occurred during upload: {e}")
        return


def create_or_update_vocabulary(
    client, vocabulary_name, vocabulary_file_uri, language_code
):
    try:
        response = client.create_vocabulary(
            VocabularyName=vocabulary_name,
            LanguageCode=language_code,
            VocabularyFileUri=vocabulary_file_uri,
        )
        print(f"Creating vocabulary with name {vocabulary_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConflictException":
            print(f"Vocabulary with name {vocabulary_name} already exists. Updating...")
            response = client.update_vocabulary(
                VocabularyName=vocabulary_name,
                LanguageCode=language_code,
                VocabularyFileUri=vocabulary_file_uri,
            )
        else:
            print(f"An error occurred: {e}")
            return
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload File to S3 and Create or Update AWS Transcribe Custom Vocabulary"
    )
    parser.add_argument(
        "--file_name", required=True, help="The name of the file to upload"
    )
    parser.add_argument(
        "--bucket", required=True, help="The name of the S3 bucket to upload to"
    )
    parser.add_argument(
        "--vocabulary_name", required=True, help="The name of the custom vocabulary"
    )
    parser.add_argument(
        "--language_code", required=True, help="The language code for the vocabulary"
    )

    args = parser.parse_args()

    if not os.path.exists(args.file_name):
        print("The file does not exist.")
        exit(1)

    s3 = boto3.client("s3")
    client = boto3.client("transcribe")

    # Upload the file to S3
    upload_file_to_s3(args.file_name, args.bucket)

    # S3 URI for the vocabulary file
    s3_uri = f"s3://{args.bucket}/{args.file_name}"

    # Create or Update the vocabulary
    response = create_or_update_vocabulary(
        client, args.vocabulary_name, s3_uri, args.language_code
    )

    print(response)
