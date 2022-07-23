variable "prefix" {
  default     = "kubeform"
  description = "Common prefix for AWS resources names"
}

variable "aws_region" {
  default     = "ap-northeast-2"
  description = "AWS Region to deploy VPC"
}

variable "vpc_cidr" {
  default     = "10.10.0.0/16"
  description = "AWS VPC CIDR range"
}
