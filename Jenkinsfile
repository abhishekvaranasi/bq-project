pipeline {
	agent none
	stages {

		stage("Environment setup") {
			agent { label "master" }
			steps {
			  bat "env.sh"
        echo $PROJECT_ID
        echo $BUCKET_ID
			}
		}
		}
}
