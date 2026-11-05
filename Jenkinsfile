pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Prepare Reports') {
            steps {
                sh '''
                    mkdir -p reports
                    rm -f reports/output.txt reports/output.pdf reports/results.xml
                '''
            }
        }

        stage('Check Docker') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t jenkins-python-practice .'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                    docker run --rm --shm-size=1g \
                      -v "$PWD/reports:/app/reports" \
                      jenkins-python-practice
                '''
            }
        }
    }

    post {
        always {
            script {
                try {
                    junit 'reports/results.xml'
                } finally {
                    archiveArtifacts(
                        artifacts: 'reports/output.txt,reports/output.pdf,reports/results.xml',
                        allowEmptyArchive: true,
                        fingerprint: true
                    )
                }
            }
        }
    }
}