@echo off
REM Manim Video Generator Setup Script for Windows
REM This script sets up the Python environment for video generation

echo 🎬 Setting up Manim Video Generator...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if we're in the right directory
if not exist "manim_renderer\requirements.txt" (
    echo ❌ Please run this script from the root of your project where manim_renderer\ exists
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "manim_renderer\venv" (
    echo 🔧 Creating virtual environment...
    python -m venv manim_renderer\venv
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call manim_renderer\venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
pip install --upgrade pip

REM Install requirements
echo 📦 Installing Python dependencies...
pip install -r manim_renderer\requirements.txt

REM Check FFmpeg installation
echo 🎥 Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ FFmpeg not found. Please install FFmpeg:
    echo    - Download from https://ffmpeg.org/download.html
    echo    - Add to your system PATH
    echo    - Or use chocolatey: choco install ffmpeg
) else (
    echo ✅ FFmpeg found and working
)

REM Test Manim installation
echo 🧪 Testing Manim installation...
python -c "import manim; print('✅ Manim installed successfully:', manim.__version__)"

echo.
echo 🎉 Setup complete! Your Manim video generator is ready.
echo.
echo 📋 Next steps:
echo    1. Make sure FFmpeg is installed and available in PATH
echo    2. Your Node.js app can now call the Python script to generate videos
echo    3. Videos will be generated in temporary directories and uploaded to Supabase
echo.
echo 🔧 To manually test the generator:
echo    cd manim_renderer
echo    venv\Scripts\activate.bat
echo    python manim_generator.py --json test_script.json --output test_video.mp4
echo.

pause
