import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'
import fs from 'fs'
import { promisify } from 'util'
import os from 'os'
import { getScriptByPromptId, getAudioByScriptId, saveVideo, getVideoByPromptId } from '@/lib/databse'
import { supabaseAdmin } from '@/lib/supabaseClient'

const writeFile = promisify(fs.writeFile)
const readFile = promisify(fs.readFile)
const unlink = promisify(fs.unlink)

export async function POST(request: NextRequest) {
  const tempFiles: string[] = []
  
  try {
    // Check if supabaseAdmin is available (server-side only)
    if (!supabaseAdmin) {
      console.error("Supabase admin client not available. Check environment variables.");
      return NextResponse.json({ error: "Server configuration error" }, { status: 500 })
    }

    const { promptId } = await request.json()
    
    if (!promptId) {
      return NextResponse.json({ error: "Prompt ID is required" }, { status: 400 })
    }

    console.log(`🎬 Starting video generation for prompt: ${promptId}`)

    // Check if video already exists
    const existingVideo = await getVideoByPromptId(promptId)
    if (existingVideo) {
      console.log(`📼 Video already exists for prompt ${promptId}`)
      return NextResponse.json({
        message: "Video already exists",
        videoUrl: existingVideo.video_url,
        videoId: existingVideo.id,
        cached: true
      })
    }

    // 1. Get the script data
    const script = await getScriptByPromptId(promptId)
    if (!script) {
      return NextResponse.json({ error: "Script not found for the given prompt ID" }, { status: 404 })
    }

    // 2. Get the audio file
    const audio = await getAudioByScriptId(script.id.toString())
    if (!audio) {
      return NextResponse.json({ error: "Audio not found for the script" }, { status: 404 })
    }

    // 3. Parse script data
    let scriptData: Record<string, unknown>
    try {
      scriptData = JSON.parse(script.script_text)
      console.log(`📝 Parsed script data:`, scriptData)
    } catch (error) {
      console.error('Script parsing error:', error)
      return NextResponse.json({ error: "Invalid script format" }, { status: 400 })
    }

    // 4. Download audio file from Supabase
    const audioUrl = audio.audio_url
    const audioResponse = await fetch(audioUrl)
    if (!audioResponse.ok) {
      return NextResponse.json({ error: "Failed to download audio file" }, { status: 500 })
    }
    
    const audioBuffer = await audioResponse.arrayBuffer()
    const tempDir = os.tmpdir()
    const audioPath = path.join(tempDir, `audio-${promptId}.mp3`)
    await writeFile(audioPath, Buffer.from(audioBuffer))
    tempFiles.push(audioPath)

    // 5. Create temporary JSON file for script
    const jsonPath = path.join(tempDir, `script-${promptId}.json`)
    await writeFile(jsonPath, JSON.stringify(scriptData, null, 2))
    tempFiles.push(jsonPath)

    // 6. Generate video using Python script
    const outputVideoPath = path.join(tempDir, `video-${promptId}.mp4`)
    const pythonScriptPath = path.join(process.cwd(), 'manim_renderer', 'manim_generator.py')
    
    console.log(`🐍 Running Python script: ${pythonScriptPath}`)
    console.log(`📁 JSON path: ${jsonPath}`)
    console.log(`🎵 Audio path: ${audioPath}`)
    console.log(`🎬 Output path: ${outputVideoPath}`)

    const success = await runPythonVideoGenerator(pythonScriptPath, jsonPath, outputVideoPath, audioPath)
    
    if (!success) {
      console.error("Python video generation failed")
      return NextResponse.json({ error: "Failed to generate video with Python script" }, { status: 500 })
    }

    console.log("Python script completed successfully")

    // 7. Check if video was generated
    if (!fs.existsSync(outputVideoPath)) {
      console.error("Video file was not created at:", outputVideoPath)
      return NextResponse.json({ error: "Video file was not created" }, { status: 500 })
    }

    console.log("Video file exists, proceeding with upload")

    // 8. Upload video to Supabase Storage
    const videoBuffer = await readFile(outputVideoPath)
    const videoFileName = `video_${promptId}_${Date.now()}.mp4`
    
    console.log(`📤 Uploading video to Supabase: ${videoFileName}`)
    console.log(`📊 Video size: ${videoBuffer.length} bytes`)
    
    const { data: uploadData, error: uploadError } = await supabaseAdmin.storage
      .from('video-files')
      .upload(videoFileName, videoBuffer, {
        contentType: 'video/mp4',
        upsert: true,
      })

    if (uploadError) {
      console.error('Supabase video upload error:', uploadError)
      return NextResponse.json({ error: "Failed to upload video file", details: uploadError.message }, { status: 500 })
    }

    console.log('Video uploaded successfully:', uploadData)

    // 9. Save video record to database
    const videoUrl = `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/video-files/${videoFileName}`
    console.log(`💾 Saving video record with URL: ${videoUrl}`)
    console.log(`🔗 Linking video to audio ID: ${audio.id}`)
    
    const videoRecord = await saveVideo(audio.id.toString(), videoUrl)
    console.log('Video record saved:', videoRecord)

    console.log(`✅ Video generated successfully: ${videoUrl}`)

    return NextResponse.json({
      message: "Video generated successfully",
      videoUrl: videoUrl,
      videoId: videoRecord.id,
    })

  } catch (error) {
    console.error('Error generating video:', error)
    return NextResponse.json({ 
      error: "Failed to generate video",
      details: error instanceof Error ? error.message : "Unknown error"
    }, { status: 500 })
  } finally {
    // Cleanup temporary files
    for (const tempFile of tempFiles) {
      try {
        if (fs.existsSync(tempFile)) {
          await unlink(tempFile)
        }
      } catch (cleanupError) {
        console.warn(`Failed to delete temporary file: ${tempFile}`, cleanupError)
      }
    }
  }
}

async function runPythonVideoGenerator(
  scriptPath: string, 
  jsonPath: string, 
  outputPath: string, 
  audioPath: string
): Promise<boolean> {
  return new Promise((resolve) => {
    const args = [
      scriptPath,
      '--json', jsonPath,
      '--output', outputPath,
      '--audio', audioPath
    ]
    
    console.log(`🐍 Executing: python ${args.join(' ')}`)
    
    const pythonProcess = spawn('python', args, {
      stdio: ['pipe', 'pipe', 'pipe'],
      cwd: process.cwd()
    })
    
    let stdout = ''
    let stderr = ''
    
    pythonProcess.stdout.on('data', (data) => {
      const output = data.toString()
      stdout += output
      console.log(`🐍 Python stdout: ${output}`)
    })
    
    pythonProcess.stderr.on('data', (data) => {
      const error = data.toString()
      stderr += error
      console.error(`🐍 Python stderr: ${error}`)
    })
    
    pythonProcess.on('close', (code) => {
      console.log(`🐍 Python process exited with code: ${code}`)
      
      if (code === 0) {
        console.log('✅ Video generation completed successfully')
        resolve(true)
      } else {
        console.error('❌ Video generation failed')
        console.error('Full stderr:', stderr)
        console.log('Full stdout:', stdout)
        resolve(false)
      }
    })
    
    pythonProcess.on('error', (error) => {
      console.error('🐍 Python process error:', error)
      resolve(false)
    })
  })
}
