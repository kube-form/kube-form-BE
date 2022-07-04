module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "17.24.0"
  cluster_name    = local.cluster_name
  cluster_version = "1.20"
  subnets         = module.vpc.private_subnets

  cluster_endpoint_private_access = false
  cluster_endpoint_public_access = true

  vpc_id = module.vpc.vpc_id
  

  /*
  node_groups are aws eks managed nodes whereas worker_groups are self managed nodes. 
  Among many one advantage of worker_groups is that you can use your custom AMI for the nodes.
  */

  node_groups = [
    {
      name          = "worker-group-1"
      instance_type = "t2.small"
      additional_userdata           = "echo foo bar"
      source_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
      desired_capacity          = 1
    }
  ]
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}