#!/bin/bash

# Build and deploy to Render.com or similar platform

echo "Building Docker image..."
docker build -t ecfr-analyzer .

echo "Deploying to cloud..."
# This would be customized for your deployment platform
# For Render.com, you would connect your GitHub repo
# For AWS: docker push to ECR and deploy to ECS
# For Heroku: heroku container:push web

echo "Deployment completed!"