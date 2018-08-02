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
        }
}
