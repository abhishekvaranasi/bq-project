pipeline {
        agent none
        stages {
		stage("Environment variables") {
			agent { label "master" }
			steps {
				bat "env.sh"
				sh "echo ${PROJECT_ID}"
				sh "echo ${BUCKET_ID}"
				sh "echo ${HOSTNAME}"
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
