---
description: Generate random mood anime prompts — one character shuffled across all PinGPT niches for maximum variety. Usage - /ranpin [number] [character]
---

# /ranpin — Random Mood Shuffle

// turbo-all

## The Vibe

**One character. Every mood.** Instead of locking into a single niche, `/ranpin` shuffles the character across ALL available PinGPT mood workflows — back-alley smoke breaks, 4am insomnia, rooftop rain, closing-time diners, street duos, dawn walks, ghost calls, mirror confrontations, last trains, waiting rooms. Every prompt is a different world.

This is a **content variety engine** — perfect for building out a character's Pinterest board with maximum visual diversity. Instead of 10 pins of the same vibe, you get 10 pins that show 10 different facets of the same character. This drives higher board engagement because followers don't fatigue on repetition.

> **52 moods and counting.** The mood pool now covers every emotional register — from 3AM bed-edge weight to Sunday apartment emptiness to 2AM gym catharsis to rain-soaked sad boy solitude to 90s nostalgia to imperfect beauty to gallery contemplation to sports hype to intellectual noir.

> **🚨 BUSINESS VALUE 🚨**
> Characters with diverse mood libraries build stronger follower loyalty. A viewer who saves a Gojo /lasttrain pin AND a Gojo /4amvibes pin is 3x more likely to follow the board than someone who sees 5 pins of the same niche.

## Usage

```
/ranpin 10 gojo        → 10 prompts for Gojo, each from a different random mood
/ranpin 5 megumi       → 5 prompts for Megumi across 5 different niches
/ranpin 8 toji         → 8 prompts for Toji shuffled across moods
/ranpin 3              → 3 prompts, auto-picks character + random moods
```

## Mood Pool

These are the available mood workflows to shuffle from. Each has its own complete DNA (environments, outfits, poses, lighting, palettes, emotional vibes):

> **🤖 AUTO-DISCOVERY:** In addition to the table below, check `mood_registry.json` for any MoodMind-generated moods not yet listed here. Any mood with `"source": "moodmind"` and `"status": "active"` is a valid shuffle target — read its workflow file at `_agents/workflows/{slug}.md`.

| # | Mood | Workflow | Core Aesthetic |
|---|---|---|---|
| 1 | Back-Alley Smoke Break | `/alleysmoke` | social exhaustion, introvert escape, the performance is over |
| 2 | 4AM Insomnia Solitude | `/4amvibes` | screen glow in dark rooms, convenience stores, the hour nobody sees you |
| 3 | Last Train Noir | `/lasttrain` | suited characters on late-night trains, rain-streaked reflections, lone-wolf |
| 4 | Rooftop Rain Catharsis | `/roofrain` | drenched in rain, defiant stance, city lights bleeding through downpour |
| 5 | Closing Time Diner | `/closingtime` | last customer, borrowed warmth, empty cafes, belonging nowhere |
| 6 | Dawn Walk Survival | `/dawnwalk` | waterfront at first light, survived the night, golden-blue liminal hour |
| 7 | Ghost Call Vulnerability | `/ghostcall` | 2AM phone calls, stairwell confessions, words they'd never say in daylight |
| 8 | Mirror Confrontation | `/mirrorself` | bathroom mirror at 3AM, identity crisis, the war behind closed doors |
| 9 | Hospital Waiting Room | `/waitingroom` | fluorescent purgatory, helpless warriors, the strongest rendered powerless |
| 10 | Street Duo | `/backstreet` | Japanese back-alley bond, daytime, street-level chemistry (auto-pairs a second character) |
| 11 | Green Breathing Room | `/greenbreath` | open-air exhale, looking up through trees, walls of ivy, the noise finally stops |
| 12 | Quiet Afternoon Off-Duty | `/quietday` | iced drinks by the window, sunlight on skin, the peaceful version nobody expects |
| 13 | Edge of Bed 3AM | `/edgeofbed` | sitting up in the dark, sheets tangled, the heaviest hour, back to camera |
| 14 | 2AM Gym Solitude | `/ironsilence` | training alone at 2AM, punching what they can't say, iron as therapy |
| 15 | Sunday Ghost | `/sundayghost` | afternoon light in empty apartments, laundry on the floor, the loneliest day |
| 16 | Sad Boy Rain | `/sadboy` | rain-soaked loners, headphones in the city, hoodie-up urban ghosts, feeling everything |
| 17 | Nostalgic Cel-Shade | `/retrocel` | VHS warmth, flat color fills, Evangelion-era palettes, the beauty of imperfect animation |
| 18 | Wabi-Sabi Beauty | `/wabisabi` | chipped ceramics, worn wood, kintsugi gold, the beauty of age and use |
| 19 | Gallery Stillness | `/gallerystill` | empty exhibition halls, art-within-art framing, contemplative distance, marble and light |
| 20 | Jersey Core | `/jerseycore` | sports streetwear crossover, athletic hype, team identity, jersey as fashion statement |
| 21 | Dark Academia | `/darkacademia` | libraries after hours, foggy campus, candlelit study, tweed and ink, the weight of knowing |
| 22 | Literally Me | `/literallyme` | *PLANNED — the meme-proxy aesthetic, characters as self-portraits of the viewer* |
| 23 | Laundromat Liminality | `/laundromat_liminality` | Fluorescent hum, spinning drum reflections, and the rhythmic waiting of a late-night chore in a soap-scented sanctuary. |
| 24 | Aquarium Blue Silence | `/aquarium_blue_silence` | Submerged blue light through glass, weightless solitude, and deep-sea tranquility. |
| 25 | Brutalist Monolith | `/brutalist_monolith` | Massive concrete planes, sharp architectural shadows, and the crushing scale of monumental indifference. |
| 26 | Rural Inaka Rust | `/rural_inaka_rust` | Blinding country sunlight, overgrown rail tracks, and the heavy, humid stillness of rural Japanese stagnation. |
| 27 | Gale-Force Clarity | `/gale_force_clarity` | Violent winds on high ridges, fluttering fabric, and the exhilarating sharpness of high-altitude cold air. |
| 28 | Mist-Veiled Bus Stop | `/mist_veiled_bus_stop` | Thick white fog obscuring the world, roadside waiting, and the soft isolation of a morning lost in mist. |
| 29 | Fumikiri Red Pulse | `/fumikiri_red_pulse` | Rhythmic red warning lights at railway crossings illuminating the blue-hour gloom as a silhouette waits for the train. |
| 30 | Petal-Storm Ephemera | `/petal_storm_ephemera` | High-velocity wind scattering thousands of cherry blossoms or autumn leaves, capturing a fleeting, beautiful goodbye. |
| 31 | Shallow Mirror-Tide | `/shallow_mirror_tide` | Walking across ankle-deep tide pools that perfectly reflect a vast, cloud-filled sky, erasing the horizon in ethereal blue. |
| 32 | Amber Archive | `/amber_archive` | Blinding sunbeams piercing through dusty, towering library stacks, highlighting suspended particles and the heavy stillness of ancient books. |
| 33 | Vapor-Glass Sanctuary | `/vaporglass_sanctuary` | Lush tropical flora trapped behind condensation-slicked glass panes, creating a blurred, emerald-tinted world of humid, sheltered isolation. |
| 34 | Sun-Drenched Downpour | `/sun_drenched_downpour` | Golden sunlight piercing through heavy rain, turning falling droplets into shimmering prisms against dark, moody storm clouds. |
| 35 | Ember Solace | `/ember_solace` | Firelight warmth against a freezing blue night, glowing sparks drifting into a snowy void. |
| 36 | Dashboard Horizon | `/dashboard_horizon` | Driving into a blinding sunset, car interior in deep shadow, golden light bleeding over the steering wheel. |
| 37 | Chlorine Blue Midnight | `/chlorine_midnight` | Floating weightless in a dark pool, underwater lights casting rippling turquoise caustics on the surface. |
| 38 | Drafting Table Dawn | `/drafting_dawn` | A single desk lamp illuminating meticulous work while the room is drowned in pre-dawn blue. |
| 39 | Storm-Drain Petals | `/storm_drain_petals` | Pink cherry blossoms trapped in the swirling gray water of an urban gutter during a heavy downpour. |
| 40 | Static-Screen Solitude | `/static_solitude` | Character sitting in front of a wall of old CRT monitors displaying white noise, the gray flicker lighting the room. |
| 41 | Fire-Escape Forest | `/fire_escape_forest` | Sitting on rusted iron stairs surrounded by a dense thicket of potted plants, golden hour light hitting the leaves. |
| 42 | Snow-Capped Phone Booth | `/snow_phone_booth` | A lone red phone booth buried in deep snow, its warm interior light glowing like a lantern in a blizzard. |
| 43 | Bakery Window Steam | `/bakery_steam` | Looking through a fogged bakery window at 5 AM; warm golden bread inside, blue cold outside. |
| 44 | Whale-Skeleton Museum | `/whale_museum` | Character standing beneath a massive blue whale skeleton in a moonlit, silent museum hall. |
| 45 | Rooftop Helipad Calm | `/helipad_calm` | Lying flat on a giant red 'H' on a skyscraper rooftop, looking up at a vast, cloudless sky. |
| 46 | Suburban Street-Light Haze | `/streetlight_haze` | The yellow-orange cone of a single streetlamp in a fog-heavy suburban cul-de-sac. |
| 47 | Tangled Wire Ghetto | `/wire_ghetto` | Character on a balcony overlooking a chaotic mess of power lines and transformers against a sunset. |
| 48 | Tunnel-Flash Rhythm | `/tunnel_flash` | The strobe effect of tunnel lights hitting a character’s face inside a fast-moving subway train. |
| 49 | Botanical Lab Decay | `/botanical_decay` | Overgrown science equipment, cracked test tubes with vines, and green/mossy palette in an abandoned lab. |
| 50 | Rooftop Water Tank Solitude | `/water_tank_solitude` | Sitting atop a rusted spherical water tank, legs dangling over a massive city grid. |
| 51 | Kitchen Light Confessional | `/kitchen_confessional` | Leaning against a fridge in a dark kitchen, the open door's light spill as the only source. |
| 52 | Terminal Gate Liminal | `/terminal_liminal` | Empty airport terminal at 3 AM, blue floor lights, wide expansive glass looking at stars. |

## Steps

1. Read the PinGPT engine modules:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. Parse input:
   - First word = **number of prompts** (required)
   - Second word = **character name** (or omit for auto-pick)

3. **Shuffle moods**: Randomly assign each prompt to a different mood from the pool above. Rules:
   - **No two consecutive prompts** may use the same mood (even in large batches)
   - **Maximize variety** — if generating ≤10 prompts, each should ideally use a DIFFERENT mood (no repeats)  
   - **If generating >10 prompts**, moods may repeat but must be spread as evenly as possible
   - **For `/backstreet` assignments**, auto-pair the character with a fitting second character from `/backstreet`'s pairing tables

4. For EACH assigned mood, read that mood's workflow file to load its complete DNA:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\_agents\workflows\[mood].md
```

5. Generate each prompt using that mood's FULL DNA (environments, outfits, poses, lighting, palette, shadows, emotional vibes, micro-details) — as if you were running that workflow directly. Apply ALL rules from `skill.md`.

6. Output each prompt with the standard PinGPT format, with an added **mood tag** showing which niche it came from.

---

## Output Format Additions

Each prompt in a `/ranpin` batch includes an extra header showing the source mood:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT [X/N] — 🎲 [MOOD NAME]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Standard PinGPT prompt output]

Mood: /[workflow]
```

Example:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROMPT 3/10 — 🎲 ROOFTOP RAIN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Full prompt following /roofrain DNA]

Mood: /roofrain
```

---

## Batch Diversity Guarantees

| Batch Size | Rule |
|---|---|
| 3 prompts | 3 different moods, guaranteed |
| 5 prompts | 5 different moods, guaranteed |
| 8 prompts | 8 different moods, guaranteed |
| 10 prompts | 10 different moods, guaranteed |
| 15 prompts | 15 different moods, guaranteed |
| 20 prompts | 20 different moods, guaranteed |
| 22 prompts | All 22 moods, one each — the full character showcase |
| 25 prompts | All 22 moods used, 3 repeats spread maximally apart |

---

## Smart Mood Ordering

Don't just randomize blindly — sequence the moods for **emotional arc** across the batch. This makes the output feel curated, not chaotic:

| Position | Mood Energy | Why |
|---|---|---|
| Open with | High visual impact (roofrain, lasttrain, backstreet, ironsilence, sadboy) | Hook attention on the first pin |
| Middle | Intimate/internal (mirrorself, ghostcall, 4amvibes, waitingroom, edgeofbed) | Pull the viewer deeper |
| Breather | Peaceful reset (greenbreath, quietday, sundayghost) | Contrast against heavy moods — makes both hit harder |
| Close with | Resolved/dawn (dawnwalk, closingtime) | Leave the viewer with emotional payoff |

This ordering is a suggestion, not a hard rule — but the sequence should FEEL intentional, not random noise.

---

## Character Fit Override

Some characters don't naturally fit every mood. When a mood is assigned, check the character against that mood's "Best Characters" table:
- **If the character is listed** → use directly, respect their rank-specific traits
- **If the character is NOT listed** → still generate, but lean into how this character would UNIQUELY inhabit that unfamiliar mood (this creates the most interesting pins — characters in unexpected contexts)

> **Example:** Gojo in `/waitingroom` isn't in the best-fit table, but the concept of the strongest sorcerer rendered powerless by a waiting room is INCREDIBLE content. Lean into the dissonance.

---

## Anti-Repetition (batch-level, ON TOP of each mood's own anti-repetition rules)

- **No two prompts** may use the same mood in sequence
- **No two prompts** may use the same emotional vibe tag, even across different moods
- **Outfits should vary** across the batch — if prompt 1 uses a hoodie (from /4amvibes), prompt 2 shouldn't also be hoodie-forward (even if it's /alleysmoke)
- **Lighting diversity** — ensure the batch contains at least 1 warm, 1 cold, and 1 mixed lighting setup
- **Time-of-day spread** — batch should span multiple times: night, pre-dawn, daytime, golden hour, late night
- **Cross-character environment uniqueness** — when generating `/ranpin` batches for multiple characters in the same session (e.g., `/ranpin 10 gojo` then `/ranpin 10 toji`), environments MUST NOT repeat across characters. If Gojo got an "empty subway car" scene from `/lasttrain`, Toji's `/lasttrain` prompt must use a completely different environment. Apply the Character-Scene Mutation rules from `skill.md § 8B` to ensure even thematically similar environments FEEL different per character.

