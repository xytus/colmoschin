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
                // Start the Flask application in the background
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
                // Optionally, use SSH to start OWASP ZAP on the Kali Linux machine
                sshagent (credentials: colmoschin) {
                    sh '''
                    ssh colmoschin@${ZAP_HOST} "zaproxy -daemon -host 0.0.0.0 -port 8080 -config 'api.addrs.addr.name=.*' -config 'api.addrs.addr.regex=true'"
                    '''
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
                // Stop OWASP ZAP on the Kali Linux machine using SSH (optional)
                sshagent (credentials: ['kali-ssh-credentials']) {
                    sh '''
                    ssh colmoschin@${ZAP_HOST} "zap.sh -shutdown"
                    '''
                }
            }
        }
    }
}
