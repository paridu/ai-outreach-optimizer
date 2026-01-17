# INFRASTRUCTURE AS CODE: BASE CLOUD RESOURCES
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# RDS Instance for Customer Data & Segment Logs
resource "aws_db_instance" "postgres_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.t3.medium"
  db_name              = "personalization_db"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
  publicly_accessible  = false
}

# ECR Repository for API Container
resource "aws_ecr_repository" "api_repo" {
  name                 = "ai-trigger-api"
  image_tag_mutability = "IMMUTABLE"
}

# S3 Bucket for ML Model Artifacts
resource "aws_s3_bucket" "model_registry" {
  bucket = "ai-personalization-model-registry"
}

variable "db_username" { type = string }
variable "db_password" { type = string }