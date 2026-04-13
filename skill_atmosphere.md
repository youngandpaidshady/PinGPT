---
name: PinGPT Atmosphere
description: Color grading, lighting setups, shadow lock, time of day, weather, expressions, and micro-details.
---

# Atmosphere

## Color Grading

| Mode | Description |
|---|---|
| Desaturated Cool (DEFAULT) | muted steel blues, dark grays, near-blacks. Zero bright colors |
| Cold Blue | icy highlights, steel blue shadows, everything washed in frigid blue |
| High-Contrast Amber | deep mahogany shadows, bright honey highlights, REQUIRES cool-toned rim light |
| Monochrome B&W | high contrast, deep pure blacks and bright whites, no color |
| Teal & Orange | atmospheric teal and orange, warm skin tones against cool teal shadows |
| Golden Amber | warm golden-amber, honey highlights, deep mahogany shadows, skin glows |
| Sakura Pink | soft pink and cream, gentle warmth, blush highlights, delicate and airy |
| Neon Bleed | mostly dark, vivid neon pinks/cyans/purples bleed from off-screen sources |
| Rust & Copper | warm rust-orange and deep copper, industrial warmth, earthy |

## Lighting (ALWAYS use dual sources + SHADOW LOCK)

| Setup | Description |
|---|---|
| Single Source + Rim | single [source] with directional shadows + cool rim light on hair/shoulders |
| Dual Cross-Light | two opposite sources — one warm amber, one cold blue — split face |
| Underlight | lit from below (phone, campfire, puddle), upward shadows |
| Backlight Only | entirely from behind, rim-lit silhouette, face in shadow |
| Dappled / Broken Light | through blinds/fence/canopy, geometric shadow patterns |
| Colored Neon Wash | neon sign painting skin in pink/cyan/purple against black shadows |

### 🔒 Shadow Lock Rule (MANDATORY)

The character's shadows MUST match the background's light color temperature. This is what stops the composite from looking like a sticker on a stock photo.

| If background light is... | Character shadows must be... | NOT this |
|---|---|---|
| Cold blue moonlight | deep navy (#000080) | generic dark/black |
| Warm amber streetlight | rich burnt sienna | generic dark/black |
| Neon pink | deep magenta-black | generic dark/black |
| Golden hour | warm purple-shadow | generic dark/black |
| Fluorescent green-white | cool grey-green | generic dark/black |

**In your prompt, always specify**: "character's shadows cast in [color matching the light source]." Never leave shadows undefined — the model defaults to flat black, which breaks the composite.

### 🚫 BANNED LIGHTING (DO NOT USE)
- Flat, even daylight with no atmospheric modifiers
- Flat studio lighting
- Generic bright festival lighting
- Any single-temperature, uniform lighting

## Time of Day

| Time | Description |
|---|---|
| Golden Hour | warm amber sunlight, long horizontal shadows, purple shadow areas, dust motes or lens flare |
| Blue Hour | cold blue twilight, sky gradient indigo to pale blue, streetlights flickering on |
| Midnight | deep darkness, only artificial light — neon, lamps, distant streetlights |
| 3 AM Fluorescent | sickly buzzing fluorescent, slight green tint, unflattering but atmospheric |
| Neon Midnight | deep darkness broken by vivid neon signs painting character in colored light |

## Weather & Particles (use in ~50% of prompts)

| Weather | Description |
|---|---|
| Heavy Rain | pouring down, water streaking, puddles reflecting light |
| Snowfall | thick snowflakes drifting, accumulating on shoulders and hair |
| Dense Fog | thick fog, obscuring background, limited visibility |
| Cherry Blossoms | pink petals drifting, landing on shoulders |
| Wind Only | strong wind whipping hair and clothes, dynamic movement |
| Ember Sparks | tiny glowing orange embers drifting upward against dark |

## Expressions (40% visible, 60% obscured)

| Expression | Mood | Description |
|---|---|---|
| Stoic Default | Neutral | no emotion, flat affect, unreadable |
| Slight Smirk | Confident | one corner of mouth barely lifted, knows something you don't |
| Eyes Closed, At Peace | Warm | eyelids down, face relaxed, rare genuine rest |
| Genuine Soft Smile | Warm | real smile, corners of eyes crinkling |
| Confident Grin | Warm | wide cocky smile, head tilted, main character energy |
| Focused Concentration | Neutral | brow drawn, lips parted, eyes locked on task |
| Tired But Satisfied | Warm | heavy-lidded, small exhausted smile |
| Playful Side-Eye | Warm | looking sideways with teasing smirk |

## Micro-Details (MANDATORY — 1-2 per prompt)

| Category | Examples |
|---|---|
| Body | visible breath, single sweat droplet, wrapped knuckle, goosebumps, vein at temple |
| Accessories | single earring, thin chain necklace, analog wristwatch, black hair tie on wrist |
| Environmental | fingers trailing wet wall, steam from coffee cup, catching raindrop on palm |
| Clothing Flaw | one sleeve pushed up higher, collar askew, shirt untucked on one side, tag sticking out |
