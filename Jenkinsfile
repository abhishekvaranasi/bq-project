pipeline {
        agent none
        stages {
		stage("Environment variables") {
			agent { label "master" }
			steps {
				bat "set GOOGLE_APPLICATION_CREDENTIALS=./validation-193604-3a770385fc34.json"
				bat "set PROJECT_ID=validation-193604"
				bat "set BUCKET_ID=validation-backup"
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
