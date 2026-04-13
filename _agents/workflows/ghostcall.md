---
description: Generate 2AM phone call vulnerability anime prompts — one-sided calls, stairwell confessions, the words they'd never say in daylight. Usage - /ghostcall [character] [number]
---

# /ghostcall — Phone Call at 2AM

// turbo-all

## The Vibe

**One-sided phone conversation.** You only see them. Sitting on a stairwell, leaning on a balcony, lying on a bed staring at the ceiling. Phone pressed to ear or held loosely. Is it good news or bad? You don't know. Their face says everything and nothing. The intimacy of a call nobody else can hear.

This is a **vulnerability-intimacy niche** — trending through `#2amthoughts` and `#latenightvibes` communities. The one-sided phone call is THE universal "I've been there" visual. The audience projects their own call — the ex, the parent, the friend they lost. These pins get bookmarked because they make people FEEL.

> **🚨 TRENDING CROSSOVER:** `#2amthoughts` + `#latenightvibes` + `#deepfeelings` + `#animevulnerable` — the "2AM confessional" hashtag cluster has massive crossover into wellness, relationship, and emotional quote boards.

> **🚨 NO 2.5D BLENDING!** Character = flat 2D cel-shading. Background = richly detailed atmospheric.

## Usage

```
/ghostcall loid 5     → 5 phone call prompts for Loid
/ghostcall any 8      → 8 prompts rotating characters
/ghostcall            → 3 prompts, auto-picks
```

## Steps

1. Read the PinGPT engine modules (niche workflows load core + characters + output only — this workflow has its own DNA below):
```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```
2. Parse input, generate with **Ghostcall DNA**, output PinGPT format.

---

## Ghostcall DNA — Vibe Lock

### Environment Pool (16 scenes, never repeat)

| # | Scene | Key Details |
|---|---|---|
| 1 | Apartment Balcony | small concrete balcony, railing, city lights below, potted plant dying, ashtray |
| 2 | Stairwell | apartment building stairwell, concrete steps, echo-prone, window on landing |
| 3 | Parked Car | sitting in driver's seat of parked car, dashboard glow, parking lot empty, rain on windshield |
| 4 | Bedroom Floor | sitting on floor beside bed, back against mattress, sheets trailing down, clock visible |
| 5 | Kitchen at Night | sitting on kitchen counter, feet dangling, fridge hum, dim range-hood light |
| 6 | Fire Escape | metal fire escape outside apartment window, city below, cold, wrapped in blanket |
| 7 | Hallway Outside Door | sitting against hallway wall outside their own apartment, keys beside them, didn't go in |
| 8 | Rooftop Access | sitting on rooftop near access door, back against wall, city sounds below |
| 9 | Bathroom Floor | sitting on cold tile floor, back against bathtub, phone light only illumination |
| 10 | Hotel Room | generic hotel room, curtains half open, city view, bed untouched, sitting on edge |
| 11 | Laundromat Bench | late-night laundromat, machines humming, bench, blue-white light, alone |
| 12 | Train Platform End | far end of empty platform, past last bench, sitting on edge, train tracks below |
| 13 | Convenience Store Parking | konbini parking lot, leaning against wall, fluorescent spill, plastic bag at feet |
| 14 | Park Bench at Night | dark park, one lamppost, bench, trees black around, distant road traffic |
| 15 | Office After Hours | empty dark office, one desk lamp on, swivel chair, everyone else left hours ago |
| 16 | Genkan / Entryway | sitting in apartment entryway, shoes on, hasn't gone in or out, stuck between |

### Outfit Lock (sleepwear / half-dressed / vulnerable, 10 variants)

| # | Style | Description |
|---|---|---|
| 1 | 🔒 Sweatpants + Bare | grey sweatpants, no shirt, chain/tags on chest, 2AM bed-escape |
| 2 | Oversized Tee | oversized dark tee hanging off one shoulder, boxers, bed-warm |
| 3 | Open Button-Up | wrinkled button-up hanging open over bare chest, last night's pants |
| 4 | Blanket Wrap | blanket/comforter wrapped around shoulders over whatever, cocoon |
| 5 | Hoodie Shield | dark hoodie pulled on, hood up, the "armor against emotions" layer |
| 6 | Suit Half-Stripped | suit pants + undershirt, tie and jacket somewhere else, came from event |
| 7 | Henley Sleep | dark henley, unbuttoned at collar, sleep-rumpled, barefoot |
| 8 | Athletic + Cold | just shorts + tank, bare feet on cold floor, grabbed phone and walked out |
| 9 | Coat Over Sleep | threw coat on over sleepwear to go outside for signal/privacy |
| 10 | Full Dressed Wrong | fully dressed at 2AM as if going somewhere, decided not to |

### Pose Lock (phone-anchored, intimate, 12 poses)

| # | Pose | Description |
|---|---|---|
| 1 | Phone to Ear Eyes Closed | phone pressed against ear, eyes closed, head tilted back, listening |
| 2 | Speaker on Chest | lying on back, phone on speaker resting on chest, staring at ceiling |
| 3 | Floor Sit | sitting on floor, knees up, phone in one hand between knees, other hand in hair |
| 4 | Balcony Lean | forearm on railing, phone to ear, looking out at city but seeing nothing |
| 5 | Forehead on Knees | curled up, forehead on knees, phone held loosely beside head |
| 6 | Pacing | mid-stride, pacing in small space, free hand gesturing, phone at ear |
| 7 | Counter Sit | sitting on kitchen counter, legs dangling, phone in both hands on lap, considering |
| 8 | Stair Sit | sitting on stairs, elbows on knees, phone in one hand, other rubbing eyes |
| 9 | Bed Edge | sitting on bed edge, hunched forward, phone at ear, feet on cold floor |
| 10 | Wall Slide | sliding down wall to floor, phone still at ear, legs extending |
| 11 | Window Lean | shoulder against window, phone to ear, reflection ghostly in glass |
| 12 | Post-Call | phone lowered from ear, held loosely at side, staring at nothing, call just ended |

### Lighting Lock (phone-intimate, 8 setups)

| # | Setup | Description |
|---|---|---|
| 1 | Phone Glow vs Dark Room | warm phone screen sole light source against pitch-dark room |
| 2 | City Through Window vs Interior Dark | distant warm city lights through window against dark interior |
| 3 | Moonlight vs Phone | cold moonlight through blinds creating stripes against warm phone underlight |
| 4 | Hallway Spill vs Dark Apartment | warm hallway light bleeding under door against dark apartment |
| 5 | Streetlight vs Shadow | single streetlight through window painting half the room amber, half shadow |
| 6 | Dashboard Glow vs Night | warm car dashboard instruments against dark parking lot outside |
| 7 | Fridge Light vs Kitchen Dark | open fridge casting cold rectangle of light against warm dark kitchen |
| 8 | Vending Machine vs Night | commercial vending glow on face against dark convenience store exterior |

### Palette Lock

| Primary | Secondary |
|---|---|
| Phone Screen Warm (30%) | Warm white-amber upward glow, intimate |
| Deep Night Black (30%) | Near-blacks, darkness, absence |
| City Distant Amber (15%) | Warm city glow through windows, far warmth |
| Moonlight Silver (15%) | Cold silver through blinds, stripes |
| Neon Bleed (10%) | Occasional neon from outside — motel sign, konbini |

### Shadow Lock

| Light Source | Shadow Color |
|---|---|
| Phone screen | Warm amber upward, deep navy elsewhere |
| Moonlight | Cool silver-blue |
| City ambient | Warm brown-grey |
| Dashboard | Cool green-amber |
| Fridge light | Cold blue-white |

### Emotional Vibe Tags (8 vibes)

| # | Vibe | Description |
|---|---|---|
| 1 | The Call You Shouldn't Make | calling someone you promised yourself you wouldn't |
| 2 | Bad News | just received or just delivered — the silence after the words |
| 3 | The Confession | saying the thing they've been holding for months, finally |
| 4 | 2AM Check-In | "are you okay?" — the call that means they care more than they show |
| 5 | Voicemail Listen | replaying a voicemail from someone who isn't around anymore |
| 6 | The Hang-Up | phone just lowered, call just ended, processing |
| 7 | Waiting for Pickup | phone ringing, they haven't picked up yet, each ring is louder |
| 8 | The Lie | "I'm fine." Said convincingly. Face says otherwise. |

---

## Micro-Details (1-2 per prompt)

| Category | Examples |
|---|---|
| Phone States | screen cracked, low battery indicator visible, call timer showing 47 min, contact name blurred |
| Sound Implied | muffled voice from phone speaker, clock ticking, distant traffic, rain on window |
| Body Tells | bags under eyes, hand trembling slightly, jaw clenched, one tear track, knuckles white |
| Temperature | bare feet on cold floor, blanket pulled tighter, visible breath on balcony |
| Time Markers | digital clock showing 2:38, darkness outside, no other lights in building |
| Evidence | empty cup, crumpled tissues, open contacts list, unsent text on screen |

---

## Best Characters

| Priority | Character | Why |
|---|---|---|
| 🥇 | Loid Forger | Calling handler vs calling Anya. The spy's two phones, two identities, one 2AM. |
| 🥇 | Nanami Kento | The man who never calls anyone, calling someone. That alone is the story. |
| 🥇 | Gojo Satoru | The loudest man being quiet. Phone to ear, no joke, no smirk. Devastating. |
| 🥈 | Choso | Calling about his brothers. Protective panic. The strongest emotion in the roster. |
| 🥈 | Aki Hayakawa | Calling someone who won't pick up. Calling someone who can't pick up. |
| 🥈 | Eren Yeager | "That scenery..." — the call to Armin, to Mikasa, to freedom |
| 🥉 | Megumi Fushiguro | Stoic on the phone. One-word answers. But he called first. |
| 🥉 | Aqua Hoshino | Calling his mother who's not there. Calling his sister at 2AM. |

---

## Virality Crossover Tags

| Community | Tags |
|---|---|
| 2AM Culture | `#2amthoughts` `#latenightvibes` `#cantsleeep` `#overthinking` |
| Deep Feels | `#deepfeelings` `#inthefeels` `#emotional` `#vulnerable` |
| Relatable | `#literallyme` `#relatable` `#moodaf` |
| Quotes/Aesthetic | `#aestheticquotes` `#moodboard` `#darkaesthetic` |
| Anime Core | `#animeboy` `#animewallpaper` `#animefeelings` |

## Caption DNA

### Title Patterns

| Pattern | Example |
|---|---|
| Lowercase | he called. she didn't pick up. he called again. |
| Time | 2:38am. phone ringing. please pick up. |
| Monologue | "i wasn't going to call" |
| Fragment | the call. the silence. the click. |
| Question | who are you calling at 2am? |
| Confession | he said "i'm fine." the ceiling heard the truth. |

### Hashtag Anchors
`#2amcall` `#phonecall` `#latenightvibes` `#animevulnerable` `#darkmoodanime` `#animeboy` `#animewallpaper` `#2amthoughts` `#overthinking` `#deepfeelings` `#literallyme` `#darkaesthetic` `#midnightvibes`

---

## Anti-Repetition

- No two prompts share environment, outfit, vibe, pose, or lighting
- At least 1 must feature phone-as-sole-light composition
- At least 1 must feature a post-call (phone lowered) moment
- At least 1 must feature a moonlight/blinds stripe composition
