#!/bin/bash

# Manim Video Generator Setup Script
# This script sets up the Python environment for video generation

echo "🎬 Setting up Manim Video Generator..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Check if we're in the right directory
if [ ! -f "manim_renderer/requirements.txt" ]; then
    echo "❌ Please run this script from the root of your project (where manim_renderer/ exists)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "manim_renderer/venv" ]; then
    echo "🔧 Creating virtual environment..."
    python -m venv manim_renderer/venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source manim_renderer/venv/bin/activate || source manim_renderer/venv/Scripts/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing Python dependencies..."
pip install -r manim_renderer/requirements.txt

# Install FFmpeg (platform-specific instructions)
echo "🎥 Checking FFmpeg installation..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg not found. Please install FFmpeg:"
    echo "   - On Windows: Download from https://ffmpeg.org/download.html"
    echo "   - On macOS: brew install ffmpeg"
    echo "   - On Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   - On CentOS/RHEL: sudo yum install ffmpeg"
else
    echo "✅ FFmpeg found: $(ffmpeg -version | head -n 1)"
fi

# Test Manim installation
echo "🧪 Testing Manim installation..."
python -c "import manim; print('✅ Manim installed successfully:', manim.__version__)"

echo ""
echo "🎉 Setup complete! Your Manim video generator is ready."
echo ""
echo "📋 Next steps:"
echo "   1. Make sure FFmpeg is installed and available in PATH"
echo "   2. Your Node.js app can now call the Python script to generate videos"
echo "   3. Videos will be generated in temporary directories and uploaded to Supabase"
echo ""
echo "🔧 To manually test the generator:"
echo "   cd manim_renderer"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   python manim_generator.py --json test_script.json --output test_video.mp4"
echo ""
