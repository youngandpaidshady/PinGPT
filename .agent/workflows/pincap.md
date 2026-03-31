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

1. **Titles** — scroll-stoppers: "The Silence After the Storm — Gojo" / "覚悟 — resolve." / "What Would Toji Do at 3 AM?"
2. **Descriptions** — write like a fan: "There's something about Gojo in the rain that hits different 🤍"
3. **Each caption = different mood** — rotate warm/dark/playful/ethereal/refined
4. **Hashtags** — 5 broad + 5 character + 5 niche + 3-5 trending
5. **Alt text** — specific, not "anime boy" but "anime illustration of Gojo at a ramen counter, warm lighting"
