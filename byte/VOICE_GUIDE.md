# Google TTS Voice Options for ByteLearn

## 🎤 Most Human-Like Voices for Educational Content

### **🌟 Top Recommendations:**

1. **`en-US-Neural2-D` (PROFESSIONAL_MALE)** ⭐ **CURRENT SELECTION**
   - Male, professional narrator style
   - Perfect for tutorials and educational content
   - Clear, authoritative, and engaging

2. **`en-US-Neural2-H` (AUTHORITATIVE_FEMALE)**
   - Female, mature and authoritative
   - Great for academic explanations
   - Professional and trustworthy

3. **`en-US-Neural2-C` (WARM_FEMALE)**
   - Female, warm and clear
   - Friendly and approachable
   - Good for beginner content

### **🎯 All Available Options:**

| Voice Name | Gender | Style | Best For |
|------------|--------|-------|----------|
| `en-US-Neural2-A` | Female | Natural, conversational | General content |
| `en-US-Neural2-C` | Female | Warm and clear | Beginner tutorials |
| `en-US-Neural2-D` | Male | Professional narrator | **Educational content** ⭐ |
| `en-US-Neural2-F` | Female | Conversational | Casual explanations |
| `en-US-Neural2-G` | Female | Young and energetic | Youth content |
| `en-US-Neural2-H` | Female | Mature, authoritative | Academic content |
| `en-US-Neural2-I` | Male | Calm and clear | Meditation, slow pace |
| `en-US-Neural2-J` | Male | Confident, engaging | Business, presentations |

## 🔧 How to Change Voice:

In `/app/api/generate-audio/route.ts`, modify this line:

```typescript
// Current voice selection - change this to test different voices
const CURRENT_VOICE = VOICE_CONFIG.PROFESSIONAL_MALE; // ← Change this
```

**Options:**
- `VOICE_CONFIG.PROFESSIONAL_MALE` (Current - best for education)
- `VOICE_CONFIG.WARM_FEMALE`
- `VOICE_CONFIG.AUTHORITATIVE_FEMALE`
- `VOICE_CONFIG.CONVERSATIONAL_MALE`
- `VOICE_CONFIG.ENGAGING_MALE`

## 🎛️ Audio Settings:

Current optimized settings for educational content:
- **Speaking Rate**: 0.95 (slightly slower for comprehension)
- **Pitch**: 0.0 (natural)
- **Volume**: 0.0 (standard)

## 🚀 Quick Test:

1. Change the `CURRENT_VOICE` variable
2. Regenerate audio for any script
3. Compare the voices to find your favorite!

**Note**: Neural2 voices are premium but provide the most human-like quality.
