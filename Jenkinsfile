pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10')) // Keep last 10 builds
        timestamps()                                  // Add timestamps to logs
        timeout(time: 1, unit: 'HOURS')               // Timeout after 1 hour
        ansiColor('xterm')                            // Support for colored output
    }

    parameters {
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region')
        string(name: 'ECR_REPO_NAME', defaultValue: 'fastapi-app-repo', description: 'ECR Repository Name')
        string(name: 'EC2_KEY_NAME', defaultValue: 'your-aws-key-name', description: 'AWS Key Pair Name for EC2')
        booleanParam(name: 'DESTROY_INFRA', defaultValue: false, description: 'Set to true to destroy infrastructure instead of deploying')
    }

    environment {
        AWS_ACCOUNT_ID = "123456789012" // [PLACEHOLDER] Replace with your AWS Account ID
        AWS_CREDENTIALS_ID = "jenkins-deploy-aws" // [PLACEHOLDER] Jenkins Credentials ID for AWS Access Key/Secret
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${params.AWS_REGION}.amazonaws.com"
        IMAGE_NAME = "${ECR_URL}/${params.ECR_REPO_NAME}"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Infrastructure Provisioning') {
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform init'
                        if (params.DESTROY_INFRA) {
                            sh "terraform destroy -auto-approve -var=\"key_name=${params.EC2_KEY_NAME}\""
                            currentBuild.result = 'SUCCESS'
                            return
                        } else {
                            sh "terraform apply -auto-approve -var=\"key_name=${params.EC2_KEY_NAME}\""
                        }
                    }
                }
            }
        }

        stage('Build & Push to ECR') {
            when {
                expression { !params.DESTROY_INFRA }
            }
            steps {
                script {
                    // Login to ECR
                    // Assumes AWS CLI is installed and configured on Jenkins agent
                    // Or use withAWS credentials block if using AWS Steps plugin
                    sh "aws ecr get-login-password --region ${params.AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}"
                    
                    dir('app') {
                        // Build using the UV-optimized Dockerfile
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy to ECS') {
            when {
                expression { !params.DESTROY_INFRA }
            }
            steps {
                script {
                    // Force a new deployment of the ECS service to pick up the new image
                    // This is the simplest way to update tasks on EC2-backed ECS
                    sh """
                        aws ecs update-service \
                            --cluster fastapi-cluster \
                            --service fastapi-service \
                            --force-new-deployment \
                            --region ${params.AWS_REGION}
                    """
                }
            }
        }
    }

    post {
        always {
            // Optional: Clean up workspace
            cleanWs()
        }
        success {
            script {
                if (!params.DESTROY_INFRA) {
                    echo "Deployment Successful!"
                    sh "cd terraform && terraform output ec2_public_ip"
                }
            }
        }
    }
}
