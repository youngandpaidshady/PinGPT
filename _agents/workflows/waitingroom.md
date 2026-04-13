---
description: Generate hospital waiting room purgatory anime prompts — fluorescent hell, helpless warriors, the strongest rendered powerless by waiting. Usage - /waitingroom [character] [number]
---

# /waitingroom — Hospital Waiting Room Purgatory

// turbo-all

## The Vibe

**Nothing to fight. No one to save. Just wait.** Plastic chairs. Fluorescent hum. Coffee gone cold in a paper cup. The strongest character you know, rendered completely powerless by four walls and a clock that won't move. Elbows on knees, staring at linoleum. The most universal anxiety turned anime — waiting for news that changes everything. The audience FEELS this because they've BEEN here.

This is a **helplessness niche** — characters defined by their strength, stripped of everything that makes them powerful. No suit, no weapon, no technique. Just a man in a hard chair with nothing to do but think. These drive saves because the dissonance between "strongest character" and "most helpless situation" creates emotional gravity that pulls the viewer in.

> **🚨 AESTHETIC DIRECTIVE: NO 2.5D BLENDING! 🚨**
> Character = flat 2D anime cel-shading. Hospital/waiting room = richly detailed atmospheric. Force the mixed media contrast.

## Usage

```
/waitingroom nanami 5    → 5 waiting room prompts for Nanami
/waitingroom choso 3     → 3 protective brother prompts for Choso
/waitingroom any 8       → 8 prompts, rotating best-fit characters
/waitingroom             → 3 prompts, auto-picks from top roster
```

## Steps

1. Read the PinGPT engine modules (niche workflows load core + characters + output only — this workflow has its own DNA below):

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. Parse input:
   - First word = **character name** (or `any`)
   - Second word = **number of prompts** (default: 3)

3. Generate prompts using the **Waitingroom DNA** below, applying ALL rules from `skill.md`.

4. Output each prompt with the standard PinGPT format.

---

## Waitingroom DNA — Vibe Lock

### Environment Pool (rotate, never repeat in a batch)

| # | Scene | Key Details |
|---|---|---|
| 1 | ER Waiting Area | rows of connected plastic chairs, half-empty, triage window in bg, harsh overhead lighting, muted TV on wall |
| 2 | Hospital Corridor | long empty hallway, gurney against wall, room numbers on doors, distant nurse station glow, floor wax shine |
| 3 | ICU Family Room | small private room, single couch, tissue box on table, window overlooking parking lot at night, dim lamp |
| 4 | Pharmacy Pickup Counter | 4AM pharmacy, bright fluorescent, aisles behind, numbered tickets, single other person sleeping in chair |
| 5 | Vending Machine Alcove | hospital vending machine alcove, sterile tile, character lit by machine glow, coffee cup in hand |
| 6 | Clinic Lobby After Hours | chairs arranged in rows, reception desk dark and empty, one light left on, pamphlet rack, silent |
| 7 | Stairwell Between Floors | hospital stairwell, stripped concrete, harsh light, sitting on steps because the waiting room was too small |
| 8 | Chapel / Prayer Room | tiny hospital chapel, single candle, wooden pew, stained glass casting colored light on empty room |
| 9 | Parking Lot Outside ER | standing outside ER entrance, automatic doors, ambulance bay visible, harsh sodium lights, rain potential |
| 10 | Cafeteria at 3AM | hospital cafeteria, mostly dark, vending machines humming, single table lit by overhead, tray untouched |
| 11 | Rooftop Smoke Spot | hospital roof, HVAC units, characters sneak up here to breathe — looking down at ambulance bay |
| 12 | Elevator Between Floors | alone in hospital elevator, steel walls, floor indicator above door, fluorescent reflection in metal |
| 13 | Lab Waiting Area | small sterile room, numbered queue display, antiseptic smell implied by the clinical emptiness |
| 14 | Discharge Desk | standing at the admin desk at 5AM, signing papers, exhausted, dawn light through automatic doors |
| 15 | Outdoor Bench by Entrance | concrete bench outside hospital entrance, predawn, breath visible, hospital glow behind through glass doors |

### Outfit Lock (rushed / civilian / stripped of power)

| # | Style | Description |
|---|---|---|
| 1 | 🔒 Grabbed-and-Ran | jacket thrown over whatever they were wearing when the call came — mismatched, unbuttoned, shoes wrong |
| 2 | Still in Work Clothes | suit wrinkled from hours of sitting, tie long gone, collar undone, jacket balled up on next chair |
| 3 | Sleepwear Rush | sweatpants + hoodie thrown on at 2AM, slides instead of shoes, bed-head hair |
| 4 | Training Interrupted | compression shirt + joggers, came straight from gym, bag dropped on floor beside chair |
| 5 | Borrowed Hospital Blanket | thin hospital blanket draped around shoulders over whatever they're wearing, shivering |
| 6 | Uniform Still On | work uniform / combat uniform still partially on, didn't have time to change |
| 7 | Over-Layered Worry | multiple layers thrown on in panic — hoodie under jacket under coat, as if warmth = protection |
| 8 | Just-Arrived Formal | formal event clothes rumpled — suit with no tie, dress shoes unlaced, clearly left somewhere important |
| 9 | Day-Old Clothes | same clothes as yesterday, wrinkled, coffee-stained, hasn't left the hospital |
| 10 | Coat Over Nothing | long coat over undershirt/bare chest, literally grabbed one thing and ran |

### Pose Lock (collapsed / waiting / powerless)

| # | Pose | Description |
|---|---|---|
| 1 | Head in Hands | elbows on knees, face buried in hands, knuckles in hair, complete collapse |
| 2 | Floor Stare | slumped in chair, elbows on thighs, hands clasped, staring at floor tiles — counting lines |
| 3 | Pacing | mid-stride in empty corridor, hands in jacket pockets, jaw clenched, can't sit still |
| 4 | Wall Lean | back against corridor wall, slid partway down, one leg bent, staring at ceiling |
| 5 | Vending Machine Stand | standing in front of vending machine, hand flat on glass, not selecting anything, just staring |
| 6 | Coffee Grip | both hands wrapped around paper coffee cup, not drinking, just holding warmth |
| 7 | Phone Clutch | phone in one hand, screen dark, waiting for it to ring, other hand covering mouth |
| 8 | Chair Sprawl | sprawled in plastic chair, legs extended, head back against wall, eyes closed, not sleeping |
| 9 | Forehead on Clasped Hands | hands interlocked, forehead resting on them, eyes closed — looks like prayer |
| 10 | Standing at Window | palms flat on hospital window, looking out at dark parking lot, reflection ghostly in glass |
| 11 | Paper Cup Tower | absently stacking empty coffee cups, three tall, hands needing something to do |
| 12 | Corridor Crouch | crouched against hallway wall, forearms on knees, staring at opposite wall |

### Lighting Lock (institutional / clinical, dual-source)

| # | Setup | Description |
|---|---|---|
| 1 | Overhead Fluorescent vs Phone | harsh institutional fluorescent above against warm phone screen glow in hands |
| 2 | Corridor Split | half-lit corridor — lights on in their section, next section dark, boundary creating drama |
| 3 | Vending Machine vs Darkness | warm vending machine glow against dark hospital alcove, character lit in commercial warmth |
| 4 | Window Dawn vs Interior | cold pre-dawn light through window against warm-yellow corridor lights still on |
| 5 | Exit Sign vs Fluorescent | green or red EXIT sign casting colored light against standard fluorescent white |
| 6 | TV Glow vs Dark Room | muted TV on wall casting flickering blue-white against dim waiting room |
| 7 | Candle vs Sterile | tiny chapel candle warm amber against sterile white hospital light leaking through door |
| 8 | Ambulance Strobe vs Interior | distant red ambulance light painting through window against static interior fluorescent |

### Palette Lock (clinical, anxious, time-dissolved)

| Primary | Secondary |
|---|---|
| Fluorescent Sick White (40%) | Flat institutional white, green tint, honest and ugly |
| Vending Warm (15%) | Warm amber from machine displays, the only warmth in the building |
| Pre-Dawn Grey (20%) | That colorless hour when it's not night and not morning |
| Exit Sign Green/Red (10%) | Institutional color accents — green EXIT, red EMERGENCY |
| Coffee Brown (15%) | Warm paper-cup brown, hospital cafeteria amber, tiny comfort |

### Shadow Lock

| Light Source | Shadow Color |
|---|---|
| Hospital fluorescent | Cool grey-green |
| Vending machine glow | Warm amber-brown |
| Pre-dawn window | Cold steel blue |
| TV screen | Flickering cool blue-white |
| EXIT sign | Deep green-black or crimson-black |

### Emotional Vibe Tags (rotate across batch)

| # | Vibe | Description |
|---|---|---|
| 1 | The Powerless | the strongest person in any room, and none of it matters here |
| 2 | Counting Minutes | time has stopped, or maybe it's moving too fast — they can't tell |
| 3 | The Call | they got THE phone call and nothing before this moment matters |
| 4 | Protector Failed | they protect everyone, but couldn't prevent whatever put someone here |
| 5 | Bargaining | making promises to nothing — if they're okay, I'll be better |
| 6 | Vigil | they haven't left, they won't leave, someone has to be here when |
| 7 | The Good News Wait | not all waiting is grief — maybe it's hope, and that's worse |
| 8 | After the News | the doctor left, the door closed, they're still sitting here, processing |

---

## Micro-Detail Mandatories (1-2 per prompt)

| Category | Examples |
|---|---|
| Waiting Room Items | crumpled tissue, hospital bracelet, insurance card bent in fingers, clipboard form half-filled |
| Time Markers | wall clock showing 3:47AM, numbered ticket in hand, phone battery at 8%, three empty coffee cups |
| Body Tells | dark circles deepened, five-o'clock shadow, knuckles white from gripping, one leg bouncing |
| Hospital Props | thin blanket on lap, vending machine coffee, pamphlet about nothing in hands, hand sanitizer smell |
| Sound Implied | distant intercom page, clock ticking, vending machine hum, elevator ding, footsteps on linoleum |
| Personal Items | car keys still in hand, wallet overstuffed with insurance cards, crumpled parking receipt |

---

## Best Characters for This Vibe

| Priority | Character | Why |
|---|---|---|
| 🥇 | Nanami Kento | The man who carries responsibility. Waiting is his worst nightmare — he can't fix this with overtime. |
| 🥇 | Choso | THE protective brother. Someone he loves is behind that door. He hasn't moved in six hours. |
| 🥇 | Loid Forger | The spy who can infiltrate anything, but can't get past the "Family Only" sign. |
| 🥈 | Megumi Fushiguro | Stoic cracks here. The partner/friend/boss is in there and his composure is disintegrating. |
| 🥈 | Aki Hayakawa | The man who watched everyone around him get hurt. Waiting is where the guilt lives. |
| 🥈 | Yuji Itadori | The optimist forced to sit with worst-case scenarios. His energy has zero outlet. |
| 🥉 | Gojo Satoru | The invincible man in the one place where his power means absolutely nothing. |
| 🥉 | Levi Ackerman | He's lost everyone. This chair. This light. This wait. He knows how it ends. |

---

## Virality Crossover Tags (CRITICAL for non-anime audience)

| Community | Tags |
|---|---|
| Healthcare / Anxiety | `#hospitallife` `#anxietyrelief` `#mentalhealth` `#caregiver` |
| Emotional Core | `#inthefeels` `#deepfeelings` `#emotional` `#vulnerable` |
| Literally Me | `#literallyme` `#relatable` `#moodaf` |
| Liminal Spaces | `#liminalspaces` `#liminal` `#backrooms` `#fluorescent` |
| Dark Aesthetic | `#darkaesthetic` `#moodboard` `#aestheticboard` |
| Lock Screen | `#lockscreenwallpaper` `#phonewallpaper` `#aestheticwallpaper` |

---

## Caption DNA

### Title Patterns

| Pattern | Example |
|---|---|
| Clock entry | 3:47am. still here. |
| Lowercase confession | the strongest man in the building is the one who can't do anything |
| Interior monologue | "just tell me they're okay" |
| Fragment | plastic chair. cold coffee. no news. |
| Question | why do anime boys in waiting rooms make me feel things? |
| Second person | you've sat in this chair. you know this fluorescent. |
| vs tension | the warrior vs the waiting room |
| Time passage | hour four. same chair. same light. |

### Description Vibe
Write like someone who's been sitting in a waiting room for four hours and just opened their phone. Numb. Honest. Not dramatic — too tired for drama. Reference the universal experience of waiting for news. Short. Exhausted.

### Hashtag Anchors
`#waitingroom` `#hospitalcore` `#animeangst` `#darkmoment` `#animefeels` `#animevulnerable` `#3amanime` `#darkanimeboy` `#animeboy` `#helpless` `#animewallpaper` `#emotionalanime` `#midnightvibes` `#animewarrior` `#darkaesthetic`

---

## Anti-Repetition (batch-level)

When generating 3+ prompts:
- **No two prompts** may use the same environment
- **No two prompts** may use the same outfit variant
- **No two prompts** may use the same emotional vibe tag
- **No two prompts** may use the same pose
- **No two prompts** may use the same lighting setup
- **At least 1 prompt** must feature vending machine warm glow
- **At least 1 prompt** must feature a dawn/time-passage composition
- **No two prompts** may use the same shadow lock color
