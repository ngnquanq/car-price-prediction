pipeline{
    //specifies where the pipeline or a specific stage will run
    agent any

    // Setup some options
    options {
        // Set max of log to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '5'))
        // Set the timeout for the pipeline
        timeout(time: 1, unit: 'HOURS')
        // Enable timestamps at each job of the pipeline
        timestamps()
    }

    // Setup environment variables
    environment {
        // registry w my dockerhub username
        registry = "ngnquanq/car-price-prediction"
        registryCredential= 'dockerhub'
    }

    // Stages of the pipeline
    stages {

        // Stage 1: test the code
        stage('Test'){ 
            steps {
                // Print somethings to the screen
                echo  'Prepare to test the code ... '
                // install required packages
                echo 'Installing required packages ... '
                // checkout the code from the github repo to 
                echo 'Check for model correctness w 5% fault tolerance ... '
                echo 'Suppose all the tests passed :)'
                // More test to come
                echo 'More tests to come, however, this is just it for now'
            }
        }
        // Stage 2: build the docker image
        stage('Build Image'){
            steps {
                echo 'Prepare to build Image ... '
                // Build the docker image
                script {
                    // Build the docker image for deployment
                    echo 'Building the docker image for deployment ... '
                    // Replace the registry with the docker image
                    echo 'Replace the registry with the docker image ... '
                    //dockerImage = docker.build registry + ":$BUILD_NUMBER"
                    //  Push the docker image to the docker hub
                    // echo 'Push the docker image to the docker hub ... '
                    // docker.withRegistry( '', registryCredential ) {
                    //     dockerImage.push()
                    //     dockerImage.push("latest")
                    // }
                    echo 'Building the deployment package ... '
                    // Replace the registry with the deployment package
                    echo 'Replace the registry with the deployment package ... '
                    //  Push the deployment package to the repository
                    echo 'Push the deployment package to the repository ... '
                // Deploy the docker image
                script {
                    // Deploy the docker image to the kubernetes cluster
                    echo 'Deploy the models ... '
                    echo 'Running a script to trigger pull and start a docker container'
                }
            }
        }
    }
    }
}