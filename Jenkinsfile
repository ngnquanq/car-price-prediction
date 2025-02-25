pipeline {
    agent any

    // Configure environment variables
    environment {
        DOCKER_REGISTRY    = "carpredictionregistry.azurecr.io"         // e.g. "mycompany.azurecr.io" 
        IMAGE_NAME         = "car-price-prediction"
        IMAGE_TAG          = "latest"                           // or a dynamic tag like "${env.BUILD_NUMBER}"
        
        AZURE_CRED_ID      = "azure-sp-credentials"             // Jenkins credentials for Azure (Service Principal)
        HELM_RELEASE_NAME  = "application"
        HELM_CHART_PATH    = "./helm/application"      // Path to your Helm chart in the repo
        
        // Optionally set tenant and subscription as environment variables
        // AZURE_TENANT_ID    = "your-tenant-id"
        // AZURE_SUBSCRIPTION = "your-subscription-id"
    }

    stages {
        stage('Install Python Dependencies') {
            steps {
                // Create a virtual environment called 'venv'
                sh "python3 -m venv venv"
                
                // Upgrade pip in the virtual environment
                sh "./venv/bin/pip install --upgrade pip"
                
                // Install the requirements using the virtual environment's pip
                sh "./venv/bin/pip install -r requirements-inference.txt"

                // Checkpoint 
                echo 'Install Python Dependencies successfully!'

            }
        }

        stage('Run Pytest') {
            steps {
                // should be sh "bash -c 'source ./venv/bin/activate && python create_model.py && pytest --maxfail=1 --disable-warnings -q'" during first time
                sh "bash -c 'source ./venv/bin/activate && pytest --maxfail=1 --disable-warnings -q'"
            }
        }




        // stage('Checkpoint 1') {
        //     steps {
        //         echo 'Run Pytest successfully, now login to Azure'
        //     }
        // }
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
                withCredentials([usernamePassword(credentialsId: 'azure-acr', 
                                                usernameVariable: 'ACR_USERNAME', 
                                                passwordVariable: 'ACR_PASSWORD')]) {
                    sh "sudo docker login ${DOCKER_REGISTRY} -u ${ACR_USERNAME} -p ${ACR_PASSWORD}"
                    //sh "az acr login --name carpredictionregistry --resource-group carPricePrediction"
                }
            }
        }


        stage('Build Docker Image') {
            steps {
                script {
                    sh "sudo docker build -t $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG ."
                }
            }
        }

        stage('Push to ACR') {
            steps {
                script {
                    // Login to ACR using the registry name extracted from the full registry URL.
                    
                    sh "sudo docker push $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
                    
                }
            }
        }

        stage('Pull from ACR (Optional)') {
            steps {
                script {
                    sh "sudo docker pull $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }

        stage('Set Azure Subscription') {
            steps {
                withCredentials([string(credentialsId: 'azure-subscription', variable: 'AZURE_SUBSCRIPTION')]) {
                    sh "az account set --subscription $AZURE_SUBSCRIPTION"
                }
            }
        }


        // stage('Deploy to AKS via Helm') {
        //     steps {
        //         script {
        //             // Fetch AKS credentials (updates kubeconfig)"
        //             sh "az aks get-credentials --resource-group carprice-aks-rg --name carprice-aks --overwrite-existing"
        //             echo(message: 'Get kubectl from Azure')
        //             // Deploy with Helm. The image.pullPolicy is set to 'Always' to ensure the latest image is pulled.
        //             sh """
        //             helm upgrade --install $HELM_RELEASE_NAME $HELM_CHART_PATH --namespace model-serving -f $HELM_CHART_PATH/values.yaml 
        //             """
        //             echo(message: 'Deployed to AKS successfully! Now deploy the Ingress Controller')
        //             sh """
        //             helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx --set controller.admissionWebhooks.enabled=false
        //             """

        //         }
        //     }
        // }

        stage('Deploy to AKS via Helm') {
            steps {
                script {
                    // Update kubeconfig to point to your AKS cluster
                    sh "az aks get-credentials --resource-group carprice-aks-rg --name carprice-aks --overwrite-existing"
                    echo 'Kubeconfig updated.'

                    // Check application status in namespace "model-serving"
                    def appStatus = sh(script: "kubectl get pods -n model-serving | grep 'application' | grep -w Running", returnStatus: true)
                    echo "Application check exit code: ${appStatus}"

                    // If application is not running, deploy or upgrade the application via Helm
                    if (appStatus != 0) {
                        echo "Application is not fully running. Deploying application via Helm..."
                        sh """
                        helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} \
                            --namespace model-serving -f ${HELM_CHART_PATH}/values.yaml
                        """
                        echo "Application deployed successfully."
                    } else {
                        echo "Application is already running."
                    }

                    // Check for an external IP on the ingress-nginx-controller service in namespace "ingress-nginx"
                    def ingressIP = sh(
                        script: "kubectl get svc ingress-nginx-controller -n model-serving -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo ''",
                        returnStdout: true
                    ).trim()
                    echo "Ingress external IP: ${ingressIP}"

                    if (ingressIP) {
                        echo "Ingress is already installed with external IP: ${ingressIP}. Testing connectivity..."
                        sh "curl -v http://${ingressIP}"
                    } else {
                        echo "Ingress external IP not assigned or ingress not installed. Deploying ingress-nginx via Helm..."
                        sh """
                        helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
                            --namespace ingress-nginx --set controller.admissionWebhooks.enabled=false
                        """
                        echo "Ingress controller deployed successfully."

                        echo "Waiting for external IP assignment..."
                        timeout(time: 5, unit: 'MINUTES') {
                            waitUntil {
                                def ip = sh(
                                    script: "kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo ''",
                                    returnStdout: true
                                ).trim()
                                echo "Polling ingress external IP: ${ip}"
                                return ip != ""
                            }
                        }
                        ingressIP = sh(
                            script: "kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}' || echo ''",
                            returnStdout: true
                        ).trim()
                        echo "Ingress external IP after installation: ${ingressIP}"
                        sh "curl -v http://${ingressIP}"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up local Docker image to free up space
            sh "sudo docker rmi $DOCKER_REGISTRY/$IMAGE_NAME:$IMAGE_TAG || true"
        }
    }
}
