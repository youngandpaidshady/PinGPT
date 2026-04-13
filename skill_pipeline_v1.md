---
name: PinGPT Aesthetic Discovery Pipeline v1
description: Full pipeline orchestration — ties Discovery Engine, Asset Translation, and Roster Discovery into a single production loop with V1 self-critique and V2 iteration targets.
---

# Aesthetic Discovery Pipeline v1 — Orchestration

> **This is the conductor.** It doesn't generate anything itself — it orchestrates the flow between discovery, roster selection, prompt generation, asset forking, and performance feedback.

---

## Pipeline Flow

```
┌──────────────────────────────────────────────────────────────┐
│                AESTHETIC DISCOVERY PIPELINE v1                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐    ┌───────────┐    ┌──────────┐               │
│  │  SCAN   │───▶│  CLUSTER  │───▶│  FILTER  │               │
│  │ 5 sources│    │ by visual │    │ cyberpunk│               │
│  └─────────┘    │ similarity│    │ negative │               │
│                 └───────────┘    └────┬─────┘               │
│                                      │                      │
│                              ┌───────▼───────┐              │
│                              │  SCORE & NAME  │              │
│                              │  novelty×vel   │              │
│                              └───────┬───────┘              │
│                                      │                      │
│                          ┌───────────▼───────────┐          │
│                    ┌─────┤    NEW MOOD?           ├────┐     │
│                    │ YES └───────────────────────┘ NO │     │
│                    │                                  │     │
│             ┌──────▼──────┐                ┌─────────▼──┐  │
│             │ Create .md  │                │ Weight     │  │
│             │ workflow    │                │ existing   │  │
│             │ + add to    │                │ mood pool  │  │
│             │ /ranpin     │                └─────────┬──┘  │
│             └──────┬──────┘                          │     │
│                    │                                  │     │
│                    └──────────────┬───────────────────┘     │
│                                  │                          │
│                      ┌───────────▼───────────┐              │
│                      │  DISCOVER_CHARACTERS() │              │
│                      │  mood × constraints    │              │
│                      └───────────┬───────────┘              │
│                                  │                          │
│                      ┌───────────▼───────────┐              │
│                      │     ASSET FORK        │              │
│                      ├───────┬───────┬───────┤              │
│                      │ 9:16  │ 1:1   │ Merch │              │
│                      │ PIN   │ PFP   │ Case/ │              │
│                      │       │       │ Tee   │              │
│                      └───┬───┴───┬───┴───┬───┘              │
│                          │       │       │                   │
│                      ┌───▼───────▼───────▼───┐              │
│                      │    /gemgen PIPELINE    │              │
│                      │   generate + overlay   │              │
│                      └───────────┬───────────┘              │
│                                  │                          │
│                      ┌───────────▼───────────┐              │
│                      │  PERFORMANCE TRACKING  │──── loop ──▶│
│                      │  saves, impressions    │     back    │
│                      └───────────────────────┘     to SCAN  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Module Dependencies

| When Running... | Load These Modules |
|----------------|-------------------|
| **Weekly Discovery Scan** | `skill_discovery.md` |
| **Any Prompt Generation** | `skill.md` + `skill_characters.md` + `skill_output.md` + `skill_roster_discovery.md` |
| **Pinterest Pin Batch** | Above + mood workflow `.md` + `skill_diversity.md` |
| **PFP Batch** | Above + `skill_pfp.md` |
| **Merch Batch** | Above + `skill_merch.md` |
| **TikTok Carousel** | Above + `skill_tiktok.md` + `skill_trending.md` |
| **Performance Review** | `skill_growth.md` + `skill_discovery.md` (for mood lifecycle updates) |

---

## Asset Fork Decision Matrix

When a mood is ready for production, decide which output formats to produce:

| Mood Stage | Pinterest 9:16 | TikTok PFP 1:1 | Phone Case | Apparel | TikTok Carousel |
|-----------|---------------|----------------|-----------|---------|----------------|
| EMERGING (testing) | ✅ 3-5 test pins | ⬜ Skip | ⬜ Skip | ⬜ Skip | ⬜ Skip |
| PEAK (exploit) | ✅ Full batch (10-20) | ✅ PFP set (5-8) | ✅ 3-5 designs | ⬜ Skip until validated | ✅ If character-driven |
| SUSTAINED | ✅ Regular (5-10) | ✅ Refresh set | ⬜ Restock if selling | ✅ Launch if demand proven | ✅ Evergreen topics |
| FADING | ⬜ Stop new | ⬜ Stop new | ⬜ Stop new | ⬜ Stop new | ⬜ Stop new |

---

## V1 Self-Critique

> **Honest assessment of what V1 can and can't do.**

### What V1 Does Well

| Strength | Why |
|----------|-----|
| Mood taxonomy is comprehensive | 12 markers + 3 new workflows cover the organic/grounded aesthetic space well |
| Cyberpunk filter is clear and actionable | Specific banned markers with specific alternatives — no ambiguity |
| Character discovery is genuinely dynamic | LLM knowledge base has 10,000+ characters ready to query |
| Asset fork is well-defined | Clear rules for adapting any mood to pin, PFP, or merch |
| Backward compatible | Existing Tier 1-2 roster and all 16 mood workflows remain functional |

### What V1 Does Poorly

| Weakness | Impact | V2 Fix |
|----------|--------|--------|
| **Signal sources are conceptual** — no API integration for Pinterest/TikTok trend scanning | Discovery relies on LLM intuition + manual scanning, not live data | Build `trend_discover.js` — scrape Pinterest autocomplete + TikTok Creative Center programmatically |
| **Merch prompts are untested with NB2** — transparent backgrounds and gradient-only scenes are new territory | Phone case and apparel output may not render correctly | Run a 10-prompt validation batch across all merch types before production |
| **PFP 1:1 square is untested** — NB2 is trained on 9:16 predominantly | Square composition quality unknown | Run 5 PFP test prompts, compare output to 9:16 baselines |
| **Visual DNA consistency depends on cache discipline** — if cache isn't updated after batches, decay mechanism breaks | Fatigue prevention becomes theoretical, not practical | Integrate cache update into post-run hooks of `/gemgen` and `/pinpost` |
| **Weekly scan cadence is manual** — no scheduled automation | Scans will be skipped when busy with production | V2: automate scan triggers, even if evaluation stays LLM-driven |
| **No A/B testing framework** — can't systematically compare mood variants | Decisions on mood weighting are instinct-driven | V2: build split-test logic into `/bulkpin` to measure variant performance |
| **Merch has no sales feedback loop** — performance tracking only covers Pinterest saves | No way to know which phone case designs actually sell | V2: integrate print-on-demand platform sales data (Printify/Spring API) |

### V1 → V2 Priority Stack

| Priority | V2 Enhancement | Estimated Effort |
|----------|---------------|-----------------|
| 1 | Validate merch and PFP output quality with NB2 | 1 session (10-15 test prompts) |
| 2 | Build Pinterest autocomplete scraper into `trend_discover.js` | 2-3 hours |
| 3 | Automate `character_cache.json` updates in post-batch hooks | 1 hour |
| 4 | Build TikTok Creative Center hashtag scanner | 2-3 hours |
| 5 | A/B testing framework for mood variants | 4-5 hours |
| 6 | Print-on-demand sales API integration | Full project |

---

## Quick-Start Commands

| What You Want | Command |
|---------------|---------|
| Discover new moods | Read `skill_discovery.md`, run weekly scan workflow |
| Generate pins from a mood | `/ranpin`, `/sadboy`, or any mood workflow |
| Generate PFP set | Load `skill_pfp.md` + mood workflow, use PFP template |
| Generate merch designs | Load `skill_merch.md`, use product-specific template |
| Discover fresh characters | Pipeline auto-calls `DISCOVER_CHARACTERS()` — see `skill_roster_discovery.md` |
| Check character fatigue | Read `character_cache.json`, check `times_used` / `last_used` |
| Review mood lifecycle | Check signal velocity against lifecycle stages in `skill_discovery.md` §5 |
