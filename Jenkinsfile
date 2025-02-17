pipeline {
    agent any

    environment {
        ACR_REGISTRY = "carpredictionregistry.azurecr.io"
        IMAGE_NAME = "${ACR_REGISTRY}/car-price-prediction"
        TAG = "latest"
        // DOCKER_CREDS = credentials('azure-acr-credential')  
    }

    stages {
        stage('Validate environment') {
            steps {
                sh 'docker --version'
                sh 'python3 --version'
                sh 'docker ps'  // Verify Docker access
            }
        }
    }
}
    //     stage('Build and Push') {
    //         steps {
    //             script {
    //                 // Login to ACR
    //                 sh "docker login ${ACR_REGISTRY} -u ${DOCKER_CREDS_USR} -p ${DOCKER_CREDS_PSW}"
                    
    //                 // Build image
    //                 sh "docker build -t ${IMAGE_NAME}:${TAG} ."
                    
    //                 // Push image
    //                 sh "docker push ${IMAGE_NAME}:${TAG}"
    //             }
    //         }
    //     }

    //     stage('Run Tests') {
    //         steps {
    //             script {
    //                 // Run tests in the built image
    //                 sh "docker run --rm ${IMAGE_NAME}:${TAG} pytest tests/"
    //             }
    //         }
    //     }

    //     stage('Deploy') {
    //         steps {
    //             script {
    //                 // Helm deployment (requires configured kubeconfig)
    //                 sh """
    //                 helm upgrade --install hpp ./helm-charts/hpp \
    //                     --namespace model-serving \
    //                     --set image.repository=${IMAGE_NAME} \
    //                     --set image.tag=${TAG}
    //                 """
    //             }
    //         }
    //     }
    // }
