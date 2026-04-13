---
name: PinGPT PFP Vertical
description: Transform any PinGPT prompt into a TikTok-optimized profile picture. 1:1 square crop, face-forward, atmosphere-wrapped, identity-statement grade.
---

# PFP Vertical — TikTok Profile Picture Engine

> **PURPOSE:** PFPs are the #1 identity asset on TikTok anime pages. A curated PFP page (matching aesthetic across all posts) drives follower conversion 4x higher than random content. This module adapts the PinGPT engine for 1:1 square, face-forward, atmosphere-wrapped compositions optimized for circular crop display.

> [!IMPORTANT]
> PFP generation is a **separate output format**, not a separate engine. All PFP prompts still follow the core `skill.md` rules (5-Layer Formula, Visual Style Lock, NB2 constraints). This module only defines the ADAPTATIONS needed for square-crop, face-forward compositions.

---

## 1. PFP vs Standard Pin — Key Differences

| Rule | Standard PinGPT (9:16 Pin) | PFP Adaptation (1:1 Square) |
|------|---------------------------|----------------------------|
| Aspect Ratio | 9:16 portrait | **1:1 square** |
| Framing | Mid-shot (waist up), lower 40-60% | **Tight upper-body/face crop, character center-frame** |
| Negative Space | Generous top 30% (wallpaper zone) | **Minimal — atmosphere wraps tight around character** |
| Background | Full environmental scene | **Simplified, bokeh-heavy, 1-2 color atmosphere** |
| Face Visibility | 60% obscured / 40% visible | **80% visible — PFPs need recognizable face** |
| Text Ban | Standard (end-of-prompt) | **ABSOLUTE — PFPs tolerate zero visual noise** |
| Color Saturation | Muted/desaturated | **5-10% warmer than standard — must pop in circular crop** |
| Micro-Details | 1-2 environmental | **1 max — facial/hair only (rain on eyelash, wind in bangs)** |
| Physical Anchor | Required (object in hand, environmental interaction) | **Optional — face IS the anchor. If present, keep it at collar-level** |
| Foreground Depth | 70-80% of prompts | **30% max — foreground elements crowd the 1:1 frame** |
| Environmental Bleed | Mandatory (rain on hair, dust on skin) | **Still mandatory but simplified to 1 element** |

---

## 2. PFP Prompt Template

### Structure: FACE-FIRST (default for all PFP prompts)

```
Generate an image in 1:1 square orientation.

[CHARACTER NAME], [2-3 visual signature traits], framed from mid-chest upward, 
face centered in frame. [1 signature outfit element visible at neckline/collar]. 
[SINGLE facial micro-detail — rain droplet on cheek, wind lifting bangs, light 
catching one eye]. [SIMPLIFIED ATMOSPHERE: heavy bokeh gradient, 1-2 colors]. 
[DUAL LIGHTING on face — Source A color/direction vs Source B color/direction]. 
Expression: [specific expression]. Character's shadows cast in [shadow color].

MIXED MEDIA: Flat 2D anime cel-shaded character in signature anime outfit with thick black outlines, 
superimposed onto an out-of-focus richly detailed atmospheric background with 
heavy bokeh. The character MUST remain 100% flat 2D cel-shaded with anime-accurate clothing. ABSOLUTELY NO 
3D character rendering, NO 2.5D blending, NO CGI faces. Grainy film texture. 
ABSOLUTELY NO text, NO typography, NO kanji, NO watermarks, NO signatures, 
clean image.
```

### Structure: ATMOSPHERE-WRAP (when mood-atmosphere matters more than face detail)

```
1:1 Square Portrait:

[ATMOSPHERE — simplified environment described as color + light + particles]. 
[CHARACTER NAME], [2-3 traits], emerging from the atmosphere, upper body and 
face visible. [Outfit at collar/shoulder level]. [DUAL LIGHTING painting face]. 
[One environmental bleed element touching character]. Expression: [specific]. 
Character's shadows cast in [shadow color].

MIXED MEDIA: Flat 2D anime cel-shaded character in signature anime outfit with thick black outlines, 
superimposed onto an out-of-focus richly detailed atmospheric background with 
heavy bokeh. ABSOLUTELY NO text. Grainy film texture. Clean image.
```

---

## 3. PFP-Specific Rules

### The Circular Crop Test
> **Before finalizing any PFP prompt, mentally crop the expected output into a circle (TikTok's display shape).** Would the face still be centered? Would the key visual elements survive the circular mask? If critical details are in the corners, they'll be cut.

### Face Expression Palette (wider range than standard pins)
PFPs are identity statements — the expression IS the content. Expand beyond the standard 60/40 obscured/visible rule:

| Expression | When to Use | Frequency |
|-----------|------------|-----------|
| Subtle smirk / quiet confidence | Default PFP energy — "this is who I am" | 25% |
| Heavy-lidded calm / composed | Moody aesthetic pages | 20% |
| Direct eye contact through hair | Creates parasocial connection with profile viewer | 20% |
| Looking slightly off-frame | Mysterious, editorial energy | 15% |
| Genuine smile (rare for this character) | Emotional dissonance = highest engagement | 10% |
| Eyes closed, peaceful | Works for meditation/chill aesthetic pages | 10% |

### Color Temperature for PFP

PFPs display at 100-200px on most screens. Color needs to READ at tiny sizes:

| Palette Strategy | When | Why |
|-----------------|------|-----|
| **Warm dominant** (amber, gold, soft orange) | Default PFP recommendation | Warm tones pop in circular crop against dark TikTok UI |
| **Cool with warm accent** (blue atmosphere, amber eye-catch) | Moody/sad aesthetic pages | The warm accent prevents the PFP from disappearing into dark feeds |
| **High contrast split** (one side warm, one side cool) | Maximum scroll-stop | Dual-temperature face is visually arresting at any size |
| **Monochrome with color pop** (desaturated base, one vivid element) | Editorial/premium pages | Single color element (red scarf, blue eye) becomes the identity anchor |

> [!CAUTION]
> **Avoid fully desaturated/dark PFPs.** They disappear in TikTok's dark-mode UI. Every PFP needs at least ONE warm or bright visual anchor that reads at thumbnail size.

---

## 4. Mood-to-PFP Suitability

Not all moods translate equally to PFP format:

| Mood Category | PFP Potential | Why | Adaptation Notes |
|--------------|--------------|-----|-----------------|
| 🌧️ Rain Intimacy | 🔥🔥🔥 | Rain on face = instant visual drama at any size | Rain droplets as the sole micro-detail |
| 🏙️ Streetwear/Fashion | 🔥🔥🔥 | Outfit visible at collar creates fashion-identity PFP | Show jacket collar, hoodie edge, chain at neck |
| 😢 Sad Boy/Melancholic | 🔥🔥🔥 | Emotional face IS the identity statement | Heavy-lidded expression, atmospheric color wash |
| 🎐 Nostalgic Cel-Shade | 🔥🔥 | Warm retro tones pop in small crop | VHS grain adds texture even at small size |
| 📻 Acoustic/Analog | 🔥🔥 | Headphones/earbuds at collar = identity marker | One earbud visible at neckline |
| 🌿 Organic Melancholia | 🔥 | Nature elements need space to read | Simplify to single leaf/petal on shoulder |
| 🖼️ Gallery Stillness | ⚠️ | Scene-dependent mood loses impact without scene | Only works if character's expression carries the whole weight |
| 🗾 Wabi-Sabi | ⚠️ | Texture-dependent, hard to convey in 1:1 face crop | Map wabi-sabi to clothing texture (worn collar, frayed edge) |
| 💪 Action/Dynamic | ❌ | Movement doesn't read in static square crop | Skip for PFP — save for pins and carousels |

---

## 5. PFP Batch Anti-Repetition

When generating PFP batches (3+ PFPs for a cohesive aesthetic page):

- **Consistent palette family** — all PFPs in a page batch should share a color temperature (all warm, or all cool-with-warm-accent). This creates the curated page aesthetic.
- **Varied expressions** — no two PFPs in a batch use the same expression
- **Varied lighting direction** — alternate light source angles across batch
- **Character diversity** — use `DISCOVER_CHARACTERS()` from `skill_roster_discovery.md` with `obscurity_ratio: "50/50"` for PFP batches (mix familiar and fresh)
- **Micro-detail rotation** — rain on cheek, wind in hair, light catching eye, steam from breath — no repeats in batch

---

## 6. PFP Output Format

Each PFP prompt output includes:

```
━━━━━━━━━━━━━━━━━━━━━
PFP [X/N] — [MOOD]
━━━━━━━━━━━━━━━━━━━━━

[Full PinGPT prompt — 1:1 square]

📱 PFP CAPTION:
Title: [lowercase aesthetic caption for the PFP post]
Description: [2-line identity-statement text]

🏷️ HASHTAGS:
#animepfp #[character]pfp #[aesthetic]pfp #tiktokpfp #aestheticpfp
#[mood-specific tags from mood workflow]
```
