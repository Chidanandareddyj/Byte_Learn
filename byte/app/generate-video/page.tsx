'use client'

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Navbar } from '@/components/Navbar'
import Silk from '@/components/ui/Silk'

export default function GenerateVideoPage() {
  const searchParams = useSearchParams()
  const promptId = searchParams.get('id')
  const router = useRouter()
  
  const [status, setStatus] = useState('🎬 Initializing video generation...')
  const [videoUrl, setVideoUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (!promptId) {
      setError('No prompt ID provided')
      setLoading(false)
      return
    }

    const generateVideo = async () => {
      try {
        setStatus('🎬 Starting video generation...')
        setProgress(10)

        const response = await fetch('/api/generate-video', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ promptId })
        })

        const result = await response.json()
        
        if (!response.ok) {
          throw new Error(result.error || result.details || 'Failed to generate video')
        }

        if (result.cached) {
          setStatus('📼 Video already exists - loading from cache!')
        } else {
          setStatus('✅ Video generated successfully!')
        }
        setVideoUrl(result.videoUrl)
        setProgress(100)
        
      } catch (err: any) {
        console.error('Video generation error:', err)
        setError(err.message)
        setStatus(`❌ ${err.message}`)
      } finally {
        setLoading(false)
      }
    }

    // Simulate progress updates with more realistic timing
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) return prev
        // Slower progress to match actual video generation time
        return prev + Math.random() * 5
      })
      
      // Update status messages based on progress
      setStatus(current => {
        if (current.includes('Starting')) return '📝 Analyzing script and audio...'
        if (current.includes('Analyzing')) return '🎨 Rendering mathematical animations...'
        if (current.includes('Rendering')) return '🎵 Synchronizing audio with video...'
        if (current.includes('Synchronizing')) return '📤 Uploading to cloud storage...'
        return current
      })
    }, 3000) // Slower updates for more realistic feel

    generateVideo().finally(() => {
      clearInterval(progressInterval)
    })

    return () => clearInterval(progressInterval)
  }, [promptId])

  const handleDownload = () => {
    if (videoUrl) {
      const link = document.createElement('a')
      link.href = videoUrl
      link.download = `video-${promptId}.mp4`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <div className="relative min-h-screen flex flex-col">
      {/* Silk background */}
      <div className="absolute inset-0 -z-10">
        <Silk speed={5} scale={1} color="#7CA3C7" noiseIntensity={0.2} rotation={0.14} />
      </div>
      
      <Navbar />
      
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-16 md:py-24">
        <div className="bg-white/20 backdrop-blur-md rounded-xl shadow-lg p-8 md:p-12 w-full max-w-4xl flex flex-col items-center animate-fade-in">
          
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-6 font-playfair text-center drop-shadow-lg">
            Video Generation
          </h1>

          {/* Status */}
          <div className="mb-8 text-center">
            <p className="text-lg text-white mb-4">{status}</p>
            
            {/* Progress Bar */}
            {loading && (
              <div className="w-full max-w-md mx-auto">
                <div className="bg-white/20 rounded-full h-3 mb-4 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-blue-400 to-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
                    style={{ width: `${Math.min(progress, 100)}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-200">{Math.round(progress)}% Complete</p>
              </div>
            )}
          </div>

          {/* Loading Animation */}
          {loading && !error && (
            <div className="mb-8">
              <div className="flex flex-col items-center space-y-4">
                <div className="relative">
                  <div className="w-16 h-16 border-4 border-white/30 rounded-full animate-spin"></div>
                  <div className="w-16 h-16 border-4 border-transparent border-t-white rounded-full animate-spin absolute top-0 left-0"></div>
                </div>
                <div className="text-center space-y-2">
                  <p className="text-white/80 text-sm">🎨 Creating mathematical animations...</p>
                  <p className="text-white/60 text-xs">This may take 2-5 minutes</p>
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="mb-8 p-4 bg-red-500/20 border border-red-400/30 rounded-lg">
              <h3 className="text-red-200 font-semibold mb-2">❌ Generation Failed</h3>
              <p className="text-red-100 text-sm">{error}</p>
              <button
                onClick={() => router.push(`/generated-script?id=${promptId}`)}
                className="mt-4 px-4 py-2 bg-red-500/30 text-red-100 rounded hover:bg-red-500/40 transition-all"
              >
                ← Go Back
              </button>
            </div>
          )}

          {/* Success - Video Preview */}
          {videoUrl && !loading && (
            <div className="w-full space-y-6">
              <div className="bg-green-100/10 border border-green-400/30 rounded-lg p-6">
                <h3 className="text-green-200 font-semibold mb-4 text-center">
                  ✅ Your Video is Ready!
                </h3>
                
                {/* Video Player */}
                <div className="mb-6">
                  <video
                    controls
                    className="w-full max-w-2xl mx-auto rounded-lg shadow-lg"
                    poster="/placeholder-video.png"
                  >
                    <source src={videoUrl} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                  <button
                    onClick={handleDownload}
                    className="px-6 py-3 bg-green-500/20 border border-green-400/30 text-green-100 rounded-lg hover:bg-green-500/30 transition-all flex items-center gap-2"
                  >
                    📥 Download Video
                  </button>
                  
                  <a
                    href={videoUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-6 py-3 bg-blue-500/20 border border-blue-400/30 text-blue-100 rounded-lg hover:bg-blue-500/30 transition-all flex items-center gap-2"
                  >
                    🔗 Open in New Tab
                  </a>
                  
                  <button
                    onClick={() => router.push('/my-videos')}
                    className="px-6 py-3 bg-white/20 border border-white/30 text-white rounded-lg hover:bg-white/30 transition-all flex items-center gap-2"
                  >
                    🎬 Create Another Video
                  </button>
                </div>
              </div>

              {/* Video Info */}
              <div className="bg-white/10 rounded-lg p-4">
                <h4 className="text-white font-semibold mb-2">📊 Video Details</h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                  <div className="text-gray-200">
                    <span className="text-gray-400">Format:</span> MP4 (H.264)
                  </div>
                  <div className="text-gray-200">
                    <span className="text-gray-400">Resolution:</span> 1080p
                  </div>
                  <div className="text-gray-200">
                    <span className="text-gray-400">Audio:</span> Synchronized
                  </div>
                  <div className="text-gray-200">
                    <span className="text-gray-400">Quality:</span> High
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Process Steps Info */}
          <div className="mt-8 w-full">
            <h4 className="text-white font-semibold mb-4 text-center">🔄 Generation Pipeline</h4>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white/10 rounded-lg p-4 text-center">
                <div className="text-2xl mb-2">📝</div>
                <div className="text-white text-sm font-semibold">Script Analysis</div>
                <div className="text-gray-300 text-xs">Parse JSON structure</div>
              </div>
              <div className="bg-white/10 rounded-lg p-4 text-center">
                <div className="text-2xl mb-2">🎨</div>
                <div className="text-white text-sm font-semibold">Manim Rendering</div>
                <div className="text-gray-300 text-xs">Create animations</div>
              </div>
              <div className="bg-white/10 rounded-lg p-4 text-center">
                <div className="text-2xl mb-2">🎵</div>
                <div className="text-white text-sm font-semibold">Audio Sync</div>
                <div className="text-gray-300 text-xs">Combine with narration</div>
              </div>
              <div className="bg-white/10 rounded-lg p-4 text-center">
                <div className="text-2xl mb-2">🚀</div>
                <div className="text-white text-sm font-semibold">Final Export</div>
                <div className="text-gray-300 text-xs">Upload & deliver</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
