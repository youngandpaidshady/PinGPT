---
name: PinGPT Photo-to-Prompt Mode
description: Transform user-uploaded photos into anime-style prompts with likeness preservation
---

# Photo-to-Prompt Mode

## Photo-to-Prompt Reverse Engineering

> **WHEN TO USE**: User provides a reference image they found in the wild (Pinterest, Twitter, etc.) and wants PinGPT to generate similar content.

**Step 1: Deconstruct the reference into the 4 layers:**

| Layer | Question to Answer |
|---|---|
| Physical Anchor | What specific object/interaction grounds the scene? |
| Spatial Logic | Where EXACTLY is the character in the space? |
| Dual Light Story | What two light sources compete? |
| Unspoken Narrative | What happened 5 seconds before this frame? |

**Step 2: Extract the visual DNA:**
- Color temperature (warm/cool/mixed)
- Dominant palette
- Composition type
- Art style
- Level of detail

**Step 3: Generate 5 variations** that keep the VIBE but change the specifics:
- Same light story, different environment
- Same physical anchor category, different character
- Same spatial logic, different time of day
- Same mood, completely different setting
- Same everything but swap the season

## Likeness Locks (CRITICAL for real person photos)

When transforming a user's uploaded photo into anime/art style, preserving **exact facial identity** is the #1 task.

### The Likeness Anchor Rules

1. **Rule of Immortality**: State early: *"The person's facial structure, bone structure, skin tone, skin texture, and every distinguishing mark are IMMUTABLE. Do not alter their identity."*
2. **Micro-Flaw Preservation**: Demand imperfections be kept: *"Keep the subtly asymmetric jawline, the exact shape of the nose bridge, under-eye texture, fine lines, and visible pores."*
3. **Anti-Beautification**: Forbid AI smoothing: *"ZERO AI smoothing, ZERO beauty filters, ZERO symmetry correction, ZERO generic 'anime pretty' face adjustments."*
4. **Style vs. Substance**: Clarify: *"The art style applies ONLY to the rendering technique (brushstrokes, shading, line art) and environment. The actual physical facial features must remain identical to the reference photo."*
5. **Pose Locking**: Force exact pose: *"Mimic the exact body language, limb positioning, head tilt, and camera framing of the reference photo."*

## Art Style Library (30+ styles for photo transformations)

**🇯🇵 Japanese**

| Style | Prompt Description |
|---|---|
| Clean Cel-Shading (DEFAULT) | clean anime cel-shading with defined black outlines and flat color fills, resembling a high-quality anime screenshot, composited over a atmospheric background with heavy bokeh |
| Ukiyo-e | traditional Japanese ukiyo-e woodblock print style with bold flat colors, thick black outlines, stylized waves and clouds |
| Samurai Ink | dramatic samurai-themed ink wash style with aggressive brushstrokes, splattered ink droplets, bold calligraphic energy |
| Sumi-e Wash | Japanese sumi-e ink wash with flowing brushstrokes, bleeding ink edges, white negative space |
| Shōnen Action | high-energy shōnen anime with dynamic speed lines, impact frames, exaggerated motion blur, screentone shading |
| Josei Elegance | refined josei manga with delicate thin linework, soft watercolor-like shading |

**🌍 African**

| Style | Prompt Description |
|---|---|
| Afrofuturism | blending traditional African patterns with futuristic technology, glowing tribal markings, gold and bronze metalwork |
| African Mythology | bold earth tones, intricate beadwork and body paint patterns, spiritual energy as golden light |
| Ankara Pattern Blend | vibrant Ankara/wax print patterns in clothing and background, bold geometric shapes |
| Tribal Ink | bold tribal ink with thick black linework inspired by African scarification patterns |

**🇰🇷 Korean**

| Style | Prompt Description |
|---|---|
| K-Drama atmospheric | soft dreamy focus, lens flare, warm golden skin tones, romantic color grading, film grain |
| Manhwa Sharp | ultra-sharp clean digital linework, vivid saturated colors, dramatic power auras |
| Webtoon Clean | soft smooth shading, pastel-adjacent palette, minimal outlines, digital airbrushed skin |

**🇨🇳 Chinese**

| Style | Prompt Description |
|---|---|
| Wuxia Martial Arts | flowing silk robes in motion, qi energy as swirling mist, traditional Chinese brushwork |
| Donghua Fantasy | modern donghua style with ethereal glowing effects, ornate traditional Chinese armor |
| Chinese Ink Landscape | traditional shan shui style with misty mountains, flowing water, ink gradients |

**🔥 Modern / Trending**

| Style | Prompt Description |
|---|---|
| Mappa Sakuga | MAPPA studio high-action with fluid dynamic poses, vivid particle effects, atmospheric camera angles |
| Dark Seinen | heavy shadow work, mature gritty linework, cross-hatching, muted desaturated palette |
| Glitch Anime | digital glitch with chromatic aberration, RGB channel splitting, corrupted scan lines |
| Neon Cyberpunk | heavy neon lighting in pink/cyan/purple, holographic overlays, rain-slicked futuristic streets |
| Lo-fi Grain | muted faded colors, visible film grain, soft light leaks, nostalgic dreamy atmosphere |

**🖌️ Artistic**

| Style | Prompt Description |
|---|---|
| Watercolor Bleed | soft watercolor with pigment bleeding outside lines, wet paper texture |
| Oil Paint Impasto | thick oil paint with visible heavy brushstrokes, dramatic chiaroscuro |
| Sketchy Lineart | raw graphite pencil sketch with visible construction lines, crosshatching |
| Digital Painting | semi-realistic digital painting with visible brushstrokes, ArtStation-quality |

**🏛️ World Cultures**

| Style | Prompt Description |
|---|---|
| Greek Mythology | marble-white and gold palette, laurel crown, Ionic column architecture, divine light rays |
| Aztec / Mayan | intricate Aztec geometric stone carvings, jade and obsidian palette, feathered serpent motifs |
| Art Nouveau | flowing organic linework, ornate floral border frames, muted jewel tones, Mucha-inspired |
| Norse Viking | runic engravings, fur and leather textures, cold steel-blue and blood-red palette |
| Egyptian Gold | gold and lapis lazuli palette, hieroglyphic border elements, Eye of Horus motifs |

**🎬 atmospheric**

| Style | Prompt Description |
|---|---|
| Shinkai atmospheric | Makoto Shinkai hyper-detailed with impossibly beautiful sky gradients, volumetric cloud lighting |
| Film Noir | extreme high-contrast B&W, venetian blind shadow patterns, 1940s detective atmosphere |
| Gothic Dark | ornate cathedral architecture, stained glass colored light, deep crimson and midnight purple |
| Mixed-Media Collage | torn paper textures, layered photographic elements, newspaper clippings, paint splatters |
| 90s Retro VHS | 1990s anime VHS aesthetic with scan lines, color bleeding, warm oversaturated colors |
| Manga Panel B&W | pure black and white manga panel with stark screentone shading, speed lines |
