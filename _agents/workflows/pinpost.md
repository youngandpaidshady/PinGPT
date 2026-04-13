---
description: Automate Pinterest pin posting — upload image from disk, fill title/description/hashtags, select board, and publish. Usage - /pinpost [batch_dir] [character]
---

# /pinpost — Full Pinterest Pin Upload & Publish

// turbo-all

> [!TIP]
> **For 5+ pins, use `/bulkpin` instead.** It bulk-uploads all pins via CSV with drip scheduling baked in — 100x faster and more reliable than one-by-one browser automation. Use `/pinpost` only for small batches (1-4 pins) or as a fallback.

## When to Use


Use `/pinpost` after you have downloaded images (from `/gemgen` or manually) AND have captions ready (from `/pincap`). This workflow automates the full posting flow — no manual uploads needed.

## Usage

```
/pinpost                     → schedule all images in output\gemgen_batch\ (drip-posted over 3-4 days)
/pinpost gojo                → schedule images, route to Gojo-related boards
/pinpost C:\path\to\images   → schedule images from a custom directory
/pinpost --now               → IMMEDIATELY publish all (USE ONLY if account has 1000+ followers)
```

## Prerequisites

- Images saved to disk (PNG/JPG, any resolution)
- Captions ready in `gemgen_queue.json` or passed inline
- Pinterest account logged in on Chrome (aaronbrian78)

> [!IMPORTANT]
> **Account Identity:** The Pinterest account `aaronbrian78` displays as **"PinCase"** (or "PinGPTbyXo") in the UI.
> These are ALL THE SAME ACCOUNT. If the browser shows you are logged into PinCase, **you are already on the correct account.**
> **DO NOT log out and re-login.** This wastes the entire session.

---

## Steps

### Step 1 — Prepare metadata

1. Read `gemgen_queue.json` for titles, descriptions, hashtags, alt text per image.
2. If no queue file exists, run `/pincap [character] [count]` first to generate captions.
3. Match images to captions by index (image 1 → caption 1, etc.).

### Step 1.5 — Build the drip schedule

> [!CAUTION]
> **NEVER publish all pins at once.** Mass-posting is the #1 shadowban trigger on Pinterest.
> Even 5 pins in 5 minutes on a low-trust account will get you suppressed.

Build a schedule that spaces pins **4+ hours apart, max 3 pins per day**:

```
Schedule Formula (for N pins):
- Day 1: Pin 1 at 09:00, Pin 2 at 14:00, Pin 3 at 19:00
- Day 2: Pin 4 at 10:00, Pin 5 at 15:00, Pin 6 at 20:00
- Day 3: Pin 7 at 11:00, Pin 8 at 16:00, Pin 9 at 21:00
- Day 4: Pin 10 at 09:00 (and so on...)
```

**Start Date:** Always schedule from TOMORROW (never today — today's burst already happened).
**Time Zone:** Use the user's local timezone. Current: UTC.
**Best Times:** 09:00-11:00, 14:00-16:00, 19:00-21:00 (peak Pinterest engagement windows).

For each pin, compute:
- `schedule_date`: YYYY-MM-DD
- `schedule_time`: HH:MM (24h format)

Embed these in the subagent task alongside captions.

### Step 2 — Launch browser subagent for posting

> **⚠️ CRITICAL:** Embed ALL image paths + captions directly in the subagent task.
> The subagent CANNOT read `gemgen_queue.json`.

Launch a `browser_subagent` with ALL image paths and captions embedded:

> **Task for subagent:**
>
> **For EACH pin (repeat for every image):**
>
> **A. Navigate to Pin creation:**
> 1. Go to `https://www.pinterest.com/pin-creation-tool/`
> 2. If not logged in, click "Log in" - select aaronbrian78 account.
> 3. **ACCOUNT CHECK:** If logged in as "PinCase", "PinGPTbyXo", or "aaronbrian78" - YOU ARE ON THE CORRECT ACCOUNT. DO NOT log out.
> 4. You should see the Pin creation form with "Drag and drop or click to upload".
>
> **B. Upload the image:**
> 1. Click the upload area ("Drag and drop or click to upload").
> 2. A file picker dialog will appear - this is handled by the `upload_file` browser tool.
> 3. Use the upload tool to select the image file from the absolute path provided below.
> 4. Wait for the image preview to appear in the form.
>
> **C. Fill in metadata:**
> 1. Click the "Title" field - type the pin title.
> 2. Click the "Tell everyone what your Pin is about" description field - type the description + hashtags.
> 3. Click the "Alt text" field (may need to expand "More options") - type the alt text.
> 4. Click the "Add a destination link" field - type the link if provided (optional).
>
> **D. Select board:**
> 1. Click the board selector dropdown (shows "Choose a board" or last used board).
> 2. Search for or select the appropriate board based on the Board Routing Rules below.
> 3. If the board doesn't exist, select "Anime Boys Aesthetic" as fallback.
>
> **E. Schedule (DRIP MODE - DEFAULT):**
> 1. Scroll down to find **"Publish at a later date"** toggle. Click it to enable.
> 2. A date and time picker will appear.
> 3. Set the **date** to the scheduled date provided for this pin.
> 4. Set the **time** to the scheduled time provided for this pin.
> 5. Click **"Publish"** (this saves it as a scheduled pin, NOT immediate).
> 6. Wait for confirmation.
>
> **E-ALT. Publish Immediately (--now MODE ONLY):**
> 1. Skip the schedule toggle.
> 2. Click the "Publish" button directly.
> 3. Wait for the "Your Pin has been published!" confirmation.
> 4. If a "Save to another board" option appears, pin to secondary board.
>
> **F. Next pin:**
> 1. Click "Create another Pin" or navigate back to the pin creation tool.
> 2. Repeat from Step B for the next image.
>
> **Pin to max 2 boards per image** (Pinterest penalizes over-pinning).
>
> **Here are the pins to post:**
> [PASTE ALL IMAGE PATHS + CAPTIONS + SCHEDULE TIMES HERE]
>
> ```
> PIN 1:
> Image: C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch\roofrain_1.png
> Title: ...
> Description: ...
> Alt text: ...
> Board: Jujutsu Kaisen Wallpapers
> Schedule: 2026-04-04 at 09:00
>
> PIN 2:
> Image: ...
> Schedule: 2026-04-04 at 14:00
> ...
> ```

### Step 3 — Verify published pins

After the subagent finishes:

1. **DO NOT trust the subagent's report blindly** — verify independently.
2. Launch a quick browser subagent to navigate to your Pinterest profile and count recent pins.
3. Cross-check: published pin count should match the number of images posted.

---

## Board Routing Rules

| Character / Mood | Primary Board | Secondary Board |
|-----------------|---------------|-----------------|
| Gojo, Toji, Megumi, Yuji | Jujutsu Kaisen Wallpapers | Anime Boys Aesthetic |
| Levi, Eren | Attack on Titan Art | Anime Boys Aesthetic |
| Sung Jinwoo | Solo Leveling Aesthetic | Anime Boys Aesthetic |
| Killua, Gon | Hunter x Hunter Art | Anime Boys Aesthetic |
| Dark/noir mood | Dark Anime Aesthetic | Anime Phone Wallpapers |
| Warm/cozy mood | Cozy Anime Vibes | Anime Phone Wallpapers |
| Best compositions | Anime Phone Wallpapers | — |

## ⚠️ Browser Automation Safety Rules

> [!CAUTION]
> These rules are NON-NEGOTIABLE when using the browser subagent to publish pins.

1. **NO NATIVE FILE PICKER UPLOADS (if drag-drop fails):** If the browser subagent's `upload_file` tool fails, do NOT attempt workarounds with the native OS file picker. Instruct the user to manually drag-and-drop images to create bulk drafts first, then use the subagent to fill metadata only.
2. **EXPLICIT WAITS:** Pinterest uses a complex React UI. The subagent MUST use explicit delays (minimum 2+ seconds) between clicking a field to focus it, verifying the cursor is active, typing the text, and clicking the next UI element. Otherwise, keystrokes will randomly drop.
3. **BOARD VERIFICATION:** The subagent MUST explicitly verify that the correct board is selected from the dropdown before clicking Publish. Read the board name text after selection to confirm.
4. **DRAFT MATCHING (CRITICAL):** You are strictly FORBIDDEN from using tiny UI thumbnails for visual matching, as this causes hallucinated miscaptions. You MUST read the default Title (which automatically inherits the original file name). If the file name is stripped, you MUST click into the draft to view the full resolution image before matching it against captions.
5. **POST-PUBLISH VERIFICATION:** After publishing all pins, independently verify by navigating to the Pinterest profile and counting recent pins. Do NOT trust the subagent's report blindly.

---

## Known Hurdles

| # | Hurdle | Fix |
|---|--------|-----|
| 1 | File upload dialog | Use the browser subagent's `upload_file` tool with the absolute image path |
| 2 | Board selector is a dropdown, not a page | Click the dropdown, then type to search for the board name |
| 3 | "More options" hides alt text | Click "More options" to expand the alt text field |
| 4 | Rate limiting | If Pinterest shows "Slow down", wait 30 seconds between pins |
| 5 | Max 2 boards per image | Pin to primary board on publish, then "Save to board" for secondary only |
| 6 | Subagent hallucination | Always verify published pin count on profile page after the run |
| 7 | PinCase ≠ aaronbrian78 confusion | Subagent sees "PinCase" display name and assumes it's the wrong account, wastes session logging out/in. **PinCase IS aaronbrian78.** Never log out if you see PinCase. |
| 8 | Mass-posting triggers shadowban | Posting 10+ pins in minutes flags the account as a spam bot. **ALWAYS use drip-posting** (3 pins/day, 4h apart). Only use `--now` on established accounts with 1000+ followers. |
| 9 | Emoji crashes Playwright | 🤍, 🔥 etc. cannot be typed via browser_press_key. Strip all emoji from descriptions before sending to subagent. |

---

## Posting Cadence Rules (Anti-Shadowban)

> [!CAUTION]
> These rules override all other posting logic. Violating them WILL trigger a shadowban.

| Rule | Limit |
|------|-------|
| Max pins per day | **15** (growth phase), **20** (established 1000+ followers) |
| Min gap between pins | **1 hour** |
| Max pins per board per day | **3** (diversity enforced) |
| Best posting windows (EST) | 6:00 AM - 10:00 PM (evenly spaced) |
| Max boards per pin | **2** (primary on publish, secondary via "Save to board") |
| Repin ratio | For every 3 own pins, save/repin **5** from others |
| Daily engagement | Follow 2-3 accounts, repin 5-10 pins from home feed |
