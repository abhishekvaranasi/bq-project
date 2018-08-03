pipeline {
        agent none
        stages {
		stage("Environment variables") {
			agent { label "master" }
			steps {
				bat "env.sh"
				bat "echo %PROJECT_ID%"
				bat "echo %BUCKET_ID%"
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
