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

3. **⚠️ CRITICAL — SCENE NARRATIVE INTELLIGENCE IS THE #1 PRIORITY ⚠️**

   Before touching ANY dictionary table, you MUST construct a **cinematic micro-story scene** using Section 4.2's Scene Construction Formula. Every prompt starts by answering: **"What is the character doing RIGHT NOW, and what happened 5 seconds ago?"**

   The 4-layer construction order is NON-NEGOTIABLE:
   1. **PHYSICAL ANCHOR** — A hyper-specific object or interaction (marshmallow on a stick, guitar pick between teeth, condensation on a coffee cup, chalk dust on fingers). If the character has nothing in their hands and isn't interacting with anything, the scene is DEAD.
   2. **SPATIAL LOGIC** — Where EXACTLY in the space? Not "in a classroom" but "perched sideways on a student desk, back against the wall, one leg dangling." Spatial precision = cinematic framing.
   3. **DUAL LIGHT STORY** — TWO competing light sources. Campfire amber vs forest darkness. Desk lamp warm vs moonlight blue through blinds. NEVER single-temperature lighting.
   4. **UNSPOKEN NARRATIVE** — Implied through environment details (gym bag already packed = leaving, coffee half-drunk = been here a while, hoodie damp = just came in from rain).

   ❌ REJECT prompts like: "Gojo standing in a forest at night" (static, no moment)
   ✅ REQUIRE prompts like: "Gojo roasting a marshmallow over a campfire, sitting in a folding camp chair, firelight painting one side of his face while the other dissolves into forest shadow"

   **ONLY AFTER the scene is constructed**, layer on:
   - **Phase 1**: Character physical details from roster
   - **Phase 2**: Outfit, camera framing, composition from dictionaries
   - **Phase 3**: Color grade, weather, micro-details
   - **Phase 4**: Template structure (A/B/C rotation) wrapping the scene
   - **Phase 5**: Typography (30% unless forced)
   - **Phase 6**: Output format with Pinterest caption

4. **VISUAL STYLE LOCK — The Pinterest Anime Aesthetic**

   Every prompt MUST produce this specific composite look (skill.md Patterns 5 + 8):
   - **Character**: Clean anime cel-shading with defined black outlines, flat color fills, subtle line hatching for muscle/shadow. Resembles a high-quality anime screenshot.
   - **Background**: Photorealistic with heavy bokeh and soft focus. Real-looking environment behind an anime-drawn character.
   - **The Result**: A mixed-media composite — anime character on a real-world backdrop. This is THE signature Pinterest-aesthetic look. If the prompt doesn't specify this contrast, it will fail.

5. When generating multiple prompts (N > 1):
   - Run the **Diversity Slot Machine** before EACH prompt
   - No two consecutive prompts share the same mood, palette, OR template structure
   - **Every prompt must have a DIFFERENT scene seed / micro-story** — no two prompts should describe the same activity or spatial setup
   - At least 3/N must use warm palettes, 2/N must show activity poses
   - Each prompt gets its own matching Pinterest caption (title, desc, tags, alt text)
   - **6-8 out of N** should use the character's signature/themed outfit

6. Present output in this format PER PROMPT:

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
