---
description: Generate Pinterest captions, titles, and SEO descriptions for anime character images. Usage - /pincap [character] [number]
---

# /pincap — Generate Pinterest Captions for Existing Images

// turbo-all

## When to Use

Use `/pincap` when you already HAVE images and need Pinterest captions to post them. For generating prompts + captions together, use `/pingpt gojo 5` instead.

If the user attaches/describes specific images, tailor each caption to match that image. If no images are provided, generate generic but diverse captions for the character.

## Usage

```
/pincap gojo 5        → 5 caption sets for Gojo (generic, diverse moods)
/pincap toji 3        → 3 caption sets for Toji
```

If user provides images alongside the command, describe each image first, then write a caption that MATCHES that specific image.

## Steps

1. Read the PinGPT skill file for character roster and aesthetic dictionaries:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
```

2. Parse input:
   - First word = **character name**
   - Second word = **number of caption sets** (default: 5)

3. If user attached images: analyze each image and write a caption MATCHING it.
   If no images: generate diverse captions using the Diversity Slot Machine (vary mood/vibe per caption).

4. Output PER caption:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 PIN [N] — [vibe tag]

📝 TITLE (max 100 chars):
[Character name + aesthetic keyword + emotional hook]

💬 DESCRIPTION (125-500 chars):
[Fan voice, NOT robotic. Hook → scene → CTA/question. Natural keywords.]

🏷️ HASHTAGS (15-20):
#broad1 #broad2 #character1 #character2 #niche1 #niche2 ...

📎 ALT TEXT:
[Specific 1-sentence image description for accessibility + SEO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Caption Rules

1. **Titles** — NEVER repeat the same structure twice. Rotate: lowercase aesthetic ("when gojo walks home at 3am"), one-word punch ("obsessed."), questions ("why does this hit different?"), quote format ("i'll be fine" — toji, lying), fragments ("that look before he walks away"), second person ("you're not ready for this edit")
2. **Descriptions** — write like you're texting a friend, NOT writing marketing copy. Mix sentence lengths. One word. Then a longer thought. Max 1-2 emojis, only when natural. NEVER use `Hook → scene → CTA` formula for every caption. Vary your openings.
3. **Each caption = different mood** — rotate warm/dark/playful/ethereal/refined
4. **Hashtags** — 5 broad + 5 character + 5 niche + 3-5 trending
5. **Alt text** — specific, not "anime boy" but "anime illustration of Gojo at a ramen counter, warm lighting"
6. **BANNED** — No kanji titles (覚悟 — resolve). No `[Character] + [Aesthetic] + [Hook]` formula. These patterns get accounts flagged.

## Automated Pinterest Publishing via Browser Subagent

If the user requests the agent to automatically publish the generated `/pincap` captions to Pinterest:
1. **NO NATIVE UPLOADS:** Do NOT attempt to use the browser subagent to upload local image files. Pinterest's native file picker blocks automation. Instruct the user to manually drag-and-drop the images to create bulk drafts on the Pinterest Pin Creation page first.
2. **ACTIVE PAGE TAKEOVER:** Send the browser subagent to the CURRENT active Pinterest drafts page. Do not navigate to a new URL.
3. **EXPLICIT WAITS:** Pinterest uses a complex React UI. The subagent MUST use explicit delays (minimum 2+ seconds) between clicking a field to focus it, verifying the cursor, typing the text, and clicking the next UI element. Otherwise, keystrokes will randomly drop.
4. **BOARD VERIFICATION:** The subagent MUST explicitly verify that the correct board is selected from the dropdown before clicking Publish.
5. **DRAFT MATCHING (CRITICAL RETRAINING):** You are strictly FORBIDDEN from using tiny UI thumbnails for visual matching, as this causes hallucinated miscaptions. You MUST read the default Title (which automatically inherits the original file name). If the original file name is stripped or unavailable, you MUST click into the draft to view the full resolution image before attempting to match it against captions.md. Never guess based on a thumbnail.
