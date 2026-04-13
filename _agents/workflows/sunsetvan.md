---
description: Generate sunset camper van chillwave anime prompts — golden hour, beach solitude, vintage vans, warm coffee, serene lo-fi aesthetic. Includes Veo 3.1 animation guides. Usage - /sunsetvan [character] [number]
---

# /sunsetvan — The Golden Hour Sanctuary

// turbo-all

## The Vibe

**The Golden Hour Sanctuary.** This is the ultimate "chillwave" and "van life" aesthetic. A vintage camper van parked by a serene body of water (beach, lake, or cliffside), the sun setting low on the horizon casting deep oranges, pinks, and purples across the sky and water. The character is completely at peace—leaning against the van or sitting on the bumper, holding a steaming cup of coffee or tea. The harshness of the world is paused. It's a nostalgic, lofi-inspired sanctuary of warmth and solitude.

This aesthetic performs incredibly well on Pinterest and TikTok/Shorts because it taps into the universal desire for escape, slow living, and peaceful solitude.

> **🚨 AESTHETIC DIRECTIVE: FLAT ANIME CEL-SHADING 🚨**
> The character MUST be prompted strictly as flat 2D anime cel-shading to contrast with the richly detailed, beautifully lit atmospheric background. Strong, warm golden-hour lighting and long shadows are required.

## Usage

```
/sunsetvan nanami 5      → 5 sunset van prompts for Nanami
/sunsetvan any 3         → 3 prompts, auto-picks from the best-fit characters
```

## Steps

1. Read the PinGPT engine modules (niche workflows load core + characters + output only — this workflow has its own DNA below):

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. Parse input:
   - First word = **character name** (or `any` to auto-select from the fit character pool)
   - Second word = **number of prompts** (default: 3)

3. Generate prompts using the **Sunset Van DNA** below, applying ALL rules from `skill.md`.

4. **VEO 3.1 ANIMATION PROMPT:** For every generated output, you must also provide a specific "Veo 3.1 Motion Prompt" so the user can easily copy-paste it to animate the result into a cinemagraph loop.

5. Output each prompt with the standard PinGPT format (prompt + caption + tags + Veo 3.1 prompt).

---

## Sunset Van DNA — Vibe Lock

### Environment Pool (rotate, never repeat in a batch)

| # | Scene | Key Details |
|---|---|---|
| 1 | Sandy Beach Sunset | white vintage camper van parked on soft sand, gentle ocean waves rolling in, golden reflection on water, distant seagulls |
| 2 | Cliffside Overlook | van parked on a grassy cliff edge overlooking a vast ocean, sun dipping below the horizon, wind blowing through grass |
| 3 | Pine Lake Retreat | van parked by a calm alpine lake surrounded by pine trees, water reflecting the pink/purple sky perfectly like a mirror |
| 4 | Desert Highway Golden Hour | van pulled over on a long desert road, massive orange sun setting behind distant mesas, warm dust in the air |
| 5 | Coastal Highway Layby | parked by a guardrail facing the sea, coastal highway winding away, warm amber light hitting the side of the van |
| 6 | Forest Clearing Twilight | van in a grassy clearing, sun filtering horizontally through tree trunks, campfire just starting, fireflies appearing |
| 7 | Surf Spot Evening | surfboards leaning against the van, wet sand reflecting the magenta sky, peaceful post-surf exhaustion |
| 8 | Pier at Dusk | parked near an old wooden pier, water gently lapping at the pilings, sequence of streetlights just beginning to flicker on |

### Outfit Lock (chill, comfort, van-life casual)

| # | Style | Description |
|---|---|---|
| 1 | 🔒 Hoodie & Joggers | dark oversized hoodie, casual joggers, bare feet or slides, the ultimate comfort uniform |
| 2 | Open Flannel Layer | thick unbuttoned flannel over a plain t-shirt, relaxed denim, perfect for evening breezes |
| 3 | Oversized Knit Sweater | chunky, oversized knit sweater slipping off one shoulder, comfortable shorts |
| 4 | Windbreaker & Surf Shorts | retro color-block windbreaker unzipped, board shorts, salt-dried hair |
| 5 | Denim Jacket Casual | worn-in denim jacket over a hoodie, relaxed pants, classic road-trip attire |
| 6 | Simple Tank & Sweats | plain tank top catching the amber light, loose sweatpants |

### Pose Lock (anchored, peaceful, resting)

| # | Pose | Description |
|---|---|---|
| 1 | Leaning on Van Side | back flat against the side of the vintage van, one foot resting flat against the metal, holding a warm mug |
| 2 | Sitting on Rear Bumper | sitting on the open back bumper, legs dangling, looking out at the water |
| 3 | Roof Perch | sitting cross-legged on the roof of the van, leaning back on hands, staring at the horizon |
| 4 | Open Side Door Relax | sitting sideways in the open sliding door of the van, one leg pulled up, elbow on knee |
| 5 | Hood Lean | leaning elbows on the front hood of the van, body angled toward the sunset |
| 6 | Sand Sit by Tire | sitting on the ground leaning back against the front tire, knees bent, completely at peace |

### Lighting Lock (Golden Hour & Twilight)

| # | Setup | Description |
|---|---|---|
| 1 | Intense Golden Wash | strong, low-angle horizontal orange sunlight wrapping around the character, casting long deep shadows |
| 2 | Magenta/Purple Twilight | the sun has just set, leaving a rich gradient of pink to deep purple in the sky, soft ambient lighting |
| 3 | Backlit Silhouette | sun directly behind the character and van, creating a glowing rim-light outline with a darkened foreground |
| 4 | Campfire & Sunset Dual | warm flickering orange campfire lighting the face from below, cool blue/purple twilight behind them |
| 5 | Golden Water Reflection | amber light bouncing up from the wet sand/water, illuminating the character with a soft, watery glow |

### Palette Lock (Warmth and Nostalgia)

| Primary | Secondary |
|---|---|
| Golden Amber (40%) | Rich, warm orange and yellow from the setting sun |
| Deep Twilight Purple (20%) | The darkening sky at the opposite end of the sunset |
| Vintage White/Cream (20%) | The color of the classic camper van catching the light |
| Warm Shadow Charcoal (20%) | Deep, warm brownish-blacks for the long shadows, avoiding pure cool blacks |

---

## 🎬 Veo 3.1 Cinemagraph Animation DNA

When outputting the final result, append a section called **VEO 3.1 PROMPT**. Follow these rules to generate it:

The Veo prompt should instruct for a **cinemagraph loop** (where only specific elements move while the rest is completely frozen). Use this structure:

`Static camera. Cinemagraph. The character and van are perfectly still and frozen. [Insert ONLY ONE subtle environmental motion]. Anime style, no camera movement.`

**Motion Modifiers (pick ONLY ONE based on the scene to prevent warping):**
- `Gentle, rhythmic ocean waves rolling onto the sand.`
- `Slow, curling wisps of steam rising from the coffee cup.`
- `Subtle shimmering reflection of the sun on the water surface.`
- `Slow drifting seagulls passing high in the background.`
- `Dust motes slowly drifting through shafts of light.`
- `Soft flickering embers from the campfire.`

**Example Veo 3.1 Prompt:**
`Static camera. Cinemagraph. The character and the vintage van are perfectly still and frozen. Gentle, rhythmic ocean waves roll onto the shore. Anime style, no camera movement.`

---

## Micro-Detail Mandatories (1-2 per prompt)

| Category | Examples |
|---|---|
| Props | a steaming ceramic mug of coffee, an acoustic guitar leaning on the tire, a retro film camera on the bumper |
| Van Details | chrome hubcaps catching sunset glare, an open pop-top roof, a string of fairy lights inside the dark interior |
| Atmosphere | glowing dust floating in the sunbeams, scattered sea glass on the wet sand, a trail of footprints leading to the van |

---

## Best Characters for This Vibe

| Priority | Character | Why |
|---|---|---|
| 🥇 | Nanami Kento | Needs this vacation more than anyone. Sipping coffee, finally off the clock. |
| 🥇 | Shoto Todoroki | Quiet, introspective, enjoying the temperature balance of the fire and the cold evening breeze. |
| 🥇 | Geto Suguru | Unclenched, hair down, finding brief peace in a beautiful landscape. |
| 🥈 | Denji | Fascinated by a peaceful life he never thought he'd have, chilling by the water. |
| 🥈 | Satoru Gojo | Sunglasses off, enjoying the sunset colors (Six Eyes picking up every hue). |
| 🥈 | Roy Mustang | Fire alchemist enjoying a non-destructive setting sun, away from the military. |

---

## Caption DNA for Sunset Van Pins

### Title Patterns (rotate, never repeat in batch)
- the peace you've been looking for.
- miles away from everything.
- golden hour therapy.
- just the sound of the waves.
- no signal, no problems.

### Hashtags
`#vanlifeaesthetic` `#sunsetchill` `#lofivibes` `#goldenhouraesthetic` `#animeboy` `#peacefulanime` `#chillwave` `#cinemagraph` `#cozyvibes` `#escapism`
