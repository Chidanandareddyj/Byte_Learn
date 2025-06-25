# Railway Deployment Guide for Byte-Learn

## 🚀 Quick Setup

### 1. Prepare Your Repository
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 3. Deploy to Railway
```bash
# Login to Railway
railway login

# Link your project (in your project directory)
railway link

# Deploy your application
railway up
```

### 4. Set Environment Variables in Railway Dashboard
Go to your Railway project dashboard and add these variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
GOOGLE_APPLICATION_CREDENTIALS=/app/gcloud-credentials.json
NODE_ENV=production
```

### 5. Configure Domain (Optional)
Railway provides a free `.railway.app` domain, or you can add your custom domain.

## 🔧 Configuration Files

Your project already has the necessary files:
- ✅ `Dockerfile` - Handles Python + Node.js setup
- ✅ `package.json` - Node.js dependencies
- ✅ `manim_renderer/requirements.txt` - Python dependencies
- ✅ Environment variable handling in code

## 📦 Deployment Process

1. **Build Phase**: Railway will use your Dockerfile to:
   - Install Python, FFmpeg, LaTeX
   - Install Manim and dependencies
   - Install Node.js dependencies
   - Build Next.js application

2. **Runtime**: Your app will have access to:
   - Python runtime for Manim video generation
   - FFmpeg for audio/video processing
   - LaTeX for mathematical rendering
   - File system for temporary video files

## 🎯 Expected Deployment URL
Your app will be available at: `https://your-project-name.railway.app`

## 💡 Tips for Success

1. **File Size**: Ensure your `gcloud-credentials.json` file is present
2. **Build Time**: First deployment may take 5-10 minutes due to dependencies
3. **Memory**: Railway provides sufficient resources for video generation
4. **Storage**: Temporary files are cleaned up automatically
5. **Scaling**: Railway handles traffic spikes well

## 🔍 Troubleshooting

### If deployment fails:
1. Check Railway logs: `railway logs`
2. Verify all environment variables are set
3. Ensure Docker build completes successfully locally
4. Check that all required files are in your repository

### Common Issues:
- **Python dependencies**: Make sure `requirements.txt` is correct
- **LaTeX rendering**: Verify TeX packages are installed in Dockerfile
- **File permissions**: Check that generated files can be written/read
- **API limits**: Monitor Gemini API and Google Cloud TTS usage

## 🎉 Post-Deployment

After successful deployment:
1. Test video generation functionality
2. Verify audio synthesis works
3. Check database connections
4. Monitor performance and logs
5. Set up monitoring/alerts if needed

---

Railway is perfect for your project because it handles the complex dependency stack (Python + Node.js + FFmpeg + LaTeX) seamlessly while providing a generous free tier.
