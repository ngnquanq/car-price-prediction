pipeline {
    agent any

    stages {
        stage('Load Environment Variables') {
            steps {
                script {
                    // Read the .env file (assumed to be in properties file format: KEY=VALUE)
                    def envProps = readProperties file: '.env'
                    envProps.each { key, value ->
                        env[key] = value
                    }
                    echo "Loaded environment variables: ${envProps}"
                }
            }
        }
        stage('Checkout') {
            steps {
                git url: 'https://github.com/your-org/your-repo.git', branch: 'main'
            }
        }
        stage('Run Tests') {
            steps {
                // Install Python dependencies and run tests.
                // Assumes a requirements.txt file is present and tests are located under a "tests/" directory.
                sh '''
                    echo "Installing Python dependencies..."
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    echo "Running pytest..."
                    pytest test
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
            }
        }
        stage('Tag and Push Image') {
            steps {
                script {
                    sh "docker tag ${env.IMAGE_NAME}:${env.IMAGE_TAG} ${env.REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "echo $PASSWORD | docker login ${env.REGISTRY} --username $USERNAME --password-stdin"
                    }
                    sh "docker push ${env.REGISTRY}/${env.IMAGE_NAME}:${env.IMAGE_TAG}"
                }
            }
        }
        stage('Deploy to AKS') {
            steps {
                withCredentials([file(credentialsId: env.KUBE_CONFIG, variable: 'KUBECONFIG_FILE')]) {
                    // Export the kubeconfig file so that Helm and kubectl can authenticate to AKS.
                    sh """
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        helm upgrade --install ${env.HELM_RELEASE} ./helm-chart/model-serving \\
                          --namespace model-serving \\
                          --set image.repository=${env.REGISTRY}/${env.IMAGE_NAME},image.tag=${env.IMAGE_TAG}
                    """
                }
            }
        }
    }
    post {
        failure {
            mail to: 'devops@example.com',
                 subject: "Jenkins Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Please check the Jenkins logs for details."
        }
    }
}
