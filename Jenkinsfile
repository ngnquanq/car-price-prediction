pipeline {
    agent any

    environment {
        ACR_REGISTRY = "carpredictionregistry.azurecr.io"  // Replace with your ACR name
        IMAGE_NAME = "${ACR_REGISTRY}/car-price-prediction"
        TAG = "latest"
        acrCredential = credentials('azure-acr-credential')  // Jenkins credential ID for ACR
    }

    stages {
        stage('Validate environment') {
            steps {
                script {
                    // Check Docker installation
                    sh(script: 'docker --version', label: 'Check Docker') 
                    
                    // Check Python installation
                    sh(script: 'python3 --version', label: 'Check Python')
                    
                    // Optional: Verify Azure CLI
                    sh(script: 'az --version', label: 'Check Azure CLI')
                    
                    // Verify Jenkins user permissions
                    sh(script: 'docker ps', label: 'Check Docker Access')
                }
            }
        }
    

        stage('Build Docker Image') {
            agent {
                docker {
                    image 'docker:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                script {
                    docker.withRegistry("https://${ACR_REGISTRY}", acrCredential) {
                        dockerImage = docker.build("${IMAGE_NAME}:${TAG}", "--build-arg ENV=prod .")
                    }
                }
            }
        }

        stage('Push to ACR') {
            steps {
                script {
                    docker.withRegistry("https://${ACR_REGISTRY}", acrCredential) {
                        dockerImage.push("${TAG}")
                    }
                }
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image "${IMAGE_NAME}:${TAG}"
                    reuseNode true
                }
            }
            steps {
                sh 'pytest tests/ --cov=app --cov-report=xml'  // Update path to your tests
            }
        }

        stage('Deploy with Helm') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm'
                        image "${IMAGE_NAME}:${TAG}"  // Use the built image
                        alwaysPullImage true
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        // Update Helm chart with new image tag
                        sh """
                        helm upgrade --install hpp ./helm-charts/hpp \
                            --namespace model-serving \
                            --set image.repository=${IMAGE_NAME} \
                            --set image.tag=${TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Cleanup and notifications
            deleteDir()
        }
        success {
            slackSend(color: "good", message: "Deployment succeeded: ${BUILD_URL}")
        }
        failure {
            slackSend(color: "danger", message: "Deployment failed: ${BUILD_URL}")
        }
    }
}