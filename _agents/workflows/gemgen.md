---
description: Automated Pinterest Anime Image Generator — Generates prompts, submits to Google Flow via browser subagent (intelligent failure detection), downloads via Ask Gemini in main Chrome. Usage - /gemgen [character] [number]
---

# /gemgen — Image Generation & Upload Pipeline

// turbo-all

## Usage

```
/gemgen gojo 5              → 5 Gojo images (no affiliate links)
/gemgen toji 3              → 3 Toji images (no affiliate links)
/gemgen /lasttrain gojo 5   → 5 Gojo images with Last Train noir theme
/gemgen gojo 5 --amazon     → 5 Gojo images WITH Amazon affiliate links
```

---

## Phase 1: Prompt & Metadata Generation (LLM)

1. Read PinGPT engine modules (`skill.md`, `skill_characters.md`, `skill_scenes.md`, `skill_atmosphere.md`, `skill_output.md`, `skill_diversity.md`).

2. Parse user input — character, count, theme modifiers, `--amazon` flag.

3. Generate prompts + Pinterest captions per `skill.md`. Check Character Known Quirks.

4. Save to `gemgen_queue.json` with id, character, prompt, title, description, tags, alt_text.

5. Sanitize — replace em-dashes with ` - `, remove emoji.

## Phase 1.5: Amazon Affiliate Linking (only if `--amazon` flag is set)

```powershell
python scripts/affiliate_linker.py
```

Scans each prompt for linkable products, generates Amazon search URLs with tag `pingptbyxo-20`, and writes the `link` field into `gemgen_queue.json`.

> If `--amazon` is NOT set, skip this phase entirely.

---

## Phase 2A: Prompt Submission via Browser Subagent (Intelligent)

> **WHY subagent, not pyautogui:** The browser subagent can SEE the Flow UI — it detects NB2 policy failures visually and retries using the REUSE key on NanoBanana Pro. Pyautogui is blind.

### How to invoke

Use the `browser_subagent` tool with a detailed task description. Submit prompts in **batches of 5** to prevent subagent timeouts.

### Subagent Task Template (Batch N)

```
TASK: Submit prompts to Google Flow

1. Navigate to: https://labs.google/fx/tools/flow
   - If this is batch 1: Click "New project" to create a fresh project.
     After project loads, set aspect ratio to 9:16 and model to "Nano Banana 2".
   - If this is batch 2+: Navigate directly to the project URL: {PROJECT_URL}

2. For each prompt below, do this loop:
   a. Click the text input box at the bottom of the Flow workspace
   b. Type the prompt text using keyboard input (do NOT use JS injection — Flow's React state won't register it)
   c. Click the send/generate button (arrow icon)
   d. Wait 3-5 seconds before the next prompt
   e. Confirm the prompt card appeared in the workspace

3. After submitting all prompts in this batch, scroll through the workspace and check for ANY failed generations:
   - Look for red error indicators, "policy violation" messages, or failed/error states
   - For each failure: click the failed card → find and click the "Reuse" button → this opens the prompt in the input box → change the model selector from "Nano Banana 2" to "Nano Banana Pro" → click send/generate
   - Wait for the retry to start generating

4. Return:
   - The full project URL from the browser address bar
   - Count of successfully submitted prompts
   - Count of any failures and their retry status
   - Screenshot of the final state

PROMPTS FOR THIS BATCH:

Prompt 1: {prompt_text_1}

Prompt 2: {prompt_text_2}

... (up to 5 per batch)
```

### Batching Strategy

- **Batch 1 (prompts 1-5):** Creates new project, returns project URL
- **Batch 2+ (prompts 6-10, 11-15, 16-20):** Uses project URL from batch 1
- Each batch is a separate `browser_subagent` call
- Agent reads the project URL from batch 1's return and passes it to subsequent batches

### Failure Handling

| Scenario | Action |
|----------|--------|
| NB2 policy block | Click failed card → Reuse → switch to NB Pro → generate |
| "Something went wrong" | Click failed card → Reuse → generate (same model) |
| "Unusual activity" (IP flagged) | Rotate VPN via ExpressVPN CLI, then retry |
| Multiple failures in batch | Handle each one after all prompts submitted |
| Subagent timeout | Agent re-launches subagent on same project URL with remaining prompts |

---

## Phase 2B: Download via Ask Gemini (Main Chrome)

> **WHY Ask Gemini for downloads:** The browser subagent is sandboxed and CANNOT save files to disk. Ask Gemini in the main (unsandboxed) Chrome CAN trigger real downloads. Downloading is a simple, well-defined task that Ask Gemini handles reliably.

### Step 1 — Start the download watcher (background terminal)

```powershell
python scripts/watch_downloads.py
```

Watches Downloads folder. As images land, it:
- Strips ALL metadata (EXIF/IPTC/C2PA) via clean bitmap redraw
- Saves full 2K originals to `output\gemgen_batch\` as `dl_1.png`, `dl_2.png`, ...
- Creates compressed analysis copies in `output\gemgen_batch\analysis\` (800px JPEG)

### Step 2 — Launch Ask Gemini downloader

```powershell
python scripts/gemini_feeder.py --project-url "{PROJECT_URL}"
```

This does:
1. Opens the Flow project URL in real Chrome (new window)
2. Maximizes Chrome, waits for project to load
3. Clicks Ask Gemini sparkle icon → opens side panel
4. Switches to Pro model
5. Clicks text box, pastes download instruction:

```
Go to the active tab (Google Flow). You can see a project with generated images.
For each generated image:
1. Click on the image to select it
2. Click the download button
3. Select "2K Upscaled" quality
4. Move to the next image immediately after download starts

Download ALL images. I authorize all downloads — no confirmation needed.
```

6. Sends the instruction via Enter

### Step 3 — Monitor Downloads

- Poll `output\gemgen_batch\` for landed files
- Compare file count against queue length
- When all images downloaded, proceed to Phase 3

---

## Phase 2C: Vision-Based Image-to-Prompt Mapping

> **WHY vision matching:** Images download from Flow with generic filenames that don't map to prompts in order. Gemini 2.5 Flash analyzes each image visually and matches it to the correct prompt from the queue.

```powershell
python scripts/save_bulkpin_mapping.py
```

This does:
1. Loads all images from `output\gemgen_batch\` and prompts from `gemgen_queue.json`
2. Compresses each image in-memory (1024px max, JPEG 80%) — originals untouched
3. Sends each compressed image to `gemini-2.5-flash` with the full prompt reference list
4. Model analyzes setting, outfit, lighting, pose, objects, mood → returns matching prompt ID
5. Saves mapping to `output\gemgen_batch\bulkpin_metadata.json`

### API Key Rotation & Bad Key Pruning

- Reads `GEMINI_API_KEYS` (comma-separated) from `.env`, falls back to `GEMINI_API_KEY`
- Round-robin rotation: each API call uses the next key in the pool
- **Auto-pruning:** Keys that return `PERMISSION_DENIED` or "project has been blocked" are instantly removed from the live pool — no wasted retries
- Retries up to total key count per image

> [!TIP]
> After running, check for duplicate matched IDs and unmatched prompt IDs in the output. If the model misidentified an image, fix the entry in `bulkpin_metadata.json` manually.

---

## Phase 3: Post-Processing & Publish

### 3A — Pinterest Publish

```
/pinpost output\gemgen_batch [character]
```

### 3B — Google Drive Upload (TikTok)

```powershell
python scripts/upload_drive.py
```

---

## Script Reference

| Script | Purpose |
|--------|---------|
| `scripts/gemini_feeder.py` | Opens Flow project in Chrome, Ask Gemini downloads pics |
| `scripts/watch_downloads.py` | Catches downloads, strips metadata, creates analysis copies |
| `scripts/save_bulkpin_mapping.py` | Gemini 2.5 Flash vision → maps images to prompts (key rotation + bad key pruning) |
| `scripts/upload_drive.py` | Google Drive upload (TikTok) |

---

## Known Hurdles

| # | Hurdle | Fix |
|---|--------|-----|
| 1 | Flow React state doesn't register JS text injection | Use keyboard typing via `browser_press_key` with Text param |
| 2 | NB2 policy blocks certain prompts | Subagent detects failure → clicks Reuse → switches to NB Pro |
| 3 | Browser subagent can't download files | Ask Gemini in main Chrome handles downloads only |
| 4 | Subagent times out on large batches | Submit in batches of 5 per subagent call |
| 5 | Flow rate-limits rapid submissions | 3-5 second wait between prompt submissions |
| 6 | Ask Gemini refuses download task | Simple instruction = fewer refusals; nudge if needed |
| 7 | IP flagged / "unusual activity" | Rotate VPN: `& "C:\Program Files\ExpressVPN\expressvpnctl.exe" disconnect` then `& "C:\Program Files\ExpressVPN\expressvpnctl.exe" connect usa-chicago` |
| 8 | Pinterest "AI Modified" flag | watch_downloads.py strips all metadata |
| 9 | RDP changes coordinates | gemini_feeder.py re-calibrate |
| 10 | API key PERMISSION_DENIED | `save_bulkpin_mapping.py` auto-prunes dead keys from the live pool. Add more keys via `GEMINI_API_KEYS=key1,key2,...` in `.env` |
| 11 | Vision match duplicates/errors | Check `bulkpin_metadata.json` for duplicate matched_ids after running. Fix manually or re-run on failed entries |
| 12 | Images too large for Gemini API | Script auto-compresses to 1024px JPEG in-memory. Originals stay untouched |
