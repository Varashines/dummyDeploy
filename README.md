# FastAPI ECS CI/CD with Jenkins & Terraform

This project provides a robust, production-ready CI/CD pipeline to deploy a FastAPI application to **Amazon ECS (EC2-backed)** using Jenkins and Terraform.

## 🚀 Key Features

- **Application**: FastAPI-based web service.
- **Dependency Management**: `uv` for lightning-fast, reproducible Python environments.
- **Containerization**: Podman for secure, daemon-less container builds (multi-arch `linux/amd64`).
- **Infrastructure (IaC)**: Terraform for automated AWS resource management.
- **State Management**: S3 Remote Backend for persistent Terraform state.
- **CI/CD**: Jenkins Pipeline with automated SCM polling.
- **Observability**: Centralized logging via AWS CloudWatch.

## 📁 Project Structure

- `app/`: FastAPI application, `pyproject.toml`, `uv.lock`, and `Dockerfile`.
- `terraform/`: Configuration for ECR, ECS (Cluster, Service, Task), EC2 (Host), and IAM.
- `Jenkinsfile`: Multi-stage pipeline (Initialize, Provision, Build, Push, Deploy).

## 🛠 Prerequisites

1.  **AWS Account**: Infrastructure is deployed in `us-east-1`.
2.  **Jenkins Agent**: Must have `terraform`, `aws-cli`, and `podman` installed.
3.  **Jenkins Credentials**: 
    - `jenkins-deploy-aws`: AWS IAM credentials (with `AdministratorAccess`).
4.  **AWS Key Pair**: An existing key pair named `Jenkins` in your AWS region.

## ⚙️ Setup & Deployment

1.  **Terraform Remote State**: The project uses an S3 bucket for state. Ensure `terraform/main.tf` points to a valid bucket.
2.  **Jenkins Pipeline**: 
    - Create a "Pipeline" job pointing to this GitHub repository.
    - The pipeline is configured to automatically poll for changes.
3.  **Triggering a Build**: 
    - Simply push code or manual trigger via "Build with Parameters".

## 🛡 Security & Best Practices

- **IAM Roles**: Uses specific Task and Instance roles with least-privilege principles.
- **Logging**: All container output is streamed to CloudWatch for debugging.
- **AMI Strategy**: Uses the latest **Amazon Linux 2023 (AL2023)** ECS-optimized AMI to ensure long-term support.
- **Cleanup**: Workspace is cleaned post-build while preserving Terraform state.

## 🔗 Accessing the App

After a successful deployment, the FastAPI root endpoint will be available at:
`http://<EC2_PUBLIC_IP>:8000/`

Interactive Documentation:
- **Swagger**: `http://<EC2_PUBLIC_IP>:8000/docs`
- **ReDoc**: `http://<EC2_PUBLIC_IP>:8000/redoc`
