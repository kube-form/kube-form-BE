provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}

resource "kubernetes_deployment" "kubeform-eks-deployment" {
  metadata {
    name = "kubeform-eks-deployment"
  }
  spec {
    replicas = 3
    selector {
      match_labels = {
        "app.kubernetes.io/name" = "kubeform-eks-deployment"
      }
    }
    template {
      metadata {
        labels = {
          "app.kubernetes.io/name" = "kubeform-eks-deployment"
        }
      }
      spec {
        container {
          image = "pengbai/docker-supermario"
          name  = "supermario"
        }
      }
    }
  }
}

resource "kubernetes_service" "kubeform-eks-deployment" {
  metadata {
    name = "kubeform-eks-deployment"
  }
  spec {
    selector = {
      "app.kubernetes.io/name" = "kubeform-eks-deployment"
    }
    port {
      port        = 8080
      target_port = 8080
    }
    type = "NodePort"
  }
}

resource "kubernetes_ingress_v1" "alb" {
  metadata {
    name = "alb"
    annotations = {
      "alb.ingress.kubernetes.io/scheme"      = "internet-facing",
      "alb.ingress.kubernetes.io/target-type" = "ip",
    }
  }
  spec {
    ingress_class_name = "alb"
    rule {
      http {
        path {
          backend {
            service {
              name = "kubeform-eks-deployment"
              port {
                number = 8080
              }
            }
          }
          path = "/*"
        }
      }
    }
  }
}