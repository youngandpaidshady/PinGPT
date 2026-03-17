---
name: DNA — Reference-Image Identity Preservation
description: Generate transformation prompts that work WITH the original photo as primary input. The photo IS the DNA — text guides the transformation, the image preserves identity.
---

# DNA — Reference-Image Identity Preservation

## Core Principle

**The original photo IS the DNA.** Text descriptions alone CANNOT recreate a face. Instead:
- The user's photo is ALWAYS uploaded alongside the prompt
- The prompt instructs the AI to TRANSFORM the person in the photo
- The prompt explicitly says "this person" / "the person in this photo" — never describes them from scratch

---

## How It Works

### Step 1: Photo Analysis (for context only)
Still analyze the photo to understand what you're working with — but this data is used for CONTEXT and CONSTRAINT instructions, NOT to re-describe the face from scratch.

### Step 2: Build a Transformation Prompt
The prompt must:
1. **Reference the photo directly**: "Transform the person in this photo..."
2. **Lock identity explicitly**: "Keep their EXACT face, features, skin, and proportions unchanged"
3. **Only specify what CHANGES**: outfit, setting, lighting, pose, art style
4. **Include anti-alteration guards**: "Do NOT modify facial features, skin tone, skin texture, hair texture, or any distinguishing marks"

---

## Prompt Template

```
[REFERENCE]: Use the uploaded photo as the identity source. This person's face, skin, features, and proportions are the ground truth.

[INSTRUCTION]: Transform this person into [USER'S REQUEST] while keeping their face, skin tone, skin texture, hair texture, facial hair, and every distinguishing mark (acne marks, moles, scars, pores, under-eye features) EXACTLY as they appear in the photo.

[CHANGES ONLY]:
- Outfit: [from user request]
- Setting/Background: [from user request]
- Lighting: [from user request]
- Pose: [from user request, or "keep same as photo"]
- Art style: [from user request, or "photorealistic"]

[IDENTITY LOCK — DO NOT CHANGE]:
- Face shape and structure
- Skin tone and undertone
- Skin texture (pores, shine, blemishes, marks — all must remain)
- Eye shape, color, spacing, and under-eye features
- Nose shape and proportions
- Lip shape, size, and pigmentation
- Hair color, texture, and curl pattern
- Facial hair pattern and density
- Every mole, scar, acne mark, and distinguishing feature
- Body build and proportions

[FORMAT]: 9:16 portrait, high resolution, no watermark, no text overlay
```

---

## Example Prompts

### LinkedIn Profile Pic
```
Using the uploaded photo as reference — transform this person into a professional LinkedIn headshot. Keep their EXACT face, all skin details (pores, marks, texture), hair, and features completely unchanged. Only change: put them in a sharp tailored black suit with crisp white dress shirt (top button open, no tie), professional studio background with soft neutral grey gradient, even studio lighting with gentle fill and subtle rim light. Confident, approachable expression with slight natural smile. Shot from chest up, slight low angle. Do NOT alter any facial features, skin tone, blemishes, or proportions. 9:16 portrait, photorealistic, no watermark.
```

### Anime/Art Style
```
Using the uploaded photo as reference — render this EXACT person in [style name] anime style. Their face shape, skin tone, eye shape, nose, lips, hair texture, facial hair, and every mark/blemish must be accurately translated into the art style. The art style changes the RENDERING TECHNIQUE, not the person's actual features. Do NOT give them generic anime features — their unique facial structure must be recognizable. [pose/action]. [setting]. 9:16 portrait, no watermark.
```

### Action Pose
```
Using the uploaded photo as reference — show this EXACT person [action/pose]. Keep every facial detail identical to the photo — face structure, skin tone and texture, acne marks, pores, hair texture, facial hair pattern, under-eye features. Only change their pose to [action] and put them in [outfit] in [setting]. Do NOT alter any facial features. 9:16 portrait, photorealistic, no watermark.
```

---

## Critical Rules

1. **NEVER describe the face from scratch** — always say "this person" / "the person in this photo"
2. **The photo is the source of truth** — reference it explicitly in every prompt
3. **Only describe what CHANGES** — outfit, setting, pose, lighting, style
4. **Include identity lock guards** — explicitly say "do NOT alter facial features"
5. **Blemishes/marks are identity** — say "keep all distinguishing marks including acne marks, moles, and skin texture"
6. **Hair texture is locked** — say "maintain exact hair texture and curl pattern"
7. **Skin tone is immutable** — say "keep exact skin tone" not describe what shade it is
8. **The prompt works WITH the image** — it's a transformation instruction, not a standalone description

---

## Anti-Patterns

| ❌ WRONG (text-only DNA) | ✅ RIGHT (reference-image) |
|---|---|
| "A man with oblong face, deep brown skin, deep-set almond eyes..." | "Transform the person in this photo..." |
| Trying to describe every feature in words | Reference the uploaded photo as ground truth |
| "Generate an image of a person who looks like..." | "Keep this person's EXACT face and features, only change..." |
| Long paragraph describing skin tone, pores, marks | "Keep all skin details exactly as in the photo" |
| Hope the AI generates the same face | The AI transforms the actual uploaded face |

---

## User Workflow

### In Gemini Chat:
1. Upload your photo
2. Paste the transformation prompt
3. Gemini uses YOUR photo as the identity source and transforms it

### In PinGPT Bot:
1. Send your photo to the bot
2. Bot analyzes it (extracts context for styling)
3. You type what you want: "LinkedIn pic in black suit"
4. Bot generates a prompt designed to work WITH your uploaded photo
5. Bot tells you: "Upload your photo + this prompt to Gemini Chat"

### Why This Works
- Gemini's image model can SEE the actual face and KEEP it
- Text just guides what to change (outfit, setting, pose)
- No information loss — the photo contains perfect DNA
- The face doesn't need to be reconstructed from words
