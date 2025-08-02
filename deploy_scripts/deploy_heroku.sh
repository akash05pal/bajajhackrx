#!/bin/bash

# HackRx 6.0 Heroku Deployment Script

echo "🚀 Starting Heroku deployment for HackRx 6.0"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    echo "Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for HackRx 6.0"
fi

# Create Heroku app
echo "🏗️ Creating Heroku app..."
APP_NAME="hackrx-6-0-$(date +%s)"
heroku create $APP_NAME

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set OPENAI_API_KEY=$OPENAI_API_KEY
heroku config:set PINECONE_API_KEY=$PINECONE_API_KEY
heroku config:set PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT

# Deploy to Heroku
echo "📤 Deploying to Heroku..."
git push heroku main

# Open the app
echo "🌐 Opening the deployed app..."
heroku open

echo "✅ Deployment complete!"
echo "📊 App URL: https://$APP_NAME.herokuapp.com"
echo "📚 API Documentation: https://$APP_NAME.herokuapp.com/docs" 