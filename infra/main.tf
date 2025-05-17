# Terraform configuration for grimOS infrastructure

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "aws" {
  region = "us-east-1"
}

resource "kubernetes_namespace" "grimos" {
  metadata {
    name = "grimos"
  }
}

resource "aws_vpc" "grimos_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "grimos_subnets" {
  count = 2
  vpc_id     = aws_vpc.grimos_vpc.id
  cidr_block = cidrsubnet(aws_vpc.grimos_vpc.cidr_block, 8, count.index)
}

resource "aws_iam_role" "eks_role" {
  name = "eks-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_eks_cluster" "grimos_cluster" {
  name     = "grimos-cluster"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = aws_subnet.grimos_subnets[*].id
  }
}

resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "grimos-backend"
    namespace = kubernetes_namespace.grimos.metadata[0].name
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "grimos-backend"
      }
    }

    template {
      metadata {
        labels = {
          app = "grimos-backend"
        }
      }

      spec {
        container {
          image = "${var.docker_registry}/grimos-backend:latest"
          name  = "grimos-backend"

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}
