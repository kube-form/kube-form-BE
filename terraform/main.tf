locals {
  prefix         = "kubeform"
  vpc_name       = "${local.prefix}-vpc"
  vpc_cidr       = var.vpc_cidr
  cluster_name   = "${local.prefix}-cluster"
  aws_account_id = data.aws_caller_identity.current.account_id
  common_tags = {
    Environment = "dev"
    Project     = "kubeform"
  }
}