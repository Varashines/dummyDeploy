
# Enterprise GenAI Microservice: FastAPI + AWS Bedrock + ECS

This project provides a robust, production-ready CI/CD pipeline to deploy a Generative AI-powered FastAPI microservice to **Amazon ECS (EC2-backed)** using Jenkins and Terraform. 

The application integrates directly with **AWS Bedrock** for LLM capabilities and **DynamoDB** for data management, serving as a template for secure, scalable MLOps and backend architecture.

## 🚀 Key Features

- **Generative AI Integration**: Securely invokes AWS Bedrock (`amazon.titan-text-express-v1`) via `boto3` for prompt-based text generation.
- **Modern Python Tooling**: Utilizes `uv` for lightning-fast dependency resolution, environment management, and optimized Docker builds.
- **Infrastructure as Code (IaC)**: Fully automated AWS resource provisioning (ALB, ECS Cluster/Service, ECR, IAM, Security Groups) using Terraform with an S3 Remote Backend.
- **Automated CI/CD**: A declarative Jenkins pipeline featuring automated SCM polling, dynamic AWS credential binding, and daemon-less container builds using Podman (multi-arch `linux/amd64`).
- **Strict Security & Observability**: Implements least-privilege IAM Task Roles (explicitly scoped for Bedrock and DynamoDB access) and centralized logging via AWS CloudWatch.

## 📁 Project Structure

- `app/`: The FastAPI application code (`app.py`), modern dependency management (`pyproject.toml`, `uv.lock`), and a highly optimized multi-stage `Dockerfile`.
- `terraform/`: IaC configurations defining the complete AWS network and compute topology.
- `Jenkinsfile`: Multi-stage deployment pipeline (Initialize ➔ Provision IaC ➔ Build & Push ➔ Deploy to ECS).

## 💻 Local Development Setup

We use `uv` to guarantee rapid, reproducible local environments.

1. **Install `uv`**:
```bash
   curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
   
```

2. **Clone and Sync**:
```bash
git clone [https://github.com/Varashines/dummyDeploy.git](https://github.com/Varashines/dummyDeploy.git)
cd dummyDeploy/app
uv sync

```


3. **Run Locally**:
Ensure you have configured your local AWS credentials (`aws configure`) to test the Bedrock endpoints.
```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

```



## 🛠 Deployment Prerequisites

1. **AWS Account**: Infrastructure is deployed in `us-east-1`.
2. **Jenkins Agent**: Must have `terraform`, `aws-cli`, and `podman` installed.
3. **Jenkins Credentials**:
* `jenkins-deploy-aws`: AWS IAM credentials bound dynamically during the pipeline run.


4. **AWS Key Pair**: An existing key pair named `Jenkins` in your AWS region for EC2 host access.

## ⚙️ CI/CD & Infrastructure Deployment

1. **Terraform Remote State**: The project uses an S3 bucket for state locking and consistency. Ensure `terraform/main.tf` points to a valid, pre-existing bucket.
2. **Jenkins Pipeline**:
* Create a "Pipeline" job pointing to this GitHub repository.
* The pipeline will automatically poll for changes every 5 minutes (`H/5 * * * *`).


3. **Execution**:
* Push code to the `main` branch or trigger manually via "Build with Parameters". You can pass the `DESTROY_INFRA` boolean to cleanly tear down the environment.



## 🔗 Accessing the Application

After a successful deployment, the Terraform output will provide the Application Load Balancer (ALB) DNS name.

* **Root Endpoint**: `http://<ALB_DNS_NAME>/`
* **GenAI Endpoint**: `http://<ALB_DNS_NAME>/generate?prompt=YourPromptHere`
* **Interactive Swagger Docs**: `http://<ALB_DNS_NAME>/docs`
