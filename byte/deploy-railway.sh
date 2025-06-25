#!/bin/bash

# Railway Deployment Script
# Run this script to prepare and deploy your app to Railway

echo "🚀 Preparing Byte-Learn for Railway deployment..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway:"
    railway login
fi

# Ensure all changes are committed
echo "Checking git status..."
if [[ `git status --porcelain` ]]; then
    echo "⚠️  You have uncommitted changes. Please commit them first:"
    git status
    exit 1
fi

# Link project if not already linked
if ! railway status &> /dev/null; then
    echo "Linking Railway project..."
    railway link
fi

# Set environment variables (you'll need to do this manually in Railway dashboard)
echo "📋 Don't forget to set these environment variables in Railway dashboard:"
echo "   - GEMINI_API_KEY"
echo "   - SUPABASE_URL"
echo "   - SUPABASE_ANON_KEY"
echo "   - SUPABASE_SERVICE_ROLE_KEY"
echo "   - GOOGLE_APPLICATION_CREDENTIALS=/app/gcloud-credentials.json"
echo ""

# Deploy
echo "🎯 Deploying to Railway..."
railway up

echo "✅ Deployment initiated! Check your Railway dashboard for progress."
echo "📱 Your app will be available at: https://your-project.railway.app"
