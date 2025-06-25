import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

export async function main(prompt: string) {
  const scriptPrompt = `
You are a math video generation assistant.
Given a user prompt "${prompt}", generate a JSON with the following structure:

{
  "title": "SceneTitleNoSpaces",
  "steps": [
    {
      "text": "Brief explanation text",
      "math": "LaTeX math expression"
    }
  ],
  "narration": "Full 2-3 minute educational narration script that explains the concept thoroughly, suitable for voice-over"
}

IMPORTANT REQUIREMENTS:
- title: Use PascalCase, no spaces or special characters (suitable as Python class name)
- steps: Array of objects with "text" and "math" fields
- math: LaTeX expressions compatible with Manim (use double backslashes for LaTeX commands)
- narration: Complete educational script (200-400 words) that thoroughly explains the concept

✳️ Output ONLY valid JSON. No explanations or markdown.
✳️ Ensure the "narration" field contains the full educational content.
✳️ Make narration engaging, clear, and beginner-friendly.
    `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.0-flash",
      contents: scriptPrompt,
    });
    if (!response.candidates || response.candidates.length === 0) {
      throw new Error(`Error generating script: No response received`);
    }
    console.log(response.candidates?.[0]?.content?.parts?.[0]?.text);
    const text = response.candidates?.[0]?.content?.parts?.[0]?.text;
    try {
      if (!text) throw new Error("No text received");

      // Clean the text to remove markdown code blocks if present
      let cleanedText = text.trim();
      if (cleanedText.startsWith("```json")) {
        cleanedText = cleanedText
          .replace(/^```json\s*/, "")
          .replace(/\s*```$/, "");
      } else if (cleanedText.startsWith("```")) {
        cleanedText = cleanedText.replace(/^```\s*/, "").replace(/\s*```$/, "");
      }

      const parsedResponse = JSON.parse(cleanedText);

      // Return only the Manim script for now
      return parsedResponse;
      /*
      // Return both scripts in a structured format (commented out for now)
      return {
        remotionScript: parsedResponse.remotionScript || parsedResponse, // fallback to old format
        ttsNarration: parsedResponse.ttsNarration || {
          title: parsedResponse.title || "Generated Video",
          fullScript: extractNarrationFromScenes(parsedResponse.scenes || []),
          segments:
            parsedResponse.scenes?.map((scene: any) => ({
              startTime: scene.startTime,
              endTime: scene.endTime,
              text: scene.text,
            })) || [],
        },
      };
      */
    } catch (parseError) {
      console.error("JSON parsing error:", parseError);
      return {
        error: "Failed to parse JSON response",
        rawText: text,
        format: "text",
      };
    }
  } catch (error) {
    console.error("Error generating script:", error);
    const errorMessage =
      error instanceof Error ? error.message : "Unknown error occurred";
    throw new Error(`Failed to generate script: ${errorMessage}`);
  }
}

// Helper function to extract narration text from scenes if needed
function extractNarrationFromScenes(scenes: any[]): string {
  return scenes.map((scene) => scene.text).join(" ");
}
