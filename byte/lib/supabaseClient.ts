// lib/supabaseClient.ts
import { createClient, SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

export function hasValidSupabaseConfig() {
  return !!(supabaseUrl && supabaseAnonKey)
}

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase URL or anonymous key is missing. Check your .env file.')
}

// Client for browser/frontend operations
export const supabase = hasValidSupabaseConfig()
  ? createClient(supabaseUrl!, supabaseAnonKey!)
  : {} as SupabaseClient

// Client for server-side operations with full permissions
// Only available on server-side (API routes, server components)
export const supabaseAdmin =
  typeof window === 'undefined' && process.env.SUPABASE_SERVICE_ROLE_KEY && hasValidSupabaseConfig()
    ? createClient(supabaseUrl!, process.env.SUPABASE_SERVICE_ROLE_KEY)
    : null
