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
                echo 'Starting Flask application...'
                sh 'python3 app.py &'
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests using unittest...'
                sh 'python3 test_app.py'
            }
        }
        stage('Dependency Check') {
            steps {
                echo 'Running OWASP Dependency-Check...'
                sh '/usr/local/bin/dependency-check --updateonly'
                sh '/usr/local/bin/dependency-check --project "colmoschin_assignment_1" --scan . --format "ALL" --out "./dependency-check-report"'
    }
}

    }
}
