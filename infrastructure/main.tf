terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-2"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
}

# Secure S3 Bucket for De-identified Research Data
resource "aws_s3_bucket" "research_archive" {
  bucket = "iu-sca-research-archive-demo"

  tags = {
    Environment = "Research"
    Compliance  = "HIPAA-Deidentified"
    ManagedBy   = "Terraform"
  }
}

# Enforce Server-Side Encryption (AES-256)
resource "aws_s3_bucket_server_side_encryption_configuration" "archive_encryption" {
  bucket = aws_s3_bucket.research_archive.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block All Public Access (Zero-Trust Governance)
resource "aws_s3_bucket_public_access_block" "archive_lockdown" {
  bucket = aws_s3_bucket.research_archive.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
