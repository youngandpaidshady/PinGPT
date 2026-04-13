---
name: PinGPT Growth & Performance Intelligence
description: Auto-expand living library system and Pinterest performance feedback loop.
---

# Auto-Expand Living Library

> **The engine doesn't just USE the libraries — it GROWS them.** Every batch generation is a discovery session. When you invent a new scene, outfit, pose, or lighting setup that isn't in the workflow tables, you MUST append it to the source file. After 50 batches, a 16-row environment table becomes 60+. The engine becomes its own content farm.

## How It Works

After generating EVERY batch, execute the **Library Growth Protocol**:

### Step 1: Invention Scan
For each prompt in the batch, check:
- Did I invent an environment NOT in the workflow's Environment Pool table? → **Capture it**
- Did I invent a pose NOT in the Pose Lock table? → **Capture it**
- Did I create an outfit variant NOT in the Outfit Lock table? → **Capture it**
- Did I create a lighting setup NOT in the Lighting Lock table? → **Capture it**
- Did I invent an emotional vibe NOT in the Vibe Tags table? → **Capture it**

### Step 2: Auto-Append
For each captured invention, append a new row to the corresponding table in the workflow `.md` file. Use the EXACT same format as existing rows. Number sequentially from the last entry.

**Format for appended entries:**
```
| [NEXT#] | [Scene Name] | [key details matching existing style] | <!-- AUTO-EXPAND: batch [date] -->
```

The `<!-- AUTO-EXPAND -->` comment marks it as engine-discovered vs hand-crafted. This enables future auditing.

### Step 3: Quality Gate
Only append inventions that pass the **Wallpaper Test** (Rule 5) AND the **Scroll-Stop Test** (Rule 7). Generic or weak inventions get discarded, not appended. The library should only grow with QUALITY — never bloat.

### Step 4: Cross-Pollination
If an invention from one workflow could work in another (e.g., a lighting setup invented in `/roofrain` that works for `/lasttrain`), append it to BOTH workflow files. Great ideas shouldn't be niche-locked.

## Auto-Expand Rules
1. **Never duplicate** — before appending, check the existing table for near-identical entries
2. **Match the voice** — appended entries must read identically to hand-crafted ones
3. **Cap per batch** — max 3 new entries per table per batch (prevents quality dilution)
4. **Caption DNA grows too** — new title patterns and description styles get appended
5. **Micro-details grow** — new character-specific or environment-specific micro-details get added
6. **New characters** — if a character not in the "Best Characters" table is used and works brilliantly, add them with a note on WHY

## Growth Metrics
Track the total library size in each workflow. The engine should report after each batch:
```
📊 Library Status:
   Environments: 16 base + 4 discovered = 20 total
   Outfits: 10 base + 2 discovered = 12 total
   Poses: 12 base + 1 discovered = 13 total
```

This makes library growth VISIBLE and motivating.

---

# Performance Intelligence — Pinterest Feedback Loop

> **The engine learns what YOUR audience saves.** Raw Pinterest analytics (saves, impressions, clicks, close-ups) flow back into the engine to weight future generation toward proven winners and away from underperformers.

## Performance Data Input

When performance data is available, feed it via the `/perfloop` command or manually. The engine accepts data in this format:

```
/perfloop [workflow] [data]

Example:
/perfloop lasttrain
Pin 1: saves=847, impressions=12400, clicks=234 — Nanami, Empty Subway Car, Drenched suit, Railing grip
Pin 2: saves=1203, impressions=18600, clicks=412 — Toji, Train Window Reflection, Leather jacket, Phone glow
Pin 3: saves=312, impressions=9800, clicks=89 — Levi, Station Stairwell, Vest Only, Walking away
```

## How the Engine Learns

### Tier 1: Element-Level Learning
The engine analyzes which individual elements correlate with high/low performance:

| Signal | Action |
|---|---|
| Environment with saves > 2x batch average | Mark with 🔥 in table, increase selection weight |
| Environment with saves < 0.5x batch average | Mark with ⚠️, investigate — is it the scene or the combo? |
| Character consistently outperforms in this workflow | Move up in priority ranking |
| Outfit variant drives disproportionate saves | Mark as 🔥, use more than the standard 60/40 signature split |
| Lighting setup underperforms | Review — possibly too subtle for Pinterest's small thumbnails |
| Specific vibe tag drives comments | Mark as engagement driver, use more frequently |

### Tier 2: Combo-Level Learning
Beyond individual elements, the engine tracks COMBINATIONS:

```
HIGH SAVE COMBOS (use more):
- Nanami + Ramen Counter + Tie Loosened + Warm Amber = 🔥🔥🔥
- Toji + Shirtless + Rain + Neon Bleed = 🔥🔥🔥

LOW SAVE COMBOS (avoid or remix):
- Levi + Station Stairwell + Vest = ⚠️ (scene too generic?)
```

### Tier 3: Trending Pattern Detection
The engine identifies macro patterns:

| Pattern | Example Insight |
|---|---|
| Time-of-day preference | "Your audience saves 2.3x more on midnight scenes vs 3AM fluorescent" |
| Character preference | "Nanami drives 40% of all saves in /closingtime" |
| Palette preference | "Warm amber palettes get 1.8x saves over cold blue in your account" |
| Composition preference | "Reflection-in-window compositions get 2.1x the save rate" |

### Tier 4: Audience Persona Building
Over time, the engine builds a model of YOUR specific audience:

```
🎯 AUDIENCE DNA (auto-updated):
- Responds strongest to: warmth-in-cold compositions, vulnerability moments, suited characters
- Saves most: Nanami, Toji, Gojo (in that order)
- Time peak: publishes at 10PM-12AM get most impressions
- Palette preference: warm amber > neon bleed > cold blue > fluorescent
- Top crossover communities: #literallyme, #darkaesthetic, #lonewolf
```

## Performance Tracking File

Pinterest performance data is stored in `performance_log.md` at the project root. This file is the engine's memory.

### Structure:
```markdown
## Performance Log

### [Date] — /[workflow] batch
| Pin | Character | Environment | Outfit | Saves | Impressions | Save Rate |
|-----|-----------|-------------|--------|-------|-------------|-----------|
| 1   | Nanami    | Ramen Counter | Tie Loosened | 847 | 12400 | 6.8% |

**Insights**: [auto-generated observations]
**Actions**: [changes made to workflow tables based on this data]
```

## Auto-Weight System

When sufficient data exists (20+ pins tracked), the engine automatically adjusts selection probabilities:

| Save Rate | Weight | Meaning |
|---|---|---|
| > 8% | 🔥🔥🔥 3x weight | Select 3x more often |
| 5-8% | 🔥 1.5x weight | Slight preference |
| 2-5% | Standard | Normal rotation |
| < 2% | ⚠️ 0.5x weight | Use less, investigate |
| < 1% | 🚫 Flag for review | Something's wrong — combo issue? |

## Business Intelligence Reports

The engine can generate periodic reports:

```
/perfloop report weekly
/perfloop report monthly
```

These reports include:
- Top 5 performing pins with element breakdowns
- Bottom 5 with failure hypotheses
- Audience growth trend
- Which workflows are driving the most saves
- Recommended next batch parameters based on data
- Hashtag performance (which crossover communities are converting)
