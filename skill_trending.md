---
name: PinGPT Trending Intelligence
description: How to interpret trending data, generate debate-bait carousel topics, write Gen-Z commentary, and ride waves for TikTok virality.
---

# Trending Content Intelligence

> **PURPOSE:** This skill teaches the LLM how to transform raw trending data into high-engagement TikTok carousel content. It bridges the gap between "what's trending" and "what to post."

## Trend Scoring

When interpreting `trending_report.json`, weight signals in this order:

1. **Currently Airing + High MAL Members** = PEAK signal (post within 24h of new episode)
2. **High MAL Score + Rising Members** = RISING signal (ride the wave before it crests)
3. **High Members but Not Airing** = WARM signal (evergreen content, post anytime)
4. **Low Members + Not Airing** = FADING signal (skip unless character is iconic)

> [!IMPORTANT]
> **PinGPT character match is the #1 filter.** A PEAK anime with zero PinGPT characters is useless. A WARM anime with 5 PinGPT characters is gold. Always prioritize topics where we have character DNA.

## Carousel Topic Generation

### The Debate Bait Formula

The highest-engagement TikTok carousels follow this pattern:
- **Provocative ranking** → drives "I disagree" comments
- **Specific to one series** → targets a fandom, not the general anime audience
- **5-10 entries** → enough to debate, not so many people lose interest

### Topic Quality Checklist

Before generating a topic, verify:
- [ ] Does the topic naturally produce debate? (If everyone agrees, it's boring)
- [ ] Are there at least 3 PinGPT characters available for the entries?
- [ ] Is the topic specific enough to trigger fandom loyalty?
- [ ] Would YOU stop scrolling to see the list?

## Gen-Z Commentary Voice

Every ranked entry needs a one-liner that sounds like it was written by a 19-year-old anime fan at 2AM:

**DO:**
- "NUN TO BE SAID FR SHE ALREADY WAS FIGHTING LIKE SHE LOST EVERYTHING"
- "WAITED 400 YEARS JUST TO FIGHT SUKUNA IT SHOULD NEVER GET THAT SERIOUS THO"
- "THE HONORED ONE. NUN MUCH TO SAY."
- "CARRIED THE ENTIRE ARC ON THEIR BACK AND STILL GOT DISRESPECTED"

**DON'T:**
- "This character demonstrated remarkable courage in battle"
- "A fan-favorite due to their complex narrative arc"
- "One of the strongest fighters in the series"

**Rules:**
- ALL CAPS always
- Use "FR", "NUN", "THO", "GOAT", "MID", "MENACE" naturally
- Max 2 lines per entry
- Bait disagreement — take a stance, don't be neutral
- Reference specific plot points fans will recognize

## Hybrid Art Style Decisions

For each slide in a carousel, the style should match the character's energy:

| Character Energy | Best Style | Overlay Font | Why |
|---|---|---|---|
| Peak action / power moment | `atmospheric` | **Bebas Neue** | Full color NB2 renders hit hardest, tall atmospheric display font |
| Emotional / tragic / raw | `manga_tint` | **Oswald** | Color-accented manga panels look premium + font amplifies mood |
| #1 pick / closer | `closer` | **Bangers** | Loud attention-grabbing font for the final CTA |
| Hook / cover | `cover` | **Bangers** | Color + bold impact font stops the scroll |

> [!CAUTION]
> **`manga_raw` (literal B&W) is DEPRECATED for TikTok carousels.** It produces uncolored, flat monochrome panels that look cheap alongside atmospheric slides. Use `manga_tint` instead — it keeps the manga panel energy but adds a color accent that pops. Reserve `manga_raw` ONLY if the user explicitly requests pure B&W.

### Model Selection Strategy

| Scenario | Model | Why |
|---|---|---|
| Default for all atmospheric + manga_tint prompts | **Nano Banana 2** | Best 2D cel-shaded output, proven quality |
| Prompt gets "termed" (policy violation) on NB2 | **NanoBanana Pro** | More permissive safety filter, handles edge-case prompts that NB2 rejects |
| Prompt fails 2+ times with "Something went wrong" | **NanoBanana Pro** | Different model path, avoids whatever NB2 is choking on |

> **NEVER waste more than 2 retries on NB2.** If a prompt fails twice on NB2, immediately switch to NB Pro and move on.

## Posting Window Strategy

| Trend Signal | When to Post | Why |
|---|---|---|
| PEAK | Within 24h of episode air | Fandom is most active, highest search volume |
| RISING | Same week as trend emergence | Ride the wave while it builds |
| WARM | Anytime (evergreen) | Consistent filler content between PEAK waves |
| FADING | Skip or repurpose | Low ROI unless the character is iconic enough to transcend the trend |

## TrendTok Prompt Guardrails (Hard-Learned from Batches 1-2)

> **🚨 These rules are NON-NEGOTIABLE for all TrendTok carousel prompts.** Derived from real generation failures across multiple JJK batches.

### BANNED in TrendTok Prompts

| Banned Pattern | Why It Fails | Safe Alternative |
|---|---|---|
| `"exit sign"`, `"signage"`, `"storefront"` | NB2 renders kanji/text ON the sign — auto-fails text check | `"neon glow strip"`, `"glowing panel (blank)"`, `"colored ambient light"` |
| `"blood"`, `"crimson liquid trailing"`, `"blood-spattered"` | NB2 renders literal gore + triggers mangled hand anatomy | `"dark energy wisps"`, `"cursed energy aura"`, `"faint crimson glow"` (never liquid) |
| `"exposed arms showing markings"` | "Exposed" + body part = safety flag risk | `"arms with visible dark markings through torn sleeve"` |
| Full-body action lunge (character fills entire frame vertically) | Full-body = leg/foot anatomy failures, NO negative space for text overlay | Frame from waist up, or knee-up crouch. Leave top 30% for overlay text |
| `"devastation"`, `"burning cityscape"` (when character is the subject) | Over-specifying destruction distracts from character composure | Focus destruction in background bokeh only, character occupies foreground calmly |
| `"dark robe open at the chest"` or any clothing-open-at-body phrasing | Policy violation — NB2 reads as exposure | `"dark kimono draped over broad shoulders"` (fully covered) |
| `"MANGA B and W STYLE"` as primary style directive | Produces literal uncolored B&W output that looks cheap in TikTok carousel context | Use `manga_tint` style with single color accent instead |

### TrendTok Framing Rules

1. **Lower 40% of frame = text overlay zone.** The overlay engine places text at center-bottom (60% down). Compose the character's face/torso in the upper-center of the frame with atmospheric space below for rank/title text. Do NOT push the character down — that puts them directly behind the overlay.
2. **Manga_tint slides use dual lighting but with ONE color accent.** Describe a single dominant color accent (crimson, teal, amber) bleeding into an otherwise muted/dark scene. This creates the manga-panel vibe with visual pop.

### Flow Submission Reliability Rules (Hard-Learned from Batch 2)

> **🚨 These rules prevent the mass "Something went wrong" cascade that killed 60% of batch 2 prompts.**

1. **BATCH SPLIT: Submit max 3-4 prompts at a time.** Rapid-fire 10+ prompts triggers Flow server-side rate limiting. Submit 3-4, wait 10 seconds, submit next batch.
2. **On failure: EXIT → RE-ENTER, don't retry in place.** The retry button on failed tiles almost never works. Navigate OUT of the project (back arrow), wait 3 seconds, navigate BACK in, then resubmit the failed prompt as a NEW submission.
3. **2-strike NB Pro rule.** If a prompt fails twice on NB2 (either "Something went wrong" or policy violation), immediately switch model to **NanoBanana Pro** and resubmit. Don't waste a third attempt on NB2.
4. **Verify settings persist after re-entering.** Aspect ratio (9:16) and multiplier (x1) sometimes reset when leaving and re-entering a project. Always confirm before resubmitting.

## Topic Diversity Rules (Anti-Repetition)

> **🚨 MANDATORY before picking a topic.** Without these rules, the LLM generates the same "Top X fighters" topic every single run regardless of model.

### Pre-Selection Checklist

1. **Read `topic_history.json`** — load all previously used topics. This file lives at the PinGPT root.
2. **Never reuse a topic** — even with slight rephrasing. "Top 10 strongest in JJK" and "Ranking the strongest JJK characters" are the **same** topic.
3. **Rotate across categories** — the 8 categories are:

   | Category | Examples |
   |---|---|
   | `power_scaling` | Strongest, broken abilities, 1v1 matchups |
   | `emotional` | Saddest backstory, heartbreaking deaths, sacrifices |
   | `hypothetical` | "What if" scenarios, rematch speculations |
   | `character_development` | Glow-ups, best arcs, wasted potential, mentors |
   | `legacy` | Iconic scenes, internet-breaking moments, entrances |
   | `design_aesthetic` | Best designs, coldest fits, transformations |
   | `comedy` | Funniest moments, unhinged characters, menace energy |
   | `villain` | Villains who were right, villain drip, threat level |

4. **Check which categories were used recently** — if the last 3 runs were all `power_scaling`, the next MUST be from a different category (emotional, hypothetical, comedy, etc.)

### Post-Selection

5. **Record the chosen topic** — after finalizing the carousel topic, write it to `topic_history.json`:
   ```javascript
   // In trend_fetch.js (already available):
   recordTopic("Top 8 villains who were actually right in JJK", "jjk", "gemini-2.5-pro");
   ```
   Or the LLM should instruct the pipeline to record it.

> [!TIP]
> **When the same series is run repeatedly** (e.g., 5 JJK runs in a row), category rotation is the ONLY way to keep content fresh. Power scaling → emotional → hypothetical → comedy → design. Never do power scaling twice in a row for the same series.

