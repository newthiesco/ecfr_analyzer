#!/bin/bash

# Build and deploy to Render.com or similar platform

#echo "Building Docker image..."
#docker build -t ecfr-analyzer .

#echo "Deploying to cloud..."
# This would be customized for your deployment platform
# For Render.com, you would connect your GitHub repo
# For AWS: docker push to ECR and deploy to ECS
# For Heroku: heroku container:push web

#echo "Deployment completed!"






# build.sh for Render.com deployment
# Exit on any error
set -o errexit

echo "========================================="
echo "Starting build process on Render.com"
echo "========================================="

# Print Python version
echo "Python version:"
python --version

# Print pip version
echo "Pip version:"
pip --version

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Optional: List installed packages for debugging
echo "Installed packages:"
pip list

echo "========================================="
echo "Build completed successfully!"
echo "========================================="