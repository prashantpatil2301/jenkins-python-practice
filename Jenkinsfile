pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'TEST_SELECTION',
            choices: ['all', 'title', 'email'],
            description: 'Choose which Selenium tests to run'
        )
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
                    case "${TEST_SELECTION:-all}" in
                        all)
                            TEST_TARGET="test_selenium_lab.py"
                            ;;
                        title)
                            TEST_TARGET="test_selenium_lab.py::test_page_title"
                            ;;
                        email)
                            TEST_TARGET="test_selenium_lab.py::test_login_email_present"
                            ;;
                        *)
                            echo "Invalid test selection"
                            exit 1
                            ;;
                    esac

                    docker run --rm --shm-size=1g \
                      -v "$PWD/reports:/app/reports" \
                      jenkins-python-practice \
                      python -m pytest -v "$TEST_TARGET" \
                      --junitxml=reports/results.xml
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