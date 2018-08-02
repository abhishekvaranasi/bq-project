#!/bin/sh

gcloud auth activate-service-account --key-file ./validation-193604-3a770385fc34.json
set GOOGLE_APPLICATION_CREDENTIALS=./validation-193604-3a770385fc34.json
set PROJECT_ID=validation-193604
set BUCKET_ID=validation-backup
