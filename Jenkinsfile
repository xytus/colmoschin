pipeline {
    agent any
    environment {
        ZAP_HOST = '192.168.1.5'           // IP address of the Kali Linux VM where OWASP ZAP is running
        LOCAL_APP_URL = 'http://192.168.1.6:5000' // URL of the Flask application running on the Jenkins (Ubuntu) server
        API_KEY = 'efvupltk0ia150atbs2prendc9'  // Include your ZAP API Key here if required
        SSH_PASSWORD = 'colmoschin'   // Replace with your actual password for the Kali machine
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
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests using unittest...'
                sh 'python3 test_app.py'
            }
        }
        stage('Start OWASP ZAP') {
            steps {
                echo 'Starting OWASP ZAP on the Kali Linux machine...'
                // Use sshpass to start ZAP on the remote Kali machine
                sh """
                sshpass -p '${SSH_PASSWORD}' ssh -o StrictHostKeyChecking=no colmoschin@${ZAP_HOST} "zaproxy -daemon -host 0.0.0.0 -port 8080 -config 'api.addrs.addr.name=.*' -config 'api.addrs.addr.regex=true'"
                """
                sleep 15 // Give some time for ZAP to fully start
            }
        }
        stage('Run ZAP Spider Scan') {
            steps {
                echo 'Running OWASP ZAP Spider scan...'
                script {
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/spider/action/scan/" \
                         -H "Content-Type: application/x-www-form-urlencoded" \
                         -d "url=${LOCAL_APP_URL}&recurse=true&apikey=${API_KEY}"
                    """
                }
                sleep 10
            }
        }
        stage('Run ZAP Active Scan') {
            steps {
                echo 'Running OWASP ZAP Active scan...'
                script {
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/ascan/action/scan/" \
                         -H "Content-Type: application/x-www-form-urlencoded" \
                         -d "url=${LOCAL_APP_URL}&apikey=${API_KEY}"
                    """
                }
                sleep 10
            }
        }
        stage('Save ZAP Report') {
            steps {
                echo 'Saving OWASP ZAP report...'
                sh """
                curl -X GET "http://${ZAP_HOST}:8080/OTHER/core/other/xmlreport/?apikey=${API_KEY}" \
                     -H "Content-Type: application/x-www-form-urlencoded" \
                     -o zap_report.xml
                """
            }
        }
        stage('Publish ZAP Report') {
            steps {
                echo 'Publishing OWASP ZAP report...'
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
