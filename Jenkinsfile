pipeline {
    agent any
    environment {
        ZAP_HOST = '192.168.1.5'           // IP address of the Kali Linux VM where OWASP ZAP is running
        LOCAL_APP_URL = 'http://192.168.1.6:5000' // URL of the Flask application running on the Jenkins (Ubuntu) server
        SSH_PASSWORD = 'colmoschin' // Replace with the SSH password for the Kali Linux VM
        SSH_USER = 'colmoschin'             // Replace with the SSH username for the Kali Linux VM
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
                // Start the Flask application in the background
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
        stage('Start OWASP ZAP') {
            steps {
                echo 'Starting OWASP ZAP on the Kali Linux machine using sshpass...'
                sh """
                sshpass -p '${SSH_PASSWORD}' ssh -o StrictHostKeyChecking=no ${SSH_USER}@${ZAP_HOST} "nohup zaproxy -daemon -host 0.0.0.0 -port 8080 -config 'api.addrs.addr.name=.*' -config 'api.addrs.addr.regex=true' &"
                """
                // Add a sleep to allow ZAP to fully initialize
                sleep 20
            }
        }
        stage('Verify ZAP Startup') {
            steps {
                script {
                    def zapReady = sh(script: """
                        sshpass -p '${SSH_PASSWORD}' ssh -o StrictHostKeyChecking=no ${SSH_USER}@${ZAP_HOST} "curl -s http://0.0.0.0:8080/JSON/core/view/version/ | grep -q 'ZAP' "
                    """, returnStatus: true) == 0

                    if (!zapReady) {
                        error "ZAP failed to start or is not responding on port 8080."
                    } else {
                        echo "ZAP is running and ready to accept commands."
                    }
                }
            }
        }
        stage('Run ZAP Spider Scan') {
            steps {
                echo 'Running OWASP ZAP Spider scan...'
                script {
                    // Run ZAP Spider scan on the locally hosted application on the Jenkins server
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/spider/action/scan/?url=${LOCAL_APP_URL}&recurse=true"
                    """
                }
                sleep 30 // Adjust the sleep time based on the size of the target application
            }
        }
        stage('Run ZAP Active Scan') {
            steps {
                echo 'Running OWASP ZAP Active scan...'
                script {
                    // Run ZAP Active scan on the application
                    sh """
                    curl -X POST "http://${ZAP_HOST}:8080/JSON/ascan/action/scan/?url=${LOCAL_APP_URL}"
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
                curl "http://${ZAP_HOST}:8080/OTHER/core/other/xmlreport/" -o zap_report.xml
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
        stage('Stop OWASP ZAP') {
            steps {
                echo 'Stopping OWASP ZAP on the Kali Linux machine...'
                sh """
                sshpass -p '${SSH_PASSWORD}' ssh -o StrictHostKeyChecking=no ${SSH_USER}@${ZAP_HOST} "pkill -f zaproxy"
                """
            }
        }
    }
}
