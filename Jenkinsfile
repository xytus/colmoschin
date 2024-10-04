pipeline {
    agent any
    environment {
        ZAP_HOST = '192.168.1.5'           // IP address of the Kali Linux VM where OWASP ZAP is running
        LOCAL_APP_URL = 'http://192.168.1.6:5000' // URL of the Flask application running on the Jenkins (Ubuntu) server
    }
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
                sh 'nohup python3 app.py &'
                sleep 10
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests using unittest...'
                sh 'python3 test_app.py'
            }
        }
        stage('Run ZAP Spider Scan') {
            steps {
                echo 'Running OWASP ZAP Spider scan...'
                script {
                    // Include the correct content-type header
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/spider/action/scan/" \
                         -H "Content-Type: application/x-www-form-urlencoded" \
                         -d "url=${LOCAL_APP_URL}&recurse=true"
                    """
                }
                sleep 30 // Adjust the sleep time based on the size of the target application
            }
        }
        stage('Run ZAP Active Scan') {
            steps {
                echo 'Running OWASP ZAP Active scan...'
                script {
                    // Include the correct content-type header
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/ascan/action/scan/" \
                         -H "Content-Type: application/x-www-form-urlencoded" \
                         -d "url=${LOCAL_APP_URL}"
                    """
                }
                sleep 60 // Adjust the sleep time based on the size of the target application
            }
        }
        stage('Save ZAP Report') {
            steps {
                echo 'Saving OWASP ZAP report...'
                // Retrieve the ZAP report in XML format
                sh """
                curl -X GET "http://${ZAP_HOST}:8080/OTHER/core/other/xmlreport/" \
                     -H "Content-Type: application/x-www-form-urlencoded" \
                     -o zap_report.xml
                """
            }
        }
        stage('Publish ZAP Report') {
            steps {
                echo 'Publishing OWASP ZAP report...'
                // Publish the OWASP ZAP report in Jenkins
                publishHTML(target: [
                    reportName: 'OWASP ZAP Report',
                    reportDir: '',
                    reportFiles: 'zap_report.xml',
                    keepAll: true,
                    alwaysLinkToLastBuild: true,
                    allowMissing: false
                ])
            }
        }
    }
}
