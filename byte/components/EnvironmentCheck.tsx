'use client'

import { useEffect, useState } from 'react'
import { hasValidSupabaseConfig } from '@/lib/supabaseClient'

export function EnvironmentCheck({ children }: { children: React.ReactNode }) {
  const [hasValidConfig, setHasValidConfig] = useState<boolean | null>(null)

  useEffect(() => {
    setHasValidConfig(hasValidSupabaseConfig())
  }, [])

  if (hasValidConfig === null) {
    return <div>Loading...</div>
  }

  if (!hasValidConfig) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-50">
        <div className="max-w-md p-6 bg-white rounded-lg shadow-lg border border-red-200">
          <div className="text-center">
            <div className="text-red-600 text-6xl mb-4">⚠️</div>
            <h1 className="text-2xl font-bold text-red-800 mb-4">
              Configuration Missing
            </h1>
            <p className="text-red-700 mb-4">
              The following environment variables are required but missing:
            </p>
            <div className="text-left bg-red-100 p-4 rounded border text-sm">
              <ul className="space-y-1">
                {!process.env.NEXT_PUBLIC_SUPABASE_URL && (
                  <li>• NEXT_PUBLIC_SUPABASE_URL</li>
                )}
                {!process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY && (
                  <li>• NEXT_PUBLIC_SUPABASE_ANON_KEY</li>
                )}
              </ul>
            </div>
            <p className="text-red-600 text-sm mt-4">
              Please check your Railway environment variables configuration.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return <>{children}</>
}
