variable "region" {
  default     = "ap-northeast-2"
  description = "AWS region"
}

provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {}

locals {
  cluster_name = "kubeform-eks-${random_string.suffix.result}"
  description  = "cluster name : kubeform-eks-{random_string}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}
