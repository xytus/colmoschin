pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the GitHub repository...'
                git 'https://github.com/xytus/colmoschin.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Start Flask Application') {
            steps {
                echo 'Starting Flask application...'
                sh 'nohup python3 app.py > flask.log 2>&1 &'
            }
        }
    }
}
