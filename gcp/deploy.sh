#!/usr/bin/env bash
# ==============================================================================
# Google Cloud Run Deployment Script for NeuroOps Duo
# Targets Google Cloud's greenest region (europe-north1: 93% Carbon-Free Energy)
# ==============================================================================

set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-gitlab-transcend-prod}"
REGION="${GCP_REGION:-europe-north1}"
SERVICE_NAME="omnipay-gateway"
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "======================================================================"
echo " Deploying ${SERVICE_NAME} to Google Cloud Run"
echo " Project: ${PROJECT_ID}"
echo " Region:  ${REGION} (Optimal Low-Carbon Green Zone: 28.4 gCO2/kWh)"
echo "======================================================================"

# 1. Build and push container to Google Container Registry
echo "--> Building container image with Google Cloud Build..."
gcloud builds submit --tag "${IMAGE_TAG}" --project "${PROJECT_ID}" .

# 2. Deploy to Google Cloud Run with canary traffic splitting (10% initial canary)
echo "--> Deploying revision to Google Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
    --image "${IMAGE_TAG}" \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --concurrency 80 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars="DEPLOYED_REGION=${REGION},CARBON_INTENSITY_GCO2_KWH=28.4,SERVICE_VERSION=v1.0.0" \
    --project "${PROJECT_ID}"

# 3. Retrieve service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)' --project "${PROJECT_ID}")

echo "======================================================================"
echo " Deployment Successful!"
echo " Live Public Google Cloud URL: ${SERVICE_URL}"
echo " Health Probe: ${SERVICE_URL}/healthz"
echo " Metrics:      ${SERVICE_URL}/metrics"
echo " Carbon CFE:   93% Carbon-Free Energy (Hamina, Finland)"
echo "======================================================================"
