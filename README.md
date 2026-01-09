# Simple FastAPI App Deployment with Jenkins, Terraform, Docker, and UV

This project provides a complete setup to deploy a simple FastAPI application to an AWS EC2 instance using a CI/CD pipeline managed by Jenkins, infrastructure provisioned by Terraform, and Python environment managed by UV.

## Project Structure

- `app/`: Contains the FastAPI application, `pyproject.toml`, `uv.lock`, and `Dockerfile`.
- `terraform/`: Contains Terraform configuration files to provision AWS infrastructure.
- `Jenkinsfile`: Defines the CI/CD pipeline stages.

## Prerequisites

1. **AWS Account**: You need an AWS account and credentials configured.
2. **Terraform**: Installed on the Jenkins agent.
3. **Docker**: Installed on the Jenkins agent and the target EC2 instance.
4. **Jenkins**: A Jenkins server with the following plugins:
   - Pipeline
   - Git
   - SSH Agent
   - Terraform Plugin (optional, can use shell commands)

## Setup Instructions

### 1. AWS Credentials
Ensure Jenkins has access to AWS credentials. You can environment variables or IAM roles if Jenkins is running on an EC2 instance.

### 2. Jenkins Credentials
Add the following credentials to Jenkins:
- `aws-ssh-key`: The SSH private key (`.pem`) used to access the EC2 instances.
- `docker-hub-credentials`: (Optional) Your Docker Hub username and password.

### 3. Terraform Configuration
Update `terraform/variables.tf` or provide a `terraform.tfvars` file with:
- `key_name`: The name of your AWS key pair.
- `aws_region`: Your preferred AWS region.

### 4. GitHub Repository
Initialize a git repository, commit the files, and push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 5. Jenkins Pipeline
1. Create a new "Pipeline" job in Jenkins.
2. Under "Pipeline definition", select "Pipeline script from SCM".
3. Choose "Git" and provide your repository URL.
4. Save and click "Build Now".

## Accessing the App
Once the pipeline completes successfully, you can access the FastAPI app at:
`http://<EC2_PUBLIC_IP>:8000`

The public IP can be found in the Jenkins build console or via the Terraform output.
