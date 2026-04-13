---
description: Generate rooftop-in-the-rain catharsis anime prompts — drenched suits, defiant stances, city lights bleeding through downpour. Usage - /roofrain [character] [number]
---

# /roofrain — Rooftop Rain Catharsis

// turbo-all

## The Vibe

**Let it pour.** Alone on a rooftop in a downpour. No umbrella. They came up here on purpose. Suit soaked through, hair plastered, city lights smeared below. Jaw set. Arms spread. Face turned up into the rain like they're daring the sky to break them first. The moment AFTER the breaking point — not grief, not sadness. **Release.**

This is a **catharsis niche** — the visual of someone surrendering to the storm drives disproportionate saves because the audience projects their own "I've had enough" moment onto it. Every image should feel like the last 30 seconds of an anime episode's emotional climax.

> **🚨 AESTHETIC DIRECTIVE: NO 2.5D BLENDING! 🚨**
> The character MUST be prompted strictly as flat 2D anime cel-shading and the background MUST be an out-of-focus richly detailed atmospheric backdrop. Force the mixed media contrast. Rain should read as atmospheric particles, character should read as anime cel art.

## Usage

```
/roofrain toji 5       → 5 rooftop rain prompts for Toji
/roofrain eren 3       → 3 catharsis prompts for Eren
/roofrain any 8        → 8 prompts, rotating best-fit characters
/roofrain              → 3 prompts, auto-picks from top roster
```

## Steps

1. Read the PinGPT engine modules (niche workflows load core + characters + output only — this workflow has its own DNA below):

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. Parse input:
   - First word = **character name** (or `any` to auto-select from the Roofrain character pool)
   - Second word = **number of prompts** (default: 3)

3. Generate prompts using the **Roofrain DNA** below, applying ALL rules from `skill.md` (5-Layer Formula, Visual Style Lock, 95-word cap, anti-repetition).

4. Output each prompt with the standard PinGPT format (prompt + caption + tags).

---

## Roofrain DNA — Vibe Lock

### Environment Pool (rotate, never repeat in a batch)

| # | Scene | Key Details |
|---|---|---|
| 1 | Highrise Rooftop Edge | concrete parapet, puddles pooling on flat roof, city skyline blurred by rain curtain, red aviation warning light on nearby tower |
| 2 | Apartment Building Roof | rooftop water tanks rusted, clothesline with soaked forgotten laundry, gravel surface, puddles reflecting neon from billboard below |
| 3 | Parking Garage Top Floor | open-air top level, rain hammering car hoods, empty except for one vehicle, fluorescent stairwell light spilling from door |
| 4 | Fire Escape Landing | narrow metal grate platform, rain pouring through gaps, brick wall behind, window light warm from apartment inside |
| 5 | Office Building Roof | HVAC units humming, rain pooling on industrial membrane, glass stairwell door behind letting warm interior light bleed out |
| 6 | Rooftop Garden Flooded | potted plants overflowing, wooden bench waterlogged, string lights shorted out, one still flickering, trellis with dripping vines |
| 7 | School Rooftop | chain-link fence around perimeter, concrete floor with faded painted lines, puddles reflecting grey sky, distant school clock tower |
| 8 | Hotel Rooftop Pool | drained or overflowing pool, rain cratering the surface, lounge chairs toppled, cabana fabric whipping in wind |
| 9 | Construction Site Roof | unfinished floor, rebar poking up, tarp half-torn flapping, rain pouring through gaps in temporary ceiling, crane visible |
| 10 | Shrine Rooftop View | from elevated shrine grounds looking over rain-drenched city, stone lanterns wet, wooden railing dark with water |
| 11 | Warehouse Roof | flat industrial roof, puddles reflecting distant factory smokestacks, rain so thick the city is just colored smears |
| 12 | Highrise Under Construction | skeletal steel beams, no walls, rain blowing through freely, city visible in all directions through the frame |
| 13 | Rooftop Basketball Court | cracked asphalt, rusted hoop, ball abandoned in puddle, chain net dripping, court lines barely visible under water |
| 14 | Bridge Overpass Top | standing on elevated highway overpass edge, cars rushing below with headlights streaking, guardrail wet, wind violent |
| 15 | Observation Deck After Hours | glass-walled observation platform, rain streaming down glass walls, city lights distorted through water, empty benches |
| 16 | Multi-Story Carpark Roof | spiral ramp edge, rain flooding the concrete, one distant car's tail lights glowing red through downpour |

### Outfit Lock (ruined formalwear / stripped-down, rotate variants)

| # | Style | Description |
|---|---|---|
| 1 | 🔒 Drenched Suit | dark fitted suit completely soaked, white shirt transparent and clinging, tie hanging loose, jacket heavy with water |
| 2 | Jacket Shed | suit jacket thrown on ground behind them, white dress shirt plastered to chest, tie pulled sideways |
| 3 | Shirtless Defiance | shirt stripped off and clenched in one fist, suit pants soaked, belt loosened, rain hitting bare skin |
| 4 | Overcoat Spread | long dark overcoat open like wings, arms slightly out, shirt beneath drenched, collar up but useless |
| 5 | Vest in Rain | suit jacket draped over railing, dark vest over white shirt both soaked, sleeves rolled showing forearms |
| 6 | Turtleneck Cling | dark turtleneck soaked and clinging to torso, dark pants, everything heavy with water, fabric stretched |
| 7 | Henley Stripped | dark henley pushed up to elbows, dog tags sticking to wet chest, dark cargo pants heavy with rain |
| 8 | Athletic Drench | dark compression shirt soaked, joggers dripping, bare feet on wet concrete, came up mid-workout |
| 9 | Leather Defiance | black leather jacket shedding water, white tee beneath soaked through, dark jeans, boots splashing |
| 10 | Morning-After Ruin | last night's blazer + untucked shirt, barefoot, clearly hasn't slept, rain as wake-up call |

### Pose Lock (ACTIVE defiance — never passive)

| # | Pose | Description |
|---|---|---|
| 1 | Face to Sky | head tilted full back, face turned directly up into rain, eyes closed or open, arms at sides fists clenched |
| 2 | Arms Spread | standing at rooftop edge, arms extended outward, rain hammering, coat/shirt billowing |
| 3 | Railing Grip | both hands white-knuckle gripping rooftop railing, head bowed between arms, rain streaming down back |
| 4 | Wall Punch | one fist pressed against wall or pillar, forehead against forearm, other arm hanging, dripping |
| 5 | Sitting in Puddle | sat down on wet rooftop floor, legs extended, leaning back on hands, looking up at rain |
| 6 | Walking Through Rain | mid-stride across rooftop, not running, deliberate slow walk, rain streaming off every surface |
| 7 | Jacket Strip | mid-motion pulling soaked jacket off one shoulder, head turned away, water spraying from fabric |
| 8 | Edge Crouch | crouched at building edge, forearms on knees, looking out over rain-blurred city below |
| 9 | Hair Sweep | one hand pushing completely drenched hair back off forehead, water cascading, jaw clenched |
| 10 | Scream Position | head thrown back, mouth open, tendons in neck visible, rain pouring into open mouth — silent scream |
| 11 | Shirt Wring | wringing soaked shirt out with both hands, bare-chested, water twisting out of fabric |
| 12 | Railing Lean Back | leaning backward against railing, elbows hooked over it, chest open to sky, chin up |

### Lighting Lock (ALWAYS storm-dramatic, dual-source)

| # | Setup | Description |
|---|---|---|
| 1 | Lightning Flash vs City Glow | split-second lightning freeze-frame painting everything blue-white against warm amber city below |
| 2 | Aviation Light vs Rain | red rooftop warning light casting crimson on one side, cold blue rain-ambient on other |
| 3 | Stairwell Spill vs Storm | warm yellow light bleeding from rooftop access door behind against cold blue-grey storm light |
| 4 | Neon Billboard vs Darkness | pink/cyan neon from rooftop billboard illuminating rain droplets against pitch-black sky |
| 5 | City Glow from Below | warm amber city light rising from below parapet edge against cold overhead storm darkness |
| 6 | Phone Glow vs Downpour | phone dropped face-up on wet ground, screen light casting upward warm glow against cold rain |
| 7 | Distant Window vs Storm | single warm lit window in adjacent building against vast cold dark storm, tiny warmth vs enormous cold |
| 8 | Car Headlights from Below | headlight beams from parking structure cutting through rain fog against cold overhead |

### Palette Lock (storm-dramatic, high-contrast)

| Primary | Secondary |
|---|---|
| Steel Storm Blue (40%) | Deep greys, near-blacks, cold blue-green, rain-grey |
| Lightning White-Blue (15%) | Electric white flash, frozen blue highlights, silver rain |
| Warm City Amber (20%) | Golden glow from below, amber streetlight bleed rising |
| Neon Rain Bleed (15%) | Rain droplets catching neon pink/cyan/magenta from signs |
| Raw Crimson (10%) | Aviation warning lights, distant brake lights, anger-coded warmth |

### Shadow Lock (storm-specific)

| Light Source | Shadow Color |
|---|---|
| Lightning flash | electric blue-white, near-silver |
| City amber from below | deep warm brown |
| Neon billboard | Deep magenta-black |
| Stairwell warm interior | Rich burnt sienna |
| Cold storm ambient | Steel grey-blue |

### Emotional Vibe Tags (rotate across batch, tag each prompt)

| # | Vibe | Description |
|---|---|---|
| 1 | The Breaking | composure finally cracking, raw and human and done performing |
| 2 | Baptism | the rain is cleaning something off them — metaphor for rebirth |
| 3 | Dare the Sky | not asking to be saved, daring the world to try harder |
| 4 | Post-Conversation | just hung up, just walked out, just said the thing they can't take back |
| 5 | Surrender | not giving up — giving IN, accepting what they've been fighting |
| 6 | Alive | the rain is the first thing they've FELT in months |
| 7 | Silent Scream | everything they can't say to anyone, given to the storm |
| 8 | After the Fight | physical or emotional — they won or lost, doesn't matter, it's done |

---

## Micro-Detail Mandatories (1-2 per prompt, rain-specific)

| Category | Examples |
|---|---|
| Rain on Skin | individual rain drops frozen on cheekbone, water streaming down jaw, rain pooling in collarbone |
| Fabric Damage | soaked shirt transparent showing skin beneath, tie dripping from end, jacket shoulder sagging with weight |
| Hair States | completely plastered to forehead, pushed back revealing full face, one strand stuck across eye |
| Ground Water | standing in ankle-deep puddle, rain craters visible in pooled water, ripples around feet |
| Rain Dynamics | diagonal rain indicating wind, rain caught in light beams as individual droplets, splash on impact |
| Body Temperature | goosebumps on forearms, visible breath in cold rain, steam rising from hot skin meeting cold rain |

---

## Best Characters for This Vibe

| Priority | Character | Why |
|---|---|---|
| 🥇 | Eren Yeager | Freedom vs cage — rooftop = the cage, rain = the freedom he can't reach |
| 🥇 | Toji Fushiguro | Raw physicality in rain. Shirtless in a downpour IS his energy. |
| 🥇 | Guts | The man who fights God. Standing in a storm is basically his Tuesday. |
| 🥈 | Gojo Satoru | The untouchable man choosing to FEEL something — rain on skin he usually shields |
| 🥈 | Aki Hayakawa | Already broken. The rain isn't the storm, he IS the storm. |
| 🥈 | Sung Jinwoo | Shadow monarch alone above his dominion. Power + isolation. |
| 🥉 | Levi Ackerman | Immaculate man allowing himself to be ruined. Maximum dissonance. |
| 🥉 | Megumi Fushiguro | Dark energy amplified. Rain + shadow = his element. |

---

## Virality Crossover Tags (CRITICAL for non-anime audience)

| Community | Tags |
|---|---|
| Storm Aesthetic | `#stormcore` `#rainaesthetic` `#stormvibes` `#thunderstorm` |
| Catharsis / Release | `#catharsis` `#letitgo` `#release` `#mentalhealth` |
| Literally Me | `#literallyme` `#relatable` `#moodaf` |
| Dark Aesthetic | `#darkaesthetic` `#moodboard` `#darkacademia` |
| Sigma / Defiance | `#sigma` `#lonewolf` `#unbreakable` `#resilience` |
| Lock Screen | `#lockscreenwallpaper` `#phonewallpaper` `#aestheticwallpaper` |

---

## Caption DNA for Roofrain Pins

### Title Patterns (rotate, never repeat in batch)

| Pattern | Example |
|---|---|
| Surrender statement | let it rain. he's done running. |
| Time stamp + weather | 11:52pm. downpour. he went up, not down. |
| Interior monologue | "the rain can have whatever's left" |
| Challenge | the sky tried to break him. it went the other way. |
| Fragment | soaked through and still standing |
| Second person | you know the feeling. roof. rain. done. |
| vs tension | the storm outside vs the one inside |
| Confession | he went to the roof because the walls were closer than people |

### Description Vibe
Write like someone watching this scene from a doorway, afraid to interrupt. Raw. Not pretty. Not poetic. Just real. Reference the universal moment of "I need air, I need out, I need to feel something."

### Hashtag Anchors (always include alongside standard character/aesthetic tags)
`#rooftopvibes` `#rainaesthetic` `#animerain` `#stormcore` `#darkanimeboy` `#catharsis` `#animenoir` `#drenched` `#rooftop` `#midnightrain` `#animewallpaper` `#defiance` `#rainynight` `#animeboy` `#darkaesthetic`

---

## Anti-Repetition (batch-level)

When generating 3+ prompts:
- **No two prompts** may use the same environment from the table
- **No two prompts** may use the same outfit variant
- **No two prompts** may use the same emotional vibe tag
- **No two prompts** may use the same pose
- **No two prompts** may use the same lighting setup
- **Rotate palettes** — max 2 of the same primary in a 5-prompt batch
- **At least 1 prompt** must feature warm amber tones from city glow below
- **At least 1 prompt** must feature a lightning flash composition
- **No two prompts** may use the same shadow lock color
