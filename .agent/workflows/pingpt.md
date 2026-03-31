---
description: Generate a Pinterest-aesthetic anime character image prompt for NanoBanana 2 using the PinGPT skill
---

# /pingpt — Generate Anime Aesthetic Prompt

// turbo-all

## Usage

```
/pingpt gojo              → 1 prompt for Gojo
/pingpt gojo 5            → 5 prompts for Gojo (each with matching Pinterest caption)
/pingpt toji 3 mood:dark  → 3 dark mood prompts for Toji
/pingpt discover 5        → web search for trending character, then 5 prompts
```

## Steps

1. Read the PinGPT skill file to load the prompt engine instructions:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
```

2. Parse the user input:
   - **First word** = character name (match against roster, or `discover` for web search)
   - **Number** (if present) = how many prompts to generate (default: 1)
   - **Optional modifiers**: `mood:dark`, `setting:gym`, `color:cold_blue`, `time:midnight`, `weather:rain`, `outfit:streetwear`, `text:yes`

3. Follow the skill.md instructions exactly. Use ALL phases for EACH prompt:
   - **Phase 1**: Character from roster (or discover via web search)
   - **Phase 2**: Environment, outfit, pose, camera, composition
   - **Phase 3**: Color grade, time of day, weather/particles
   - **Phase 4**: Construct prompt using rotating template structures (A/B/C) + Scene Narrative Intelligence
   - **Phase 5**: Japanese typography (30% chance unless forced with `text:yes`)
   - **Phase 6**: Output with Pinterest caption INLINE per prompt

4. When generating multiple prompts (N > 1):
   - Run the **Diversity Slot Machine** before EACH prompt
   - No two consecutive prompts share the same mood, palette, OR template structure
   - At least 3/N must use warm palettes, 2/N must show activity poses
   - Each prompt gets its own matching Pinterest caption (title, desc, tags, alt text)
   - **6-8 out of N** should use the character's signature/themed outfit

5. Present output in this format PER PROMPT:

```
━━━━━━━━━━━━━━━━━━
[1/N] 🎴 [VIBE TAG — e.g. "Golden Hour Quiet" or "Neon Rain Energy"]

> [Complete natural language prompt — ready to paste into NanoBanana 2]

📋 Character: [Name] | Mood: [mood] | Color: [grade] | Time: [time] | Typography: [Yes/No]

📌 PIN CAPTION:
📝 TITLE: [scroll-stopping title, max 100 chars]
💬 DESC: [2-3 sentences, fan voice, natural keywords, ends with CTA/question]
🏷️ TAGS: #tag1 #tag2 ... (15-20 mixed broad + niche + character tags)
📎 ALT: [1 sentence describing the image for accessibility + SEO]
━━━━━━━━━━━━━━━━━━
```
