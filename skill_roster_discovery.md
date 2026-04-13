---
name: PinGPT Algorithmic Roster Discovery
description: Dynamic character sourcing via LLM knowledge query — no hardcoded lists. Characters are discovered per mood, cached on first use, and weighted by performance and freshness.
---

# Algorithmic Roster Discovery

> **The roster is NOT a list. It's a discovery function.** Characters are sourced dynamically per mood query using the LLM's own anime/manga knowledge + real-time trend signals. The existing Tier 1-2 roster in `skill_characters.md` becomes a **performance-weighted seed**, not a ceiling.

> [!IMPORTANT]
> **This module replaces the concept of "adding characters to PinGPT."** No character is ever manually added. They are discovered, generated, cached, and weighted — all at runtime.

---

## 1. Why Dynamic Roster

| Problem with Static Lists | Impact |
|--------------------------|--------|
| Audience fatigue | Same 6 characters dominate every batch — followers scroll past |
| Trend paralysis | Tuesday-viral character can't be used until someone edits a .md file |
| Mood-lock | Characters pre-assigned to moods → same combos forever |
| Discovery ceiling | LLM knows 10,000+ anime characters but pipeline hardcodes 22 |
| Genre bias | Static lists reflect curator's taste, not audience demand |

---

## 2. The Discovery Function

When ANY workflow needs characters, it uses the following query interface:

```
DISCOVER_CHARACTERS(mood, count, constraints)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `mood` | string | The current workflow vibe — e.g., `"/sadboy"`, `"organic melancholia"`, `"nostalgic cel-shade"` |
| `count` | integer | How many characters needed for this batch |
| `constraints` | object | Filtering and weighting rules (see below) |

### Constraint Options

```
constraints: {
  cyberpunk_filter:  true,          // REJECT characters coded as tech/cyber/mech
  series_diversity:  true,          // No 2 characters from the same series in one batch
  recency_boost:     0.3,          // 0.0-1.0 — weight toward currently-airing series
  obscurity_ratio:   "60/40",      // 60% recognizable names, 40% deep cuts
  gender_mix:        "any",         // "any", "male", "female", or "70/30" etc.
  exclude:           ["Gojo", ...], // Characters used in last N batches (from cache)
  visual_priority:   false          // If true, weight Visual Distinctiveness axis higher
}
```

### Default Constraints by Output Type

| Output Type | `recency_boost` | `obscurity_ratio` | `visual_priority` | Notes |
|------------|-----------------|-------------------|-------------------|-------|
| Pinterest Pin | 0.3 | 60/40 | false | Balanced — familiar names drive saves, deep cuts drive comments |
| TikTok PFP | 0.5 | 50/50 | true | PFPs need strong face rendering — visual distinctiveness matters more |
| Phone Case | 0.2 | 70/30 | true | Daily-use product — customers buy characters they recognize |
| Apparel | 0.3 | 60/40 | true | Streetwear audience values aesthetic over recognition |
| TikTok Carousel | 0.7 | 80/20 | false | Carousels need recognizable characters for debate engagement |

---

## 3. Character Evaluation Axes

The LLM evaluates every candidate character on 5 axes:

| Axis | Weight | Question | Scoring Guide |
|------|--------|----------|---------------|
| **Mood-Fit** | 30% | Does this character's canon emotional register match the current mood? | 10 = perfect emotional match. 5 = plausible stretch. 0 = complete mismatch |
| **Visual Distinctiveness** | 25% | Will NB2 render them recognizably with just 2-3 trait descriptors? | 10 = iconic look (white hair, scar, heterochromia). 5 = generic anime face. 0 = indistinguishable from others |
| **Trend Velocity** | 20% | Are they currently being discussed/searched/posted? | 10 = new episode this week. 5 = evergreen popular. 0 = forgotten/dormant |
| **Roster Freshness** | 15% | How recently were they used in PinGPT output? | 10 = never used or 30+ day gap. 5 = used 2-3 times this month. 0 = used 10+ times this month |
| **Surprise Factor** | 10% | Would fans be delighted/intrigued to see them in this mood? | 10 = unexpected but brilliant (Baki at a poetry reading). 5 = sensible choice. 0 = obvious/boring |

### Scoring Example

```
Query: DISCOVER_CHARACTERS("/sadboy", 5, {obscurity_ratio: "60/40"})

Candidate: Spike Spiegel (Cowboy Bebop)
  Mood-Fit:              9/10  — jazz loneliness, cigarettes, analog melancholy
  Visual Distinctiveness: 8/10  — green afro-ish hair, narrow eyes, cigarette
  Trend Velocity:         4/10  — evergreen, no active season
  Roster Freshness:      10/10  — never used in PinGPT
  Surprise Factor:        7/10  — classic choice but fresh for this pipeline

  COMPOSITE: (9×0.3) + (8×0.25) + (4×0.2) + (10×0.15) + (7×0.1) = 7.8 ✅ INCLUDE

Candidate: Kirito (SAO)
  Mood-Fit:              3/10  — main character energy, not melancholic
  Visual Distinctiveness: 4/10  — generic dark-hair anime protagonist
  Trend Velocity:         2/10  — no current activity
  Roster Freshness:      10/10  — never used
  Surprise Factor:        2/10  — feels forced, doesn't fit

  COMPOSITE: (3×0.3) + (4×0.25) + (2×0.2) + (10×0.15) + (2×0.1) = 4.0 ❌ REJECT
```

---

## 4. Visual DNA Cache

When a character is discovered for the FIRST time, the LLM generates their visual DNA on-the-fly and writes it to:

### File: `character_cache.json` (PinGPT root)

```json
{
  "spike_spiegel": {
    "added": "2026-04-09",
    "source_mood": "/sadboy",
    "series": "Cowboy Bebop",
    "visual_signature": "lean man with wild dark green-brown afro hair, narrow sharp lazy eyes, perpetual cigarette, easy confident slouch",
    "wardrobe": [
      "🔒 dark blue suit jacket, loosened yellow tie, wrinkled white shirt",
      "casual: rumpled white shirt, suspenders hanging loose at sides",
      "night: dark overcoat collar up, cigarette smoke trailing behind"
    ],
    "times_used": 0,
    "last_used": null,
    "save_rate": null,
    "quirks": [],
    "best_moods": ["/sadboy", "/alleysmoke", "/closingtime"],
    "cyberpunk_safe": true
  }
}
```

### Cache Rules

1. **Write AFTER first successful generation** — not before. The visual DNA is validated by successful NB2 rendering.
2. **LLM generates all fields from its own knowledge** — no manual data entry needed.
3. **Append-only** — never delete cache entries. Even failed experiments provide data.
4. **Quirks auto-update** — when a character-specific rendering issue is discovered (via the feedback loop in `skill_growth.md`), append to `quirks` array.
5. **`times_used` and `last_used` update after every batch** — this feeds the Exclusion Decay mechanism.
6. **`save_rate` populated when Pinterest data is available** — feeds back into performance weighting.
7. **`cyberpunk_safe` flag** — manually set to `false` if a character's default coding is too tech/cyber (e.g., Motoko Kusanagi, characters in mech suits).

### Cache Lookup Priority

When generating prompts for a character:

1. **Check `character_cache.json` first** — if the character has a cached entry, use it for visual consistency
2. **Check `skill_characters.md` Tier 1-2 roster** — proven performers with hand-crafted DNA (takes priority over cache if both exist)
3. **Generate fresh DNA** — if character is in neither source, LLM generates visual DNA from its own knowledge and writes to cache

---

## 5. Exclusion Decay (Anti-Fatigue Mechanism)

Characters naturally fade from rotation as they accumulate uses, then resurface after a cooling period:

| Usage Count (last 30 days) | Weight Modifier | Effect |
|---------------------------|----------------|--------|
| 0 (never used or 30+ day gap) | **1.0x** | Full weight — available for any batch |
| 1-2 uses | **0.8x** | Slight de-prioritization |
| 3-5 uses | **0.5x** | Noticeable fade — will be passed over for fresher options |
| 6-10 uses | **0.2x** | Strong suppression — only if they're a perfect mood fit |
| 10+ uses | **0.05x** | Near-zero — only used if explicitly requested by user |

### How It Works In Practice

```
Month 1: Gojo is fresh → 1.0x weight → appears in 8 batches
Month 2: Gojo at 8 uses → 0.2x weight → pipeline discovers Spike, Dazai
Month 3: Gojo at 0 uses (30-day reset) → 1.0x weight → resurfaces naturally
```

No manual intervention needed — the system self-balances.

---

## 6. The Tuesday Viral Test (Acid Test)

This is the scenario the dynamic roster MUST handle:

```
Timeline:
  2:00 PM Tuesday  — Random supporting character from niche manga 
                      goes viral on TikTok (unexpected meme/clip)
  2:05 PM          — Discovery Engine flags velocity spike in signals
  2:10 PM          — DISCOVER_CHARACTERS() evaluates the character:
                      Mood-Fit: 7   (surprisingly fits melancholy)
                      Visual:   8   (distinctive look)
                      Trend:   10   (VIRAL RIGHT NOW)
                      Fresh:   10   (never used)
                      Surprise: 9   (nobody expected this character here)
                      Score: 8.6 → INCLUDE
  2:15 PM          — LLM generates visual DNA from its own knowledge
  2:20 PM          — Prompt generated using /sadboy DNA + fresh character
  2:30 PM          — Image generated via /gemgen
  2:45 PM          — Visual DNA cached to character_cache.json
  3:00 PM          — Pin posted to Pinterest, PFP variant for TikTok
  
  Total: trend → posted in under 1 hour
  Static roster: would have taken DAYS of manual character research + .md edits
```

---

## 7. Integration Points

| Workflow | How It Uses DISCOVER_CHARACTERS() |
|----------|----------------------------------|
| `/ranpin` | Calls with random mood per prompt, `obscurity_ratio: "60/40"` |
| `/sadboy` | Calls with mood `"/sadboy"`, checks against Best Characters table first, then discovers fresh options |
| `/trendtok` | Calls with `recency_boost: 0.9` for maximum trend-riding |
| Any niche workflow | Calls with that workflow's mood, respects Best Characters table as seed |
| PFP batch | Calls with `visual_priority: true` for strong face rendering |
| Merch batch | Calls with `visual_priority: true`, `obscurity_ratio: "70/30"` for recognizable characters |

### Backward Compatibility

The existing Tier 1-2 roster in `skill_characters.md` is untouched. Those characters have:
- Hand-crafted visual DNA validated across hundreds of generations
- Known quirks and NB2 behavior documented
- Performance data from real Pinterest metrics

They function as the **performance-weighted seed** — always available, always high-quality. The dynamic roster EXTENDS beyond them, not replaces them. When a Tier 1-2 character is selected by `DISCOVER_CHARACTERS()`, the pipeline uses the hand-crafted DNA from `skill_characters.md`, not the cache.
