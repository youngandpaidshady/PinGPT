---
name: PinGPT Aesthetic Discovery Engine
description: Micro-mood scanning, trend signal processing, cyberpunk negative filter, and the workflow for discovering emerging anime aesthetics before they hit mainstream.
---

# Aesthetic Discovery Engine

> **PURPOSE:** This module transforms PinGPT from a static mood library into a self-updating creative engine. Instead of manually defining aesthetic niches, the engine scans visual platforms for emerging micro-moods and translates them into production-ready workflows.

> [!CAUTION]
> **CYBERPUNK NEGATIVE FILTER IS ACTIVE.** Every mood candidate discovered by this engine MUST pass the cyberpunk filter before entering the pipeline. We are pivoting away from neon-drenched, high-tech, and generic sci-fi aesthetics. See §3 for banned markers.

---

## 1. Signal Sources & Weights

The engine pulls trend signals from 5 sources, weighted by reliability and relevance:

| Source | Signal Type | Weight | Integration |
|--------|------------|--------|-------------|
| **Pinterest Trends** (search autocomplete + related pins) | Visual palette clustering, rising hashtag velocity, "more like this" chain analysis | 35% | Scan Pinterest search suggestions for rising anime aesthetic terms weekly. Track which visual styles appear in autocomplete that didn't 30 days ago. |
| **TikTok Creative Center** (trending hashtags + sounds) | Micro-mood velocity, audio-visual pairing, PFP page aesthetic clustering | 25% | Monitor hashtags in the anime/aesthetic intersection. Track sounds associated with specific visual moods — sound trends predict visual trends by 1-2 weeks. |
| **Jikan/MAL** (existing `trend_fetch.js`) | Airing schedule, member growth rate, genre tags | 20% | Already integrated. Use for series-level trend data and character sourcing. |
| **Reddit/X Visual Communities** (r/animewallpapers, r/moescape, anime art X accounts) | Upvote velocity on emerging styles, comment sentiment on aesthetic categories | 10% | Conceptual scan — identify which visual styles are getting disproportionate engagement relative to post frequency. |
| **Internal PinGPT Performance Data** (`performance_log.md`) | Save-rate spikes on specific palettes, moods, compositions | 10% | Feed back from existing pin performance. A sudden spike in saves for warm-toned pins = signal to weight warm moods higher. |

### Signal Processing Rules

1. **Velocity over volume.** A hashtag going from 500 → 5,000 uses in a week matters more than one stable at 100K. We chase acceleration, not mass.
2. **Cross-platform confirmation.** A mood that appears on BOTH Pinterest and TikTok simultaneously is 3x more valuable than single-platform signals.
3. **Visual-first, tag-second.** Hashtags lie (people mistagg). Visual clustering (similar color palettes, compositions, subject matter appearing independently) is the real signal.
4. **Recency window: 14 days.** Signals older than 2 weeks are stale for discovery purposes. They may still be valid for production but aren't "emerging."

---

## 2. Visual Marker Detection Framework

The engine scans for these micro-mood markers. Each marker has detection cues the LLM should look for when analyzing trending content.

### Currently Tracked Markers

| # | Marker | Detection Cues | Current Coverage | Priority |
|---|--------|---------------|-----------------|----------|
| 1 | 🌿 **Organic Melancholia** | Nature-reclaiming-urban, moss on concrete, overgrown train tracks, ivy on walls, roots through pavement | `/greenbreath` (partial) | HIGH — expand |
| 2 | 🌧️ **Rain Intimacy** | Close-up rain textures, rain on clothing, rain as emotional proxy, wet hair detail | `/sadboy`, `/roofrain` (strong) | MAINTAIN |
| 3 | 🎐 **Nostalgic Cel-Shade** | 90s flat color fills, VHS grain/scanlines, 4:3 aspect framing, Evangelion/Bebop-era palettes, visible cel paint edges | ❌ GAP | HIGH — create `/retrocel` |
| 4 | ☕ **Domestic Quiet** | Kitchen mornings, laundry folding, alarm clocks, teapot steam, the beauty of routine, morning light through curtains | `/quietday`, `/sundayghost` (partial) | MEDIUM — expand |
| 5 | 🏙️ **Streetwear Grounding** | Cargo pants, oversized silhouettes, sneaker culture, layered fits, fashion-as-identity, brand-less style | Outfit tables (scattered) | MEDIUM — consolidate |
| 6 | 📻 **Acoustic/Analog** | Vinyl records, cassette tapes, guitar picks, handwritten notes on paper, rotary phones, film cameras, warm analog tones | `/closingtime` (partial) | MEDIUM — expand |
| 7 | 🌅 **Golden Solitude** | Amber hour isolation, warm-toned loneliness, sunset-lit empty spaces, long shadows, everything bathed in honey | `/dawnwalk` (partial) | LOW — covered |
| 8 | 🗾 **Wabi-Sabi Spaces** | Chipped ceramics, worn wood, patina, deliberately aged surfaces, imperfect beauty celebrated, kintsugi aesthetic | ❌ GAP | HIGH — create `/wabisabi` |
| 9 | 🖼️ **Museum/Gallery Stillness** | Empty exhibition halls, characters dwarfed by art, art-within-art framing, contemplative distance, marble and light | ❌ GAP | HIGH — create `/gallerystill` |
| 10 | 🚬 **Post-Performance Collapse** | After the fight/show/exam, towel over head, exhaustion-as-beauty, the performance is over | `/alleysmoke`, `/ironsilence` (partial) | LOW — covered |
| 11 | 🌊 **Coastal Erosion** | Sea-worn concrete, rusted guardrails, salt-bleached wood, ocean fog, characters at the edge of land | ❌ GAP | MEDIUM — future |
| 12 | 📚 **Worn Page** | Libraries, old books, reading nooks, candlelight on worn paper, ink stains, knowledge as solitude | `/darkacademia` ✅ | COVERED |
| 13 | ⚽ **Jersey Core** | Anime characters in football/soccer/basketball jerseys, sports streetwear crossover, team-color palettes, athletic confidence poses, wearable fandom fashion | `/jerseycore` ✅ | COVERED |
| 14 | 📖 **Dark Academia** | Libraries after hours, foggy campus walks, tweed/wool textures, candlelit study, fountain pen, leather-bound books, intellectual melancholy | `/darkacademia` ✅ | COVERED |

### Adding New Markers

When the weekly scan surfaces a visual pattern not in the table above:

1. **Name it** — working title + 3-word vibe phrase (e.g., "Coastal Erosion: salt-worn edges")
2. **Define 5+ detection cues** — specific visual elements that identify this mood
3. **Map coverage** — does any existing workflow partially cover this?
4. **Score priority** — based on signal velocity + PinGPT production fitness
5. **Append to table** — the marker table is a living document

---

## 3. Cyberpunk Negative Filter (MANDATORY)

> **Every mood candidate, every prompt, every batch must pass this filter.** The anime aesthetic market is oversaturated with cyberpunk/neon/tech visuals. Our competitive edge is organic, emotionally grounded content.

### Banned Aesthetic Markers

| Banned Signal | Why | Safe Alternative |
|--------------|-----|-----------------|
| Holographic UI overlays | Saturated sci-fi market | Analog devices (radio, vinyl, paper, weathered screens) |
| Circuit-board / motherboard patterns | Generic tech aesthetic | Organic textures (wood grain, moss, woven fabric, stone) |
| Full-neon palettes (>40% neon in scene) | Oversaturated on Pinterest | Neon bleed capped at 15%, ONLY as environmental reflection |
| Robot / mech companion elements | Sci-fi genre drift | Animal companions, analog objects, plants |
| Laser / energy beam weapons | Generic action aesthetic | Traditional weapons, instruments, craft tools, bare hands |
| Digital rain / matrix effects | Dead 2019 aesthetic | Physical rain, dust motes, cherry petals, pollen |
| Chrome / metallic skin tones | Uncanny valley | Natural skin pallor, environmental bleed on skin |
| Floating holographic screens | Tech-utopia trope | Physical books, paper notes, photographs, letters |
| Glitch / data-corruption effects | Played out, everyone does it | Film grain, water damage, light leak, lens flare |
| LED strip / underglow on everything | TikTok oversaturation | Candles, oil lamps, firelight, window-filtered sunlight |

### The Neon Bleed Exception

> [!IMPORTANT]
> We do NOT eliminate neon entirely. "Neon Bleed" is a core PinGPT palette element (used in `/sadboy`, `/lasttrain`, 3AM Pack) and it WORKS. The distinction:
>
> ✅ **Organic neon** — neon light reflected in a rain puddle, a distant konbini glow bleeding through fog, pink neon painting one cheek from an off-frame source
>
> ❌ **Cyberpunk neon** — full neon cityscape as primary backdrop, character surrounded by neon tubes, neon as the SUBJECT rather than ambient light
>
> **Rule: Neon never exceeds 15% of total scene palette. It is always reflected, filtered, or distant — never direct.**

### Filter Application

Apply the filter at **three checkpoints**:

1. **Mood Discovery** — when scoring a new micro-mood candidate, reject if >30% of its visual markers overlap with banned signals
2. **Prompt Generation** — before finalizing any prompt, scan for banned terms and replace with safe alternatives
3. **Post-Generation QA** — visually inspect generated images for cyberpunk drift (NB2 sometimes adds neon elements not in the prompt)

---

## 4. Micro-Mood Discovery Workflow

### Weekly Cadence

```
┌─────────────────────────────────────────────────────┐
│  AESTHETIC DISCOVERY PIPELINE — WEEKLY CYCLE        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. SCAN     Pull signals from all 5 sources        │
│       ↓                                             │
│  2. CLUSTER  Group visual markers into candidates   │
│       ↓                                             │
│  3. SCORE    Rate: novelty × velocity × fitness     │
│       ↓                                             │
│  4. FILTER   Apply cyberpunk negative filter        │
│       ↓                                             │
│  5. NAME     Working title + 3-word vibe phrase     │
│       ↓                                             │
│  6. DRAFT    Generate 3 test prompts                │
│       ↓                                             │
│  7. TEST     Generate images via /gemgen            │
│       ↓                                             │
│  8. GATE     Quality + NB2 compatibility check      │
│       ↓                                             │
│  9. SHIP     Create workflow .md + add to /ranpin   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Step Details

**Step 1 — SCAN**
- Run `trend_fetch.js` for Jikan/MAL data (airing shows, member growth)
- Manually scan Pinterest search for rising anime aesthetic terms
- Check TikTok Creative Center for velocity spikes in anime-adjacent hashtags
- Review `performance_log.md` for internal save-rate anomalies
- Time budget: 15 minutes

**Step 2 — CLUSTER**
- Group raw signals by visual similarity, not series or character
- Ask: "What FEELING do these signals share? What would the color palette look like?"
- A valid cluster needs 3+ independent signals converging

**Step 3 — SCORE**
Each candidate mood gets a 0-100 composite score:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Novelty (not in current library) | 30% | 100 = completely new, 0 = fully covered by existing workflow |
| Velocity (acceleration rate) | 30% | 100 = explosive growth, 0 = flat/declining |
| PinGPT Fitness (can we produce it?) | 25% | 100 = perfect NB2 compatibility + character availability, 0 = impossible to render |
| Cross-Platform Confirmation | 15% | 100 = confirmed on 3+ platforms, 0 = single source only |

**Threshold: Score ≥ 60 = proceed to naming. Score < 60 = log and revisit next week.**

**Step 4 — FILTER**
- Run candidate through §3 Cyberpunk Negative Filter
- If >30% of the mood's visual markers overlap with banned signals → reject
- If borderline → reframe the mood away from tech elements and re-score

**Step 5 — NAME**
- Working title: 1-2 words (e.g., "Coastal Erosion", "Worn Page", "Gallery Still")
- Vibe phrase: exactly 3 words that capture the emotional core (e.g., "salt-worn edges", "ink-stained solitude")
- Slash command: `/[lowercase]` (e.g., `/coastalerosion`, `/wornpage`)

**Step 6 — DRAFT**
- Generate 3 test prompts using existing PinGPT engine rules
- Use 3 different characters (prefer 1 Tier 1 proven performer + 2 fresh discoveries)
- Apply the full 5-Layer Formula from `skill.md`

**Step 7 — TEST**
- Generate images through `/gemgen` pipeline
- Check for NB2 rendering quality, style lock compliance, cyberpunk drift

**Step 8 — GATE**
Quality checklist:
- [ ] All 3 images pass the Wallpaper Test
- [ ] All 3 images pass the Scroll-Stop Test
- [ ] Zero cyberpunk filter violations in generated images
- [ ] Character likeness maintained
- [ ] Mixed media composite (2D character on atmospheric background) holds
- [ ] No text/kanji hallucination

**Step 9 — SHIP**
- Create full workflow `.md` file following existing niche workflow structure (environments, outfits, poses, lighting, palette, shadows, vibes, assembly formula)
- Add to `/ranpin` mood pool
- Add to `skill_diversity.md` content buckets if applicable
- Log in `topic_history.json` equivalent for mood tracking

---

## 5. Mood Lifecycle Management

Moods aren't permanent. They have lifecycles:

| Stage | Signal | Action |
|-------|--------|--------|
| **EMERGING** | First detected, velocity rising, <2 weeks old | Scout: generate 3-5 test pins, measure early performance |
| **PEAK** | High velocity, cross-platform confirmed, high save rates | Exploit: heavy batch production, multi-character coverage |
| **SUSTAINED** | Velocity flattening but saves remain strong | Maintain: regular production at reduced cadence |
| **FADING** | Velocity declining, saves dropping | Wind down: stop new batches, existing pins remain as evergreen |
| **DORMANT** | No active signals, but periodic nostalgic revival possible | Archive: keep workflow file, don't delete, may resurface |

> **No mood workflow is ever deleted.** Dormant workflows stay in the system. Nostalgia cycles are real — a mood that faded 6 months ago may spike again.

---

## 6. Integration with Existing Modules

| Module | How Discovery Engine Connects |
|--------|-------------------------------|
| `skill.md` (Core) | Discovered moods use the same 5-Layer Formula, Visual Style Lock, and NB2 rules |
| `skill_characters.md` (Characters) | Characters are sourced via `DISCOVER_CHARACTERS()` — see `skill_roster_discovery.md` |
| `skill_growth.md` (Growth) | New environments/poses invented during discovery batches get auto-appended |
| `skill_trending.md` (Trending) | Discovery Engine extends trending intelligence beyond series-level to mood-level |
| `skill_diversity.md` (Diversity) | New moods create new content buckets for batch diversity |
| `skill_pfp.md` (PFP) | Discovered moods are rated for PFP suitability — see Mood-to-PFP mapping |
| `skill_merch.md` (Merch) | Discovered moods are rated for merchandise suitability — see Mood-to-Merch matrix |
