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
                sh 'pip3 install -r requirements.txt'
                sh 'pip3 install pytest==6.2.4'
                echo 'Starting Flask application...'
                sh 'python3 app.py &'
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests using pytest...'
                sh '/usr/local/bin/pytest test_app.py'

            }
        }
    }
}
