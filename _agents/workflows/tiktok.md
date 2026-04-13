---
description: Generate TikTok 10-slide carousel anime prompts for character virality — hook-to-closer narrative arc. Usage - /tiktok [character] [number]
---

# /tiktok — TikTok 10-Slide Carousel Generator

// turbo-all

## The Vibe

**10 slides. One character. Maximum scroll damage.** Each slide is a different atmospheric scene designed for the swipe-through carousel format that dominates TikTok engagement. Hook slide stops the scroll. Closer slide makes them follow. Every slide in between escalates, shifts, and reveals.

## Usage

```
/tiktok gojo         → 10-slide carousel for Gojo
/tiktok toji 2       → 2 separate 10-slide carousels for Toji
/tiktok any          → auto-picks trending character
```

## Steps

1. Read the PinGPT engine modules:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_tiktok.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. Parse input:
   - First word = **character name** (or `any`)
   - Second word = **number of carousels** (default: 1)

3. Generate the 10-slide carousel using `skill_tiktok.md` pacing rules + character data from `skill_characters.md` + visual style from `skill.md`.

4. Output format (per carousel):

```
━━━━━━━━━━━━━━━━━━
🎬 TIKTOK CAROUSEL — [Character Name]

SLIDE 1 (🪝 HOOK — stop the scroll):
TITLE: [2-4 word scene title]
PROMPT: [complete NB2 prompt, 9:16 vertical]

SLIDE 2 (🌍 CONTEXT — full-body reveal):
TITLE: [2-4 word scene title]
PROMPT: [complete NB2 prompt]

... [slides 3-9] ...

SLIDE 10 (👑 CLOSER — wallpaper-quality hero shot):
TITLE: [2-4 word scene title]
PROMPT: [complete NB2 prompt]

📱 TIKTOK CAPTION:
[2 punchy lines + emoji + question hook + save CTA + series hook]

🏷️ TIKTOK TAGS:
[3-5 hashtags: 1 broad + 1 niche + 1 trending + 1 character]

🎵 SOUND SUGGESTION:
[Mood-matched trending sound from skill_tiktok.md]
━━━━━━━━━━━━━━━━━━
```

## Slide Arc (MANDATORY narrative progression)

| Slide | Role | Energy | Description |
|-------|------|--------|-------------|
| 1 | 🪝 HOOK | HIGH | Most dramatic, stop-the-scroll — extreme angle or lighting |
| 2 | 🌍 CONTEXT | MEDIUM | Full-body, environment reveal — establish the world |
| 3 | ⚡ ESCALATION | HIGH | Action pose, dynamic energy — build momentum |
| 4 | 🔍 TEXTURE | LOW | Quiet, micro-details, human touch — breathe |
| 5 | 💧 MOOD SHIFT | LOW | Vulnerability, emotional contrast — the turn |
| 6 | 🎬 PEAK | MAX | Most atmospheric, dramatic lighting — the money shot |
| 7 | 🎬 PEAK | MAX | Widest environmental shot — scale and isolation |
| 8 | 📐 DRAMATIC SHIFT | HIGH | Extreme angle surprise — jarring composition |
| 9 | 📐 DRAMATIC SHIFT | HIGH | Different extreme angle from slide 8 — keep surprising |
| 10 | 👑 CLOSER | MEDIUM-HIGH | Wallpaper-quality hero shot, most polished — the follow bait |

## Rules

- Same character with IDENTICAL physical description across all 10 slides
- Different outfit from character's wardrobe for each slide (match to setting)
- Different environment, pose, lighting, and color grade per slide
- All prompts are 9:16 vertical portrait
- Max 100 words per prompt
- End every prompt with the Mixed Media cel-shading composite tag
- NO text overlays in any prompt
