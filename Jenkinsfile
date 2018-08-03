pipeline {
        agent none
        stages {
		stage("Environment variables") {
			agent { label "master" }
			environment {
			GOOGLE_APPLICATION_CREDENTIALS=./validation-193604-3a770385fc34.json
			PROJECT_ID=validation-193604
			BUCKET_ID=validation-backup
			}
			steps {
				bat "echo %PROJECT_ID%"
				bat "echo %BUCKET_ID%"
				bat "echo %HOSTNAME%"
			}
		}
		stage("Executing scripts"){
			agent { label "master" }
			steps {
				bat "python app.py table create --bulk"
			}
		}

        }
}
