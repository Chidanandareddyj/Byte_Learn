# 🎬 Byte-Learn Video Generation System

A complete pipeline for generating educational math videos using AI script generation, Text-to-Speech, and Manim animations.

## 🏗️ Architecture Overview

```
User Prompt → AI Script → Audio Generation → Video Rendering → Final Video
     ↓           ↓             ↓                ↓              ↓
  Database    Gemini AI    Google TTS       Manim Python    Supabase Storage
```

## 📋 Complete Pipeline

### 1. **User Input** (`/my-videos`)
- User enters a math topic prompt
- Prompt stored in Supabase `prompts` table

### 2. **Script Generation** (`/api/generated-script`)
- Gemini AI converts prompt to structured JSON
- JSON includes: title, steps (text + math), narration
- Script stored in `scripts` table

### 3. **Audio Generation** (`/api/generate-audio`)
- Google Cloud TTS converts narration to speech
- Audio chunking for long scripts
- MP3 uploaded to Supabase Storage (`audio-files` bucket)
- Audio record saved in `audios` table

### 4. **Video Generation** (`/api/generate-video`) ⭐ **NEW**
- Python Manim script converts JSON to animated video
- Combines math animations with synchronized audio
- MP4 uploaded to Supabase Storage (`video-files` bucket)
- Video record saved in `videos` table

### 5. **User Interface**
- `/generated-script` - Shows script + audio preview
- `/generate-video` - Video generation progress + preview
- Download and sharing capabilities

## 🚀 Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.8+
- FFmpeg
- Supabase project with storage buckets

### 1. Install Node.js Dependencies
```bash
npm install
```

### 2. Setup Python Environment
```bash
# On Windows
cd manim_renderer
setup.bat

# On macOS/Linux  
cd manim_renderer
chmod +x setup.sh
./setup.sh
```

### 3. Install FFmpeg
- **Windows**: Download from https://ffmpeg.org/download.html
- **macOS**: `brew install ffmpeg`
- **Ubuntu**: `sudo apt install ffmpeg`

### 4. Configure Supabase
See `SUPABASE_SETUP.md` for detailed instructions on:
- Creating storage buckets (`audio-files`, `video-files`)
- Setting up database tables
- Configuring bucket policies

### 5. Environment Variables
Create `.env.local`:
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Google Cloud (for TTS)
GOOGLE_APPLICATION_CREDENTIALS=./gcloud-credentials.json

# Gemini AI  
GEMINI_API_KEY=your-gemini-api-key
```

## 🧪 Testing the System

### Test Python Video Generator
```bash
cd manim_renderer
source venv/bin/activate  # venv\Scripts\activate on Windows
python manim_generator.py --json test_script.json --output test.mp4
```

### Test Complete Pipeline
1. Go to `/my-videos`
2. Enter: "Explain the quadratic formula with examples"
3. Wait for script + audio generation
4. Click "Generate Video"
5. Download your video!

## 📁 Project Structure

```
byte/
├── app/
│   ├── api/
│   │   ├── generate-audio/     # TTS generation
│   │   ├── generate-video/     # NEW: Video generation
│   │   └── generated-script/   # AI script generation
│   ├── generate-video/         # NEW: Video generation UI
│   ├── generated-script/       # Script + audio UI
│   └── my-videos/             # User input
├── manim_renderer/            # NEW: Python video generation
│   ├── manim_generator.py     # Main video generator
│   ├── requirements.txt       # Python dependencies
│   ├── setup.bat             # Windows setup
│   ├── setup.sh              # Unix setup
│   └── test_script.json      # Test data
├── lib/
│   ├── gemini.ts             # AI script generation
│   ├── databse.ts            # Database operations
│   └── supabaseClient.ts     # Supabase config
└── components/               # UI components
```

## 🔧 How It Works

### JSON Script Format
```json
{
  "title": "QuadraticFormula",
  "steps": [
    {
      "text": "Let's explore the quadratic formula",
      "math": "ax^2 + bx + c = 0"
    }
  ],  
  "narration": "Full narration script for TTS..."
}
```

### Manim Animation Pipeline
1. **Parse JSON** - Extract title, steps, math expressions
2. **Create Scene** - Generate Python Manim scene code
3. **Render Video** - Use Manim to create MP4 animation
4. **Sync Audio** - Combine video with TTS audio using FFmpeg
5. **Upload** - Save final video to Supabase Storage

### Video Generation Process
- **Quality**: 1080p, 30fps
- **Duration**: Matches audio length (typically 2-5 minutes)
- **Format**: MP4 with H.264 encoding
- **Audio**: Synchronized AAC audio track

## 🎯 Features

### ✅ Current Features
- ✅ AI-powered script generation (Gemini)
- ✅ Text-to-Speech audio generation (Google Cloud)
- ✅ Mathematical animation rendering (Manim)
- ✅ Audio-video synchronization (FFmpeg)
- ✅ Cloud storage and streaming (Supabase)
- ✅ Progress tracking and error handling
- ✅ Download and sharing capabilities

### 🚧 Future Enhancements
- [ ] Multiple animation styles
- [ ] Custom voice selection
- [ ] Batch video processing
- [ ] Advanced math rendering
- [ ] Interactive elements
- [ ] Multiple output formats

## 🐛 Troubleshooting

### Common Issues

**Python/Manim Installation**
```bash
# Reinstall Manim
pip uninstall manim
pip install manim==0.18.1
```

**FFmpeg Not Found**
```bash
# Verify FFmpeg installation
ffmpeg -version
# Add to PATH if needed
```

**Supabase Upload Errors**
- Check bucket permissions in Supabase dashboard
- Verify service role key in environment variables
- Ensure buckets are public for read access

**Video Generation Timeout**
- Videos typically take 2-5 minutes to generate
- Check Python process logs in terminal
- Verify all dependencies are installed

## 📊 Performance

- **Script Generation**: ~5-10 seconds
- **Audio Generation**: ~10-30 seconds  
- **Video Generation**: ~2-5 minutes
- **Total Pipeline**: ~3-6 minutes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

**🎉 Congratulations! Your complete AI-powered video generation pipeline is ready!**
