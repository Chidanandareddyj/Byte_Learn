import { supabase, supabaseAdmin } from "@/lib/supabaseClient";

export async function getpromptbyID(promptID: string) {
  try {
    const { data, error } = await supabase
      .from("prompts")
      .select("*")
      .eq("id", promptID)
      .single();
    if (error) throw error;
    return data;
  } catch (error) {
    console.log(error);
  }
}

// Store generated script in database
interface ScriptData {
  prompt_id: string;
  script_text: string;
}

export async function saveScript(
  promptId: string,
  scriptText: string | object
): Promise<ScriptData | undefined> {
  try {
    const { data, error } = (await supabase
      .from("scripts")
      .insert({
        prompt_id: promptId,
        script_text:
          typeof scriptText === "object"
            ? JSON.stringify(scriptText)
            : scriptText,
      })
      .select()
      .single()) as any;

    if (error) throw error;
    return data;
  } catch (error) {
    console.error("Error saving script:", error);
    throw error;
  }
}

// Get script by prompt ID
interface Script {
  id: number;
  prompt_id: string;
  script_text: string;
  created_at: string;
}

export async function getScriptByPromptId(
  promptId: string
): Promise<Script | null> {
  try {
    const { data, error } = await supabase
      .from("scripts")
      .select("*")
      .eq("prompt_id", promptId)
      .order("created_at", { ascending: false })
      .limit(1);

    if (error) throw error;
    return data && data.length > 0 ? (data[0] as Script) : null;
  } catch (error) {
    console.error("Error fetching script:", error);
    throw error;
  }
}

export async function saveAudio(scriptId: string, audioUrl: string) {
  if (!supabaseAdmin) {
    throw new Error('Admin client not available - this function can only be called server-side');
  }
  
  const { data, error } = await supabaseAdmin
    .from('audios')
    .insert([{ script_id: scriptId, audio_url: audioUrl }])
    .select()
    .single()
  if (error) throw error
  return data
}

export async function getAudioByScriptId(scriptId: string) {
  const { data, error } = await supabase
    .from('audios')
    .select('*')
    .eq('script_id', scriptId)
    .order('created_at', { ascending: false })
    .limit(1)
  
  if (error) throw error
  return data && data.length > 0 ? data[0] : null
}

export async function saveVideo(audioId: string, videoUrl: string) {
  if (!supabaseAdmin) {
    throw new Error('Admin client not available - this function can only be called server-side');
  }
  
  const { data, error } = await supabaseAdmin
    .from('videos')
    .insert([{ audio_id: audioId, video_url: videoUrl }])
    .select()
    .single()
  if (error) throw error
  return data
}

export async function getVideoByAudioId(audioId: string) {
  const { data, error } = await supabase
    .from('videos')
    .select('*')
    .eq('audio_id', audioId)
    .order('created_at', { ascending: false })
    .limit(1)
  
  if (error) throw error
  return data && data.length > 0 ? data[0] : null
}

// Get video by prompt ID (through script and audio relationships)
export async function getVideoByPromptId(promptId: string) {
  const { data, error } = await supabase
    .from('videos')
    .select(`
      *,
      audios!inner(
        script_id,
        scripts!inner(
          prompt_id
        )
      )
    `)
    .eq('audios.scripts.prompt_id', promptId)
    .order('created_at', { ascending: false })
    .limit(1)
  
  if (error) throw error
  return data && data.length > 0 ? data[0] : null
}

