pipeline {
    agent any
    environment {
        REGISTRY = "carpredictionregistry.azurecr.io"
        IMAGE_NAME = "car-price-prediction"
        KUBE_CONFIG = "aks-kubeconfig" // Matches credentials ID from Jenkins
        HELM_CHART_PATH = "./k8s-resources" // From your codebase
        MONITORING_NAMESPACE = "monitoring"
    }
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    stages {
        stage('Build Image') {
            steps {
                script {
                    docker.build("${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_TAG}")
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_TAG}").inside {
                        sh 'pytest tests/' // Using pytest from your custom Dockerfile
                    }
                }
            }
        }
        
        stage('Push to ACR') {
            steps {
                script {
                    docker.withRegistry("https://${env.REGISTRY}", 'acr-credentials') {
                        docker.image("${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_TAG}").push()
                    }
                }
            }
        }
        
        stage('Deploy to AKS') {
            steps {
                withCredentials([file(credentialsId: env.KUBE_CONFIG, variable: 'KUBECONFIG_FILE')]) {
                    script {
                        sh """
                        export KUBECONFIG=${KUBE_CONFIG_FILE}
                        helm upgrade --install carprice-app ${env.HELM_CHART_PATH} \
                            --namespace production \
                            --set image.repository=${env.REGISTRY}/${env.IMAGE_NAME} \
                            --set image.tag=${env.BUILD_TAG} \
                            --set autoscaling.enabled=true \
                            --wait --timeout 5m
                        """
                    }
                }
            }
        }
        
        stage('Update Monitoring') {
            steps {
                withCredentials([file(credentialsId: env.KUBE_CONFIG, variable: 'KUBECONFIG_FILE')]) {
                    sh """
                    export KUBECONFIG=${KUBE_CONFIG_FILE}
                    # Add new deployment to monitoring targets
                    kubectl label svc carprice-app -n production monitoring=enabled
                    # Restart monitoring pods to pick up changes
                    kubectl rollout restart deployment -n ${env.MONITORING_NAMESPACE}
                    """
                }
            }
        }
        
        stage('Rollback Check') {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        input message: 'Verify deployment success. Rollback if needed?', 
                              ok: 'Deployment Successful'
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            script {
                docker.image("${env.REGISTRY}/${env.IMAGE_NAME}:${env.BUILD_TAG}").prune()
            }
        }
        failure {
            emailext (
                subject: "🚨 Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """Check failed pipeline: ${env.BUILD_URL}
                
                Error Details:
                ${currentBuild.currentResult}: ${currentBuild.currentBuild.result}
                
                Last 50 lines of log:
                ${currentBuild.rawBuild.getLog(50).join('\n')}
                """,
                to: 'devops@example.com'
            )
            
            // Automatic rollback on failure
            withCredentials([file(credentialsId: env.KUBE_CONFIG, variable: 'KUBECONFIG_FILE')]) {
                sh """
                export KUBECONFIG=${KUBE_CONFIG_FILE}
                helm rollback carprice-app 0 -n production
                """
            }
        }
    }
}