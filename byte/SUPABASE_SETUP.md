# Supabase Storage Setup

## Required Storage Buckets

Your Supabase project needs the following storage buckets:

### 1. `audio-files` bucket
- **Purpose**: Store generated TTS audio files
- **Public Access**: Yes (for serving audio to frontend)
- **File Types**: `.mp3`

### 2. `video-files` bucket  
- **Purpose**: Store generated Manim videos
- **Public Access**: Yes (for serving videos to frontend)
- **File Types**: `.mp4`

## How to Create Buckets

1. Go to your Supabase Dashboard
2. Navigate to **Storage** → **Buckets**
3. Click **New Bucket**
4. Create each bucket with these settings:

### Audio Files Bucket:
```
Name: audio-files
Public: ✅ Yes
File size limit: 50MB
Allowed MIME types: audio/mpeg, audio/mp3
```

### Video Files Bucket:
```
Name: video-files  
Public: ✅ Yes
File size limit: 500MB
Allowed MIME types: video/mp4
```

## Bucket Policies

The buckets need proper RLS (Row Level Security) policies:

### For `audio-files`:
```sql
-- Allow public read access
CREATE POLICY "Public read access for audio files" ON storage.objects
FOR SELECT USING (bucket_id = 'audio-files');

-- Allow authenticated users to upload
CREATE POLICY "Authenticated users can upload audio files" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'audio-files' AND auth.role() = 'authenticated');
```

### For `video-files`:
```sql
-- Allow public read access  
CREATE POLICY "Public read access for video files" ON storage.objects
FOR SELECT USING (bucket_id = 'video-files');

-- Allow authenticated users to upload
CREATE POLICY "Authenticated users can upload video files" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'video-files' AND auth.role() = 'authenticated');
```

## Database Tables

Make sure you have these tables in your Supabase database:

### `audios` table:
```sql
CREATE TABLE audios (
    id SERIAL PRIMARY KEY,
    script_id TEXT NOT NULL,
    audio_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### `videos` table:
```sql
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    script_id TEXT NOT NULL,
    video_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Environment Variables

Ensure your `.env.local` has:
```
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

The service role key is needed for server-side file uploads.
