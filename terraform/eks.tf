data "aws_caller_identity" "current" {}

# EKS Terraform - Cluster
resource "aws_eks_cluster" "eks_cluster" {
  depends_on = [aws_iam_role_policy_attachment.eks_iam_policy_attachment]

  name     = local.cluster_name
  role_arn = aws_iam_role.eks_iam_role.arn

  vpc_config {
    subnet_ids = concat(module.vpc.public_subnets, module.vpc.private_subnets)
  }

  tags = merge(
    {
      Name = local.cluster_name
    },
    local.common_tags
  )
}

# EKS Terraform - Creating the private EKS Node Group
resource "aws_eks_node_group" "private_node_group" {
  depends_on = [
    aws_iam_role_policy_attachment.worker_node_policy_attachment,
    aws_iam_role_policy_attachment.cni_policy_attachment,
    aws_iam_role_policy_attachment.ecr_readonly_policy_attachment
  ]

  cluster_name    = aws_eks_cluster.eks_cluster.name
  node_group_name = "${local.cluster_name}-private-ng"
  node_role_arn   = aws_iam_role.eks_node_role.arn

  subnet_ids = module.vpc.private_subnets

  ami_type       = "AL2_x86_64"
  capacity_type  = "ON_DEMAND"
  instance_types = [var.instance_type]
  disk_size      = 8

  scaling_config {
    desired_size = var.node_group_num
    max_size     = 6
    min_size     = 1
  }

  update_config {
    max_unavailable = 2
  }

  tags = merge(
    {
      Name = local.cluster_name
    },
    local.common_tags
  )
}
