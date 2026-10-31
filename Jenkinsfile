pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
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

        stage('Generate Reports') {
            steps {
                sh '''
                    mkdir -p reports
                    docker run --rm \
                      -v "$PWD/reports:/app/reports" \
                      jenkins-python-practice
                '''
            }
        }

        stage('Save Reports') {
            steps {
                archiveArtifacts artifacts: 'reports/output.txt,reports/output.pdf',
                                 fingerprint: true
            }
        }
    }
}