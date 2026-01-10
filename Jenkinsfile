pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10')) // Keep last 10 builds
        timestamps()                                  // Add timestamps to logs
        timeout(time: 1, unit: 'HOURS')               // Timeout after 1 hour
    }

    triggers {
        pollSCM('H/5 * * * *') // Poll GitHub every 5 minutes
    }

    parameters {
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region')
        string(name: 'ECR_REPO_NAME', defaultValue: 'fastapi-app-repo', description: 'ECR Repository Name')
        string(name: 'EC2_KEY_NAME', defaultValue: 'Jenkins', description: 'AWS Key Pair Name for EC2')
        booleanParam(name: 'DESTROY_INFRA', defaultValue: false, description: 'Set to true to destroy infrastructure instead of deploying')
    }

    environment {
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
        AWS_CREDENTIALS_ID = "jenkins-deploy-aws"
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: env.AWS_CREDENTIALS_ID, accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        // Dynamically fetch and set environmental variables
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        
                        // Set variables at the global env level so they persist across stages
                        env.AWS_ACCOUNT_ID = accountId
                        env.ECR_URL = "${accountId}.dkr.ecr.${params.AWS_REGION}.amazonaws.com"
                        env.IMAGE_NAME = "${env.ECR_URL}/${params.ECR_REPO_NAME}"
                        
                        echo "--- Environment Initialized ---"
                        echo "AWS Account: ${env.AWS_ACCOUNT_ID}"
                        echo "ECR URL: ${env.ECR_URL}"
                    }
                }
            }
        }

        stage('Infrastructure Provisioning') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: env.AWS_CREDENTIALS_ID, accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
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
        }

        stage('Build & Push to ECR') {
            when {
                expression { !params.DESTROY_INFRA }
            }
            steps {
                script {
                    // Safety check to ensure variables are present
                    if (!env.ECR_URL || env.ECR_URL == "null") {
                        error "ECR_URL is not set. The Initialize stage might have failed or variables did not propagate."
                    }

                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: env.AWS_CREDENTIALS_ID, accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                        sh "aws ecr get-login-password --region ${params.AWS_REGION} | podman login --username AWS --password-stdin ${env.ECR_URL}"
                        
                        dir('app') {
                            sh "podman build --platform linux/amd64 -t ${env.IMAGE_NAME}:latest ."
                            sh "podman push ${env.IMAGE_NAME}:latest"
                        }
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
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: env.AWS_CREDENTIALS_ID, accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
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
            cleanWs()
        }
    }
}
