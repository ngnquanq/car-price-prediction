pipeline {
    agent any

    // Configure environment variables
    environment {
        DOCKER_REGISTRY    = "carprediction.azurecr.io"         // e.g. "mycompany.azurecr.io" 
        IMAGE_NAME         = "car-price-prediction"
        IMAGE_TAG          = "latest"                           // or a dynamic tag like "${env.BUILD_NUMBER}"
        
        AZURE_CRED_ID      = "azure-sp-credentials"             // Jenkins credentials for Azure (Service Principal)
        AKS_RESOURCE_GROUP = "myResourceGroup"
        AKS_CLUSTER_NAME   = "myAksCluster"
        HELM_RELEASE_NAME  = "car-price-prediction"
        HELM_CHART_PATH    = "./helm/car-price-prediction"      // Path to your Helm chart in the repo
        
        // Optionally set tenant and subscription as environment variables
        // AZURE_TENANT_ID    = "your-tenant-id"
        // AZURE_SUBSCRIPTION = "your-subscription-id"
    }

    stages {
        stage('Install Python Dependencies') {
            steps {
                sh "python3 -m pip install -r requirements.txt"
            }
        }

        stage('Run Pytest') {
            steps {
                dir('test') {
                    sh "pytest --maxfail=1 --disable-warnings -q"
                }
            }
        }
        stage('Checkpoint 1') {
            steps {
                echo 'Run Pytest successfully, now login to Azure'
            }
        }
        stage('Login to Azure') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${AZURE_CRED_ID}", usernameVariable: 'AZURE_CLIENT_ID', passwordVariable: 'AZURE_CLIENT_SECRET')]) {
                    sh """
                    az login --identity --allow-no-subscriptions
                    """
                }
            }
        }

        stage('Sign in to ACR') {
            steps {
                sh "az acr login --name ${DOCKER_REGISTRY.split('\\.')[0]}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG ."
                }
            }
        }

        stage('Push to ACR') {
            steps {
                script {
                    // Login to ACR using the registry name extracted from the full registry URL.
                    sh """
                    az acr login --name ${DOCKER_REGISTRY.split('\\.')[0]}
                    docker push $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Pull from ACR (Optional)') {
            steps {
                script {
                    sh "docker pull $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }

        stage('Deploy to AKS via Helm') {
            steps {
                script {
                    // Fetch AKS credentials (updates kubeconfig)
                    sh "az aks get-credentials -g $AKS_RESOURCE_GROUP -n $AKS_CLUSTER_NAME --overwrite-existing"
                    
                    // Deploy with Helm. The image.pullPolicy is set to 'Always' to ensure the latest image is pulled.
                    sh """
                    helm upgrade --install $HELM_RELEASE_NAME $HELM_CHART_PATH \
                        --set image.repository=$DOCKER_REGISTRY/$IMAGE_NAME \
                        --set image.tag=$IMAGE_TAG \
                        --set image.pullPolicy=Always
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean up local Docker image to free up space
            sh "docker rmi $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG || true"
        }
    }
}
