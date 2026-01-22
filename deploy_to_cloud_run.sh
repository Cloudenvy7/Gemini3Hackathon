#!/bin/bash

# Configuration
SERVICE_NAME="gemini3-seattle-permits"
REGION="us-west1"
PROJECT_ID="gen-lang-client-0637434086"

# Load environment variables from .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "🚀 Deploying $SERVICE_NAME to Google Cloud Run..."

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --project $PROJECT_ID \
  --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY,BOOTSTRAP_SERVERS=$BOOTSTRAP_SERVERS,SASL_USERNAME=$SASL_USERNAME,SASL_PASSWORD=$SASL_PASSWORD" \
  --allow-unauthenticated \
  --port 8080

echo "✅ Deployment requested."
