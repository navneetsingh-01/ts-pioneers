terraform {
  required_version = ">= 1.4.6"
  backend "s3" {}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.61"
    }
  }
}

provider "aws" {
  region = var.region
  assume_role {
    role_arn = var.role_arn
  }
}

provider "vault" {
  address          = "https://vault.us-west-2.${var.env}.btna.sfdc.sh"
  token            = var.vault_token
  skip_child_token = true
}
