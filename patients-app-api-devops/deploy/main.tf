terraform {
  backend "s3" {
    bucket         = "patients-app-api-devops-tfstate"
    key            = "patients-app.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "patients-app-api-devops-tf-state-lock"
  }
}

provider "aws" {
  region  = "us-east-1"
  version = "~> 2.50.0"
}

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}

data "aws_region" "current" {}
