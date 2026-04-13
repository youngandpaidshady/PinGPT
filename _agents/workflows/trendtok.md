---
description: Run the TrendTok pipeline — auto-discover trending anime topics, generate ranked tier-list TikTok carousels with text overlays, and upload to Google Drive. Usage - /trendtok [character] or /trendtok custom "topic"
---

# /trendtok — Trend-Driven TikTok Carousel Engine

// turbo-all

## Quick Run (One-Command Pipeline)

**Full autonomous pipeline** (VPN check → Flow project → submit → download → overlay → verify → upload):
```powershell
node scripts/trendtok_oneshot.js
```

**Skip modes:**
```powershell
node scripts/trendtok_oneshot.js --dry-run       # Phases 6-9 only (skip Flow)
node scripts/trendtok_oneshot.js --from-overlay   # Phases 7-9 only (images already downloaded)
node scripts/trendtok_oneshot.js --from-upload    # Phase 9 only (upload existing overlaid)
```

**Legacy pipeline** (overlay → preview → upload only):
```powershell
python scripts/pipeline.py --clean --preview --kill-stale
```

## The Vibe

**LLM-brained TikTok carousel factory.** The LLM IS the intelligence — it picks the topic, ranks characters from actual manga knowledge, writes Gen-Z commentary, and generates atmospheric NB2 prompts. Scripts only handle things the LLM can't: real-time API data and image processing.

## Usage

```
/trendtok jjk              → LLM picks debate-worthy JJK topic, ranks from manga feats, generates carousel
/trendtok aot              → Same for Attack on Titan
/trendtok                   → Full auto: LLM picks what's hot right now
/trendtok custom "Top 5 villains who were actually right" → You provide the topic
```

## Steps

### Phase 1 — Intelligence (LLM Brain)

> **The LLM handles: topic selection, character ranking, commentary, and prompt generation.**
> Scripts are NOT needed for this. The LLM already has deep knowledge of anime/manga feats, power scaling, and fan discourse.

1. **Read the PinGPT engine modules:**

```
View the file at C:\Users\Administrator\Desktop\PinGPT\skill.md
View the file at C:\Users\Administrator\Desktop\PinGPT\skill_characters.md
View the file at C:\Users\Administrator\Desktop\PinGPT\skill_trending.md
View the file at C:\Users\Administrator\Desktop\PinGPT\skill_output.md
```

2. **Load topic history** — read `topic_history.json` at PinGPT root to see what's been done before.

3. **Generate 10 topic suggestions** — whether a series was specified or not, present **exactly 10** diverse topics for user approval:

   - **If a series was specified** (e.g., `/trendtok jjk`): Skip `trend_fetch.js`. Use LLM manga knowledge + PinGPT character roster to generate 10 topics spread across different categories.
   - **If no series was specified** (full auto `/trendtok`): Optionally run `node scripts/trend_fetch.js` for seasonal data, then generate 10 topics.

   **Present topics in this format:**

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 TRENDTOK TOPIC SUGGESTIONS — [SERIES]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    #  │ Category              │ Topic
   ────┼───────────────────────┼──────────────────────────────────────
    1  │ 🗡️ power_scaling       │ Top 8 most broken abilities in JJK
    2  │ 😭 emotional           │ Characters who suffered the most in JJK
    3  │ 🤔 hypothetical        │ What if Toji never died in JJK
    4  │ 📈 character_dev       │ Top 8 characters with the best glow-up in JJK
    5  │ 🏛️ legacy              │ Top 10 entrances that gave you chills in JJK
    6  │ 🔥 design_aesthetic    │ Coldest fits in JJK
    7  │ 😈 villain             │ Ranking every villain in JJK by threat level
    8  │ 💀 comedy              │ Characters who chose violence for no reason in JJK
    9  │ 🗡️ power_scaling       │ 8 characters who would beat Gojo in a rematch
   10  │ 😭 emotional           │ Most heartbreaking deaths in JJK

   📜 Previously used: [N] topics in history (filtered out above)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Pick a number (1-10) or describe a custom topic:
   ```

   **Rules for topic suggestions:**
   - Every topic must be checked against `topic_history.json` — never suggest a previously used topic
   - Spread topics across ALL 8 categories (power_scaling, emotional, hypothetical, character_development, legacy, design_aesthetic, comedy, villain)
   - Max 2 topics from the same category
   - Cross-reference with PinGPT character roster — only suggest topics where we have enough characters

   > [!IMPORTANT]
   > **WAIT for user to pick a topic before proceeding.** Do NOT auto-select. Present the 10 options and ask the user to choose or provide a custom topic.

4. **After user selects a topic** — record it to `topic_history.json`, then proceed:
   - Rank characters based on actual feats, power scaling, and canon events
   - Cross-reference with PinGPT character roster for available characters

5. **Build the carousel deck** — the LLM generates `carousel_deck.json` directly:
   - **Topic**: Debate-bait title that triggers fan engagement
   - **Ranking**: Based on REAL manga feats, not guesses. Must be defensible but slightly spicy.
   - **Slide count**: 8-12 slides (cover + ranked entries + closer)
   - **Style rotation**: Alternate atmospheric / manga_raw / manga_tint / split_panel (see `skill_trending.md`)
   - **Commentary**: Gen-Z voice, ALL CAPS, debate-bait one-liners per entry
   - **TikTok caption + hashtags**

6. **Generate NB2 prompts** for each slide using PinGPT engine rules:
   - Each prompt follows the 5-Layer Formula from `skill.md`
   - Check ALL prompts against Safety Policy + TrendTok Prompt Guardrails in `skill_trending.md`
   - Save to `gemgen_queue.json`

> [!CAUTION]
> **BEFORE generating prompts, re-read the TrendTok Prompt Guardrails in `skill_trending.md`.** Banned: exit signs, blood/liquid FX, full-body poses on ranked slides, text-magnet objects. Every violation wastes a generation slot.

### Phase 2 — Image Generation

6. Feed all prompts into the `/gemgen` pipeline (Phase 2 onward from gemgen.md):
   - All prompts are 9:16 vertical portrait
   - Use the standard Flow → CDP → download pipeline
   - Images saved to `output\gemgen_batch\`

   > [!CAUTION]
   > **BATCH SPLIT (bare IP only — skip if VPN is active).** Without VPN, Flow rate-limits rapid-fire submissions. Submit in groups of **3-4 prompts**, wait **10 seconds** between groups. **With VPN on, submit all prompts back-to-back — no batching needed.**
   >
   > **On failure:** Do NOT click the retry button — it almost never works. Instead: EXIT the project (back arrow) → wait 3 seconds → RE-ENTER the project → resubmit the failed prompt as a NEW submission.
   >
   > **Termed prompts (policy violation):** Switch model to **NanoBanana Pro** in the settings pill and resubmit. NB Pro has a more permissive safety filter. Apply the 2-strike rule: if NB2 fails a prompt twice, go to NB Pro immediately.
   >
   > **Style note:** Do NOT use `manga_raw` (literal B&W) — it produces cheap uncolored panels. Use `manga_tint` (color-accented manga) or `atmospheric` instead.

   > [!WARNING]
   > **IP RATE-LIMITING — VPN ROTATION FIX.** Flow flags IPs that spam generations. If ALL prompts fail with "Something went wrong" (even simple test prompts on both NB2 and NB Pro), the IP is flagged.
   >
   > **Fix:** Rotate ExpressVPN to a fresh US location:
   > ```powershell
   > & "C:\Program Files\ExpressVPN\expressvpnctl.exe" disconnect
   > & "C:\Program Files\ExpressVPN\expressvpnctl.exe" connect usa-chicago   # or usa-dallas, usa-denver, etc.
   > & "C:\Program Files\ExpressVPN\expressvpnctl.exe" status               # verify connected
   > ```
   > After switching, create a **NEW project** and resubmit. The old project on the flagged IP is cursed.
   >
   > **Known good US locations:** `usa-chicago`, `usa-dallas`, `usa-denver`, `usa-seattle`, `usa-miami`
   > **Avoid:** `usa-new-york` (frequently flagged due to high traffic)

### Phase 3 — Text Overlays (v2.0 — Per-Style Fonts)

7. After images are downloaded, burn text overlays:

```powershell
node scripts/overlay_text.js
```

   This reads `carousel_deck.json` and the images in `output\gemgen_batch\`, applies text to each image with **style-mapped fonts and backgrounds**, and saves overlaid images to `output\gemgen_batch\overlaid\`.

   **Font Mapping (automatic — do NOT hardcode `"font": "Impact"` in deck JSON):**

   | Style | Font | Background |
   |-------|------|------------|
   | COVER / CLOSER | **Bangers** | Tight pill behind each line |
   | atmospheric | **Bebas Neue** | Subtle bottom fade gradient |
   | Manga B&W (`manga_raw`) | **Anton** | None (stroke-only for clean manga look) |
   | Manga Tint (`manga_tint`) | **Oswald** | Tight pill behind each line |

   > **⚠️ Do NOT set `"font": "Impact"` in `carousel_deck.json` slide specs.** The overlay engine auto-selects the font from the style. Only set `font` in spec if you want to override the default for a specific slide.

### Phase 3.5 — Compress Overlaid Images for Caption QA

> **⚠️ MANDATORY before any caption mismatch analysis.**
> Overlaid 2K PNGs are ~9MB+. Viewing all 10 in one conversation blows past the **30MB context limit**.

```powershell
node scripts/compress_images.js --dir overlaid --qa
```

Creates **≤300KB JPEG** analysis copies in `output\gemgen_batch\overlaid\analysis\`. The `--qa` flag targets 800px/JPEG-72 — just enough quality to verify character identity + text readability, while keeping 10 images under ~3MB total. When verifying caption-to-character matching, read from `overlaid/analysis/` — NOT the raw overlaid folder. Originals stay untouched for Drive upload.

### Phase 3.75 — Caption Mismatch Verification Gate (MANDATORY)

> [!CAUTION]
> **HARD GATE: DO NOT upload to Drive until EVERY slide passes this check.**
> Miscaptioned slides going to Drive = wasted content that has to be manually fixed.
> This step exists because `overlay_text.js` maps slides by index order, and any mismatch between image filenames, `carousel_deck.json` slide order, or download order will put the wrong text on the wrong character.

**Steps:**

1. **Read `carousel_deck.json`** — load the slide list with expected character + text per slide number.

2. **View EVERY compressed overlaid image** from `output\gemgen_batch\overlaid\analysis\`:
   - For each image, read it with `view_file` and verify:
     - **Character match:** Does the character in the image match the character specified in the deck for that slide number?
     - **Text match:** Does the burned-in text (rank number, name, commentary) match what's in `carousel_deck.json` for that slide?
     - **Readability:** Is the text legible (not obscured by the image composition)?

3. **Output a verification table:**

   ```
   | Slide | Expected Character | Expected Text       | Image Match | Text Match | Status |
   |-------|--------------------|---------------------|-------------|------------|--------|
   | 01    | Gojo               | "1. GOJO SATORU"    | ✅          | ✅         | PASS   |
   | 02    | Sukuna             | "2. RYOMEN SUKUNA"  | ✅          | ✅         | PASS   |
   | 03    | Toji               | "3. TOJI FUSHIGURO" | ❌ (Geto)   | ❌         | FAIL   |
   ```

4. **If ANY slide is FAIL:**
   - Identify the root cause (image order mismatch, wrong filename mapping, deck JSON error)
   - Fix: either re-order images in `output\gemgen_batch\` and re-run overlay, OR manually fix `carousel_deck.json` slide order
   - Re-run `node scripts/overlay_text.js`
   - Re-run `node scripts/compress_images.js --dir overlaid`
   - **Re-verify** — loop back to step 2 until ALL slides pass

5. **Only when ALL slides show PASS → proceed to Phase 4 (Drive upload).**

> [!WARNING]
> **Common mismatch causes:**
> - Download order ≠ generation order (Flow grid isn't always chronological)
> - `download_2k.js` skipped/retried an image, shifting all subsequent indices
> - Agent assumed filename order = slide order without verifying
>
> **Prevention:** After download, always verify image-to-prompt mapping by checking the visual content of each image against the prompt list BEFORE overlaying.

### Phase 4 — Upload to Drive (Python API SDK)

8. **Write a `tiktok_metadata.txt`** in `output\gemgen_batch\overlaid\` with:
   - Catchy viral hook title (NOT just the carousel topic)
   - Engaging TikTok caption with debate bait and emotional hooks
   - Curated hashtags (25 tags mixing broad + niche)
   - Sound suggestion with specific TikTok sound search terms
   - **Do NOT dump raw `gemgen_queue.json` fields** — write original, copy-paste-ready content

9. Upload the overlaid images + metadata to Google Drive:

```powershell
python scripts/upload_drive.py
```

   This uses the **Google Drive API SDK** (OAuth 2.0) to upload all `.png` files and `tiktok_metadata.txt` from `output\gemgen_batch\overlaid\` to the "Tiktok ready" folder.

   > **⚠️ DO NOT use Playwright/browser subagent for Drive uploads.** The CDP `fileChooser.setFiles()` method fails at 50MB+ payloads and the Drive UI blocks synthetic DOM file injection. The Python API SDK is the only stable path.

   - **First run:** Will open browser for OAuth consent (one "Allow" click). Saves `token.json` for future runs.
   - **Subsequent runs:** Silent, immediate uploads using saved token.
   - **Token expired?** Auto-refreshes via `refresh_token` in `token.json`.

### Phase 5 — Output Summary

9. Display the final summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 TRENDTOK CAROUSEL COMPLETE

TOPIC: [topic]
SLIDES: [count] | STYLE: Hybrid (atmospheric + manga)
SOURCE: LLM manga knowledge

📱 TIKTOK CAPTION:
[caption text]

🏷️ HASHTAGS:
[hashtags]

🎵 SOUND: [suggestion]

📁 FILES: output\gemgen_batch\overlaid\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Rules

- All images are **9:16 vertical portrait** (TikTok carousel format)
- Output is **PNG (lossless)** — TikTok compresses on upload, we deliver max quality
- **Hybrid style**: every carousel mixes atmospheric NB2 renders with manga-panel treatments
- Cover and closer slides are ALWAYS atmospheric (stop the scroll)
- Middle entries alternate between atmospheric, manga B&W, manga tinted, and split-panel
- Text overlays use **per-style fonts** (Bangers/Bebas Neue/Anton/Oswald), bold ALL CAPS, with black stroke for readability
- Same character must have IDENTICAL physical description across all their slides
- Commentary is punchy Gen-Z tone — bait debate, drive comments
- **Rankings must be based on actual manga feats** — not vibes, not guesses
- NO approval gates — full auto-fire from topic selection to upload
- **Read `skill_trending.md` TrendTok Prompt Guardrails** before generating any prompts

## What trend_fetch.js is for (and when to skip it)

| Scenario | Use trend_fetch.js? | Why |
|---|---|---|
| `/trendtok jjk` (series specified) | **NO** | LLM already knows JJK |
| `/trendtok` (full auto, no series) | **OPTIONAL** | LLM knows trends, but Jikan shows what's airing THIS season |
| Need real-time episode air dates | **YES** | Only Jikan has this week's schedule |
| Need MAL member counts | **YES** | Real-time popularity metrics |

## What carousel_planner.js is for (and when to skip it)

> `carousel_planner.js` handles structural scaffolding only (slide count, style rotation).
> The LLM can do this inline — the script is **optional** and exists as a convenience.
> **NEVER use carousel_planner.js for topic selection, character ranking, or commentary.**
