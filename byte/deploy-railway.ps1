# Railway Deployment Script for Windows
# Run this script to prepare and deploy your app to Railway

Write-Host "🚀 Preparing Byte-Learn for Railway deployment..." -ForegroundColor Green

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (!$railwayInstalled) {
    Write-Host "Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Check if user is logged in
$loginStatus = railway whoami 2>$null
if (!$loginStatus) {
    Write-Host "Please login to Railway:" -ForegroundColor Yellow
    railway login
}

# Check git status
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "⚠️  You have uncommitted changes. Please commit them first:" -ForegroundColor Red
    git status
    exit 1
}

# Link project if not already linked
$projectStatus = railway status 2>$null
if (!$projectStatus) {
    Write-Host "Linking Railway project..." -ForegroundColor Yellow
    railway link
}

# Environment variables reminder
Write-Host "📋 Don't forget to set these environment variables in Railway dashboard:" -ForegroundColor Cyan
Write-Host "   - GEMINI_API_KEY" -ForegroundColor White
Write-Host "   - SUPABASE_URL" -ForegroundColor White
Write-Host "   - SUPABASE_ANON_KEY" -ForegroundColor White
Write-Host "   - SUPABASE_SERVICE_ROLE_KEY" -ForegroundColor White
Write-Host "   - GOOGLE_APPLICATION_CREDENTIALS=/app/gcloud-credentials.json" -ForegroundColor White
Write-Host ""

# Deploy
Write-Host "🎯 Deploying to Railway..." -ForegroundColor Green
railway up

Write-Host "✅ Deployment initiated! Check your Railway dashboard for progress." -ForegroundColor Green
Write-Host "📱 Your app will be available at: https://your-project.railway.app" -ForegroundColor Cyan
