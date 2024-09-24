terraform {
  required_version = "1.6.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_iam_user" "transcribe_user" {
  # checkov:skip=CKV_AWS_273:ease of use skip
  name = "aws-transcribe-user"
}

resource "aws_iam_user_policy_attachment" "transcribe_policy_attachment" {
  # checkov:skip=CKV_AWS_40:ease of use skip
  user       = aws_iam_user.transcribe_user.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonTranscribeFullAccess"
}

resource "aws_s3_bucket" "transcribe_custom_cs_vocab_bucket" {
  # checkov:skip=CKV_AWS_144
  # checkov:skip=CKV2_AWS_62
  # checkov:skip=CKV_AWS_18:it's the default
  # checkov:skip=CKV2_AWS_61
  # checkov:skip=CKV2_AWS_6:already setby defalut
  # checkov:skip=CKV_AWS_21
  # checkov:skip=CKV_AWS_145
  bucket = "my-transcribe-custom-cs-vocab-bucket"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_policy" "transcribe_custom_cs_vocab_bucket_policy" {
  # checkov:skip=CKV_AWS_144
  bucket = aws_s3_bucket.transcribe_custom_cs_vocab_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "s3:*",
        Effect = "Allow",
        Resource = [
          "arn:aws:s3:::my-transcribe-custom-cs-vocab-bucket/*",
          "arn:aws:s3:::my-transcribe-custom-cs-vocab-bucket"
        ],
        Principal = {
          AWS = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${aws_iam_user.transcribe_user.name}"]
        }
      }
    ]
  })
}

data "aws_caller_identity" "current" {}
