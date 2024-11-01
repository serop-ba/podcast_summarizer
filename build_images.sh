#!/bin/bash

# Set project ID
PROJECT_ID="secure-project-tutorial"



# Docker images and paths
cd ./frontend
IMAGE_NAME="europe-west1-docker.pkg.dev/$PROJECT_ID/dasc-docker/frontend:latest"
gcloud builds submit --tag "$IMAGE_NAME" 

echo "pushed $IMAGE_NAME To image registry" 

cd ../external_service
IMAGE_NAME="europe-west1-docker.pkg.dev/$PROJECT_ID/dasc-docker/ollama:latest"
gcloud builds submit --tag "$IMAGE_NAME" 
echo "pushed $IMAGE_NAME To image registry" 

cd ../api/
IMAGE_NAME="europe-west1-docker.pkg.dev/$PROJECT_ID/dasc-docker/backend:latest"
gcloud builds submit --tag "$IMAGE_NAME" 
echo "pushed $IMAGE_NAME To image registry" 


echo "All images have been successfully built and pushed to GCR."
