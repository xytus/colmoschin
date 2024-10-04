pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                echo 'Cloning the GitHub repository...'
                git branch: 'main', url: 'https://github.com/xytus/colmoschin.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip3 install flask'
                sh 'pip3 install pytest'
                echo 'Starting Flask application...'
                sh 'python3 app.py &'
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests using pytest...'
                sh 'pytest test_app.py'
            }
        }
    }
}
