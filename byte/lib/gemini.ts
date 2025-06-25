import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

export async function main(prompt: string) {
  const scriptPrompt = `
You are creating a cohesive 4-5 minute educational math video with perfect audio-visual synchronization.

Given the user prompt "${prompt}", generate a JSON with this EXACT structure:

{
  "title": "ConceptName",
  "totalDuration": 300,
  "introduction": {
    "text": "Brief hook that introduces the concept",
    "duration": 30
  },
  "sections": [
    {
      "title": "Section Title",
      "narration": "What the narrator says during this section (50-80 words)",
      "duration": 60,
      "visualSequence": [
        {
          "type": "text_display",
          "content": "Key concept text",
          "timing": [0, 15]
        },
        {
          "type": "math_equation", 
          "content": "x^2 + y^2 = z^2",
          "timing": [15, 45]
        },
        {
          "type": "graph_plot",
          "content": "function description",
          "timing": [45, 60]
        }
      ]
    }
  ],
  "conclusion": {
    "text": "Summary and key takeaways",
    "duration": 20
  },
  "fullNarration": "Complete script that matches the total duration (600-800 words)"
}

🎯 CRITICAL REQUIREMENTS:

**PERFECT TIMING SYNC:**
- Each visual element timing must match the narration exactly
- No overlapping visuals - one clear visual at a time
- Visual transitions should be smooth and logical

**VISUAL TYPES (USE ONLY THESE):**
- "text_display": Key concepts, definitions, introductions
- "math_equation": LaTeX expressions, formulas, equations  
- "graph_plot": Function graphs, coordinate systems
- "step_by_step": Breaking down problems with | separators
- "highlight_parts": Emphasizing specific parts of equations
- "real_world_example": Practical applications and examples

**EDUCATIONAL FLOW:**
1. Introduction (30s): Hook + basic concept
2. Foundation (60s): Core mathematical principle
3. Example (75s): Step-by-step problem solving
4. Application (75s): Advanced usage or real-world connection
5. Conclusion (20s): Summary and key takeaways

**NARRATION GUIDELINES:**
- Conversational and educational tone
- Speak directly to the audience ("Let's explore...", "Notice how...")
- Explain each step clearly as visuals appear
- Match timing: visual changes should align with spoken words
- 600-800 total words for 4-5 minute video

**TIMING PRECISION:**
- Each section duration should match visual sequence timings
- Visuals should not overlap (clear transitions)
- Total duration must equal sum of all sections + intro + conclusion
- Each visual should display for 10-30 seconds typically

✅ EXAMPLE TIMING FLOW:
- Text appears as you start explaining concept
- Math equation shows when you say the formula
- Graph displays when discussing visual representation
- Step-by-step breaks down problem solving process

❌ AVOID:
- Cluttered visuals or too many elements at once
- Misaligned timing between narration and visuals
- Overly complex LaTeX that might fail to render
- Vague or generic content descriptions

✳️ Output ONLY valid JSON. No markdown blocks.
✳️ Ensure ALL timings add up correctly.
✳️ Make each visual serve the specific narration moment.
✳️ Create a logical, flowing educational experience.
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
