# HyperCode V3.0 - AWS EKS Infrastructure
# Provisioned via Terraform

provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-west-2"
}

variable "cluster_name" {
  default = "hypercode-cluster-v3"
}

# VPC Module
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "hypercode-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b", "${var.region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Terraform   = "true"
    Environment = "production"
    Project     = "HyperCode"
  }
}

# EKS Cluster Module
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.27"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id

  eks_managed_node_groups = {
    # General Purpose Node Group (API, Orchestrator)
    general = {
      min_size     = 2
      max_size     = 5
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
    
    # High Performance Node Group (Agents, LLM processing)
    agents = {
      min_size     = 1
      max_size     = 10
      desired_size = 2

      instance_types = ["c6i.large"] # Compute optimized
      capacity_type  = "SPOT"        # Cost optimization
      
      labels = {
        role = "agent-worker"
      }
      
      taints = {
        dedicated = {
          key    = "workload"
          value  = "agents"
          effect = "NO_SCHEDULE"
        }
      }
    }
  }

  # Enable OIDC for IRSA (IAM Roles for Service Accounts)
  enable_irsa = true

  tags = {
    Environment = "production"
    Project     = "HyperCode"
  }
}

# Kubernetes Provider
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    command     = "aws"
  }
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  value = module.eks.cluster_security_group_id
}
