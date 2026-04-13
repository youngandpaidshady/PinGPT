---
name: PinGPT MoodMind Intelligence v2
description: LLM-powered mood evolution system — auto-generates Pinterest-viral aesthetic workflows with structural validation and templated assembly formulas.
---

# MoodMind v2 — Mood Evolution Engine

> **PURPOSE:** MoodMind transforms PinGPT from a fixed mood library into a self-evolving creative engine. v2 enforces 1M-impression quality standards — every concept must pass a Pinterest viability test, every workflow gets a proven assembly formula, and every output is structurally validated.

## How It Works

```
┌──────────────────────────────────────────────────────┐
│  MOODMIND v2 PIPELINE                                │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. SCAN       Read mood_registry.json for gaps      │
│       ↓                                              │
│  2. IDEATE     LLM generates concepts with           │
│       ↓        1M-Impression Test:                   │
│                • scroll-stop moment                  │
│                • atmospheric element                 │
│                • dual-lighting potential              │
│                • emotional universality              │
│  3. FILTER     Cyberpunk filter + kill list           │
│       ↓        (no dry architecture, no niche         │
│                hobbies, no activity-based concepts)   │
│  4. GENERATE   LLM writes DNA tables only            │
│       ↓        (envs, outfits, poses, lighting,      │
│                palette, shadows, vibes, captions)     │
│  5. VALIDATE   Structural checks on DNA:             │
│       ↓        20 envs, 10 outfits, 12 poses,       │
│                10 lights, 12 vibes, 12 characters    │
│                env names ≤5 words, cyberpunk-free    │
│  6. RETRY      If validation fails → regenerate      │
│       ↓        with issue feedback (1 retry max)     │
│  7. INJECT     Post-process: add standardized        │
│       ↓        frontmatter, title, steps, proven     │
│                assembly formula + self-check table   │
│  8. WRITE      Creates workflow .md file             │
│       ↓                                              │
│  9. REGISTER   Updates mood_registry.json            │
│       ↓        (uuid-based generation IDs)           │
│  10. INTEGRATE Appends to /ranpin mood pool          │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Usage

```bash
python moodmind.py                    # Ideate + generate 3 new moods
python moodmind.py --count 5          # Ideate 5 new moods
python moodmind.py --theme "coastal"  # Constrain to a theme
python moodmind.py --review           # Show registry stats
python moodmind.py --dry-run          # Preview without writing
```

Or via the agent workflow: `/moodmind`, `/moodmind 5`, `/moodmind coastal`

## Quality Gates (v2 — All Implemented)

### Ideation Phase
1. **1M-Impression Test** — scroll-stop moment, atmospheric element, dual lighting, emotional universality
2. **Kill List** — auto-rejects dry architecture, niche hobbies, activity-based, industrial, overly specific subcultures
3. **Cyberpunk Negative Filter** — no holographic UIs, circuit patterns, neon-dominant scenes, robots, chrome, glitch
4. **Slug Uniqueness** — no duplicate slugs against existing registry

### DNA Generation Phase
5. **Structural Validation** — verified table counts: 20 environments (≤5 words each), 10 outfits, 12 poses, 10 dual-source lighting setups, 4-5 palette entries, 5 shadows, 12 emotional vibes, 12 ranked characters, caption DNA with title patterns + hashtags + crossover tags
6. **Retry on Failure** — if validation fails, regenerates with issue feedback (1 retry)
7. **Cyberpunk Scan** — second pass on generated DNA content

### Post-Processing Phase
8. **Standardized Format** — title format (`# /slug — Name`), `// turbo-all`, Steps with full skill paths
9. **Proven Assembly Formula** — hardcoded 9-step formula from /sadboy with ❌/✅ examples and self-check table (never LLM-generated)
10. **Anti-Repetition Rules** — standardized batch-level diversity rules

## v2 vs v1 Differences

| Aspect | v1 | v2 |
|---|---|---|
| Assembly formula | LLM-generated (skeletal) | Hardcoded from /sadboy (proven, detailed) |
| Validation | None (keyword grep only) | Full structural parser (section counts, word limits) |
| Ideation quality | "Think about gaps" | 1M-Impression Test + Kill List |
| Post-processing | None | Inject frontmatter, title, steps, formula |
| Env count tracking | Broken (counted all table rows) | Section-aware parser |
| Generation IDs | List-length based (collisions) | UUID-based (unique) |
| Retry logic | None | Retry once with issue feedback |
| DNA prompt quality | Generic instructions | BAD/GOOD examples for every section |

## Mood Registry Schema

`mood_registry.json` tracks all moods:

| Field | Type | Description |
|---|---|---|
| `name` | string | Human-readable mood name |
| `slug` | string | Slash command / filename slug |
| `source` | enum | `"handcrafted"` or `"moodmind"` |
| `created` | date | ISO date string |
| `core_aesthetic` | string | One-sentence aesthetic DNA |
| `environment_count` | int | Number of environments in pool |
| `generation_id` | string | MoodMind generation ID (`mm_{date}_{uuid6}`) |
| `status` | enum | `"active"`, `"dormant"`, `"archived"` |

## Integration with Existing Modules

| Module | Connection |
|---|---|
| `skill.md` (Core) | Generated moods use all core rules (5-Layer Formula, NB2 rules, anti-repetition) |
| `skill_characters.md` | Generated moods include "Best Characters" tables sourced from the full roster |
| `skill_output.md` | Output format standardized via injected Steps section |
| `/ranpin` | New moods auto-register in the mood pool for random shuffling |

## Running MoodMind Periodically

Recommended cadence: **weekly or bi-weekly**. Each run generates 3-5 new moods.

After generation:
1. Review the new workflow `.md` files for quality
2. Test with a small batch: `/{new_mood} gojo 3`
3. If quality passes, the mood is production-ready
4. Run `/ranpin` to include new moods in shuffled batches
