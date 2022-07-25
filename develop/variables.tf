variable "aws_region" {
  default = "ap-northeast-2"
}

locals {
  cluster_name = "kubeform-eks-${random_string.suffix.result}"
  description  = "cluster name : kubeform-eks-{random_string}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}