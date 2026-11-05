pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    stages {
        stage('Prepare Environment') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt

                    mkdir -p reports
                    rm -f reports/output.txt reports/output.pdf reports/results.xml
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '.venv/bin/python -m pytest -v --junitxml=reports/results.xml'
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