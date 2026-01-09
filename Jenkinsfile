pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10')) // Keep last 10 builds
        timestamps()                                  // Add timestamps to logs
        timeout(time: 1, unit: 'HOURS')               // Timeout after 1 hour
    }

    parameters {
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region')
        string(name: 'ECR_REPO_NAME', defaultValue: 'fastapi-app-repo', description: 'ECR Repository Name')
        string(name: 'EC2_KEY_NAME', defaultValue: 'Jenkins', description: 'AWS Key Pair Name for EC2')
        booleanParam(name: 'DESTROY_INFRA', defaultValue: false, description: 'Set to true to destroy infrastructure instead of deploying')
    }

    environment {
        // Add common tool paths for macOS Homebrew
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        
        AWS_ACCOUNT_ID = "976709231767" // Update with your actual AWS Account ID
        AWS_CREDENTIALS_ID = "jenkins-deploy-aws" // [PLACEHOLDER] Jenkins Credentials ID for AWS Access Key/Secret
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${params.AWS_REGION}.amazonaws.com"
        IMAGE_NAME = "${ECR_URL}/${params.ECR_REPO_NAME}"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Infrastructure Provisioning') {
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform init -no-color'
                        if (params.DESTROY_INFRA) {
                            sh "terraform destroy -auto-approve -no-color -var=\"key_name=${params.EC2_KEY_NAME}\""
                            currentBuild.result = 'SUCCESS'
                            return
                        } else {
                            sh "terraform apply -auto-approve -no-color -var=\"key_name=${params.EC2_KEY_NAME}\""
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
                    // Login to ECR using podman
                    sh "aws ecr get-login-password --region ${params.AWS_REGION} | podman login --username AWS --password-stdin ${ECR_URL}"
                    
                    dir('app') {
                        // Build using the UV-optimized Dockerfile with podman
                        sh "podman build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                        sh "podman push ${IMAGE_NAME}:${IMAGE_TAG}"
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
                    def clusterName = ""
                    def serviceName = ""
                    dir('terraform') {
                        clusterName = sh(script: "terraform output -raw ecs_cluster_name", returnStdout: true).trim()
                        serviceName = sh(script: "terraform output -raw ecs_service_name", returnStdout: true).trim()
                    }
                    
                    // Force a new deployment of the ECS service to pick up the new image
                    sh """
                        aws ecs update-service \
                            --cluster ${clusterName} \
                            --service ${serviceName} \
                            --force-new-deployment \
                            --region ${params.AWS_REGION}
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Build finished."
        }
        success {
            script {
                if (!params.DESTROY_INFRA) {
                    echo "Deployment Successful!"
                    dir('terraform') {
                        sh "terraform output ec2_public_ip"
                    }
                }
            }
        }
        cleanup {
            // Clean up workspace but PRESERVE terraform state files
            // otherwise terraform will try to recreate everything on every build
            cleanWs(
                deleteDirs: true,
                notFailBuild: true,
                patterns: [
                    [pattern: 'terraform/*.tfstate*', type: 'EXCLUDE'],
                    [pattern: 'terraform/.terraform/**', type: 'EXCLUDE']
                ]
            )
        }
    }
}
