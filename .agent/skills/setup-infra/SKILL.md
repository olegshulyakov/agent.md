---
name: setup-infra
description: >
  Generates infrastructure-as-code scaffolding using Terraform or Pulumi for cloud infrastructure (AWS, GCP,
  Azure) including compute, networking, storage, databases, and IAM. Use this skill whenever the user wants
  to set up cloud infrastructure, write Terraform or Pulumi code, provision AWS/GCP/Azure resources, create
  a VPC, deploy a database, set up an ECS or Kubernetes cluster, or asks to "write Terraform for X",
  "provision this infrastructure", "set up AWS resources", "create a Pulumi stack", "scaffold cloud infra",
  or "infrastructure as code for this architecture". Also trigger for networking setup, IAM role creation,
  and managed service provisioning.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# setup-infra

Generate **infrastructure-as-code** scaffolding using Terraform (default) or Pulumi for the target cloud and services.

## Tool & cloud detection

Identify the IaC tool and cloud:

1. **Explicit mention**: "Terraform", "Pulumi", "CDK", "Bicep"
2. **Existing files**: `.tf` files → Terraform, `Pulumi.yaml` → Pulumi
3. **Default**: Terraform (most widely used, HCL)

Cloud provider:
1. **Explicit mention**: "AWS", "GCP", "Azure", "Google Cloud"
2. **Context clues**: Service names ("EC2", "S3", "GKE", "AKS")
3. **Default**: AWS

## Output structure

Produce modular Terraform code organized by concern:

```
infrastructure/
├── main.tf          # Root module: provider config, module calls
├── variables.tf     # Input variables with descriptions and defaults
├── outputs.tf       # Exported values (IDs, ARNs, endpoints)
├── versions.tf      # Provider version constraints
└── modules/
    ├── networking/  # VPC, subnets, security groups
    ├── compute/     # ECS, EC2, Lambda, or K8s
    └── database/    # RDS, DynamoDB, etc.
```

## Terraform output format

Always produce:
1. Complete `.tf` files with all required fields
2. Clear variable descriptions and sensible defaults
3. Inline comments explaining non-obvious choices
4. Resource naming using variables (not hardcoded)
5. Tags/labels on all resources

### Example: AWS base infrastructure

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

# variables.tf
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
}

# main.tf
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      Application = var.app_name
      ManagedBy   = "terraform"
    }
  }
}

module "networking" {
  source      = "./modules/networking"
  environment = var.environment
  app_name    = var.app_name
}

module "database" {
  source             = "./modules/database"
  environment        = var.environment
  app_name           = var.app_name
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
}
```

### Networking module example

```hcl
# modules/networking/main.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "${var.app_name}-${var.environment}-vpc" }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = { Name = "${var.app_name}-private-${count.index}" }
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 10)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = { Name = "${var.app_name}-public-${count.index}" }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.app_name}-igw" }
}
```

### RDS module example

```hcl
# modules/database/main.tf
resource "aws_db_subnet_group" "main" {
  name       = "${var.app_name}-${var.environment}"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "main" {
  identifier        = "${var.app_name}-${var.environment}"
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = var.instance_class
  allocated_storage = var.storage_gb

  db_name  = var.database_name
  username = var.database_username
  password = random_password.db.result  # never hardcode

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 7
  deletion_protection     = var.environment == "prod"
  skip_final_snapshot     = var.environment != "prod"

  storage_encrypted = true
}

resource "random_password" "db" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}
```

## IAM best practices

Always follow least-privilege IAM:

```hcl
# IAM role for ECS task — only what the app needs
resource "aws_iam_role" "app" {
  name = "${var.app_name}-${var.environment}-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "app" {
  role = aws_iam_role.app.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = [aws_secretsmanager_secret.db_password.arn]
      }
    ]
  })
}
```

## Security defaults

Always include these in generated infrastructure:
- Private subnets for compute and database resources
- Public subnets only for load balancers
- Security groups with minimum required ports (no 0.0.0.0/0 on database ports)
- Encryption at rest for databases and S3 buckets
- Secrets in AWS Secrets Manager (never hardcoded)
- Multi-AZ for production databases
- `deletion_protection = true` for production resources

## Setup instructions to include

Always end with:
```bash
# Initialize and deploy
terraform init
terraform plan -var="app_name=myapp" -var="environment=dev"
terraform apply -var="app_name=myapp" -var="environment=dev"

# Destroy
terraform destroy -var="app_name=myapp" -var="environment=dev"
```
