
################################################################################
# Basic
################################################################################

output "prefix" {
  value       = try(local.prefix, "")
  description = "Exported common resources prefix"
}

output "common_tags" {
  value       = try(local.common_tags, "")
  description = "Exported common resources tags"
}

output "vpc_id" {
  value       = try(module.vpc.vpc_id, "")
  description = "VPC ID"
}

output "public_subnets" {
  value       = try(module.vpc.public_subnets, "")
  description = "VPC public subnets' IDs list"
}

output "private_subnets" {
  value       = try(module.vpc.private_subnets, "")
  description = "VPC private subnets' IDs list"
}

output "cluster_name" {
  value       = try(local.cluster_name, "")
  description = "EKS cluster name"
}

################################################################################
# Cluster
################################################################################

output "cluster_arn" {
  description = "The Amazon Resource Name (ARN) of the cluster"
  value       = try(aws_eks_cluster.eks_cluster.arn, "")
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = try(aws_eks_cluster.eks_cluster.certificate_authority, "")
}

output "cluster_endpoint" {
  description = "Endpoint for your Kubernetes API server"
  value       = try(aws_eks_cluster.eks_cluster.endpoint, "")
}

output "cluster_oidc_issuer_url" {
  description = "The URL on the EKS cluster for the OpenID Connect identity provider"
  value       = try(aws_eks_cluster.eks_cluster.identity, "")
}

output "cluster_version" {
  description = "The Kubernetes version for the cluster"
  value       = try(aws_eks_cluster.eks_cluster.version, "")
}

output "cluster_platform_version" {
  description = "Platform version for the cluster"
  value       = try(aws_eks_cluster.eks_cluster.platform_version, "")
}

output "cluster_primary_security_group_id" {
  description = "Cluster security group that was created by Amazon EKS for the cluster. Managed node groups use this security group for control-plane-to-data-plane communication. Referred to as 'Cluster security group' in the EKS console"
  value       = try(aws_eks_cluster.eks_cluster.vpc_config[0].cluster_security_group_id, "")
}

