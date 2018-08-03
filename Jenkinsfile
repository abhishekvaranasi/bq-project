pipeline {
        agent none
        stages {
		stage("Environment variables") {
			agent { label "master" }
			steps {
				bat "echo %PROJECT_ID%"
				bat "echo %BUCKET_ID%"
				bat "echo %GOOGLE_APPLICATION_CREDENTIALS%"
			}
		}
		stage("Execution") {
		    agent { label "master" }
		    steps {
		        echo "Executing python script..."
		        bat "python app.py dataset create --bulk"
		        echo "execution complete!"
		    }
		}
    }
}
