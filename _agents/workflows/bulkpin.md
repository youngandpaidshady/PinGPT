---
description: Bulk upload pins to Pinterest with drip scheduling via CSV. Replaces one-by-one browser pinpost. Usage - /bulkpin or /bulkpin --now
---

# /bulkpin — Bulk Upload Pins with Drip Scheduling

// turbo-all

## When to Use

Use `/bulkpin` when you have 5+ images ready to post and want to schedule them all at once instead of the slow one-by-one `/pinpost` flow. This uses Pinterest's native bulk CSV upload with built-in drip scheduling.

## Usage

```
/bulkpin                     → upload all images in output\gemgen_batch\ (drip-posted over 3-4 days)
/bulkpin --now               → publish all immediately (USE ONLY if account has 1000+ followers)
/bulkpin --per-day 5         → 5 pins per day (for established accounts)
/bulkpin --start "2026-04-10" → start scheduling from a specific date
```

## Prerequisites

- Images saved to disk (PNG/JPG) in `output\gemgen_batch\`
- Captions ready in `gemgen_queue.json` (run `/pincap` first if needed)
- Pinterest business account logged in on Chrome (aaronbrian78 / PinCase)
- Google Drive OAuth token (`token.json`) — first run will prompt for auth

> [!IMPORTANT]
> **Account Identity:** The Pinterest account `aaronbrian78` displays as **"PinCase"** (or "PinGPTbyXo") in the UI.
> These are ALL THE SAME ACCOUNT. If the browser shows PinCase, **you are on the correct account.**

---

## Steps

### Step 0 — Map images to prompts (Gemini 2.5 Flash vision)

> **REQUIRED** if images were downloaded from Flow with generic filenames.

```powershell
python scripts/save_bulkpin_mapping.py
```

Sends each image to Gemini 2.5 Flash (compressed in-memory, originals untouched) which visually matches it to the correct prompt from `gemgen_queue.json`. Outputs `bulkpin_metadata.json`.

**Key rotation:** Uses `GEMINI_API_KEYS` (comma-separated) from `.env`. Dead keys (PERMISSION_DENIED) are auto-pruned from the live pool.

**Verify:** Check output for duplicate matched IDs or unmatched prompts. Fix manually if needed.

### Step 1 — Strip metadata & Upload to public Drive folder

First, strip all AI and EXIF metadata from the images to prevent Pinterest's filters from flagging them. Then upload them to Google Drive with public sharing enabled.

```powershell
powershell scripts\strip.ps1
python scripts/upload_drive.py --pinterest
```

This will:
- Create/reuse a "Pinterest Bulk" folder in Drive
- Upload all PNG/JPG images
- Set each file to "anyone with link can view"
- Save URL mapping to `pinterest_urls.json`

**Verify:** Check the sample URL printed at the end — paste it in a browser to confirm the image loads.

### Step 2 — Generate the bulk CSV

Build the Pinterest-compatible CSV with metadata + drip schedule:

```powershell
node scripts/build_bulk_csv.js
```

Optional flags:
- `--now` — no scheduling, publish immediately
- `--per-day 5` — increase daily pin limit (established accounts only)
- `--start "YYYY-MM-DD"` — custom start date

**Output:** `output\pinterest_bulk.csv`.

**Verify:** Open the CSV and confirm:
- Every row has a valid `Media URL` (direct Drive link starting with `https://lh3.googleusercontent.com/d/`)
- `Publish date` column shows future dates in `YYYY-MM-DD HH:MM:SS` format (**NOT** ISO 8601 with `T`)
- **All titles are unique** — no two rows share the same `Title` value
- `Pinterest board` names match your actual Pinterest boards
- No emoji in descriptions

### Step 3 — Upload CSV to Pinterest (pyautogui)

> **WHY pyautogui, not browser subagent:** The browser subagent is sandboxed and CANNOT interact with native OS file dialogs. `upload_file` and `browser_set_file_input_files` are not available tools. Pyautogui can bring Chrome to the foreground, click the upload zone, and type the file path into the Windows Open dialog.

```python
python -c "
import pyautogui, time, ctypes, subprocess

user32 = ctypes.windll.user32

# 1. Open the bulk create page in Chrome
subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe',
                   'https://www.pinterest.com/settings/bulk-create-pins/'])
time.sleep(5)

# 2. Find and bring Chrome to foreground
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
chrome_hwnd = None
def find_chrome(hwnd, _):
    global chrome_hwnd
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if 'Pinterest' in buff.value or 'Google Chrome' in buff.value:
            chrome_hwnd = hwnd
    return True
user32.EnumWindows(EnumWindowsProc(find_chrome), 0)
user32.ShowWindow(chrome_hwnd, 9)  # SW_RESTORE
time.sleep(0.5)
user32.SetForegroundWindow(chrome_hwnd)
time.sleep(1)

# 3. Click the CSV upload zone (center of 'Drop your .csv file here')
pyautogui.click(440, 375)
time.sleep(3)

# 4. Find and focus the Open file dialog
dialog_hwnd = None
def find_dialog(hwnd, _):
    global dialog_hwnd
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if buff.value.strip() == 'Open':
            dialog_hwnd = hwnd
    return True
user32.EnumWindows(EnumWindowsProc(find_dialog), 0)
user32.SetForegroundWindow(dialog_hwnd)
time.sleep(1)

# 5. Type the CSV path into the filename field
pyautogui.hotkey('alt', 'n')  # Focus filename field
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.typewrite(r'C:\Users\Administrator\Desktop\PinGPT\output\pinterest_bulk.csv', interval=0.01)
time.sleep(0.5)
pyautogui.press('enter')
print('CSV submitted — check Pinterest for Upload successful dialog')
"
```

**Expected result:** Pinterest shows "Upload successful — Your Pins are being created. This usually takes about 2 hours."

> [!CAUTION]
> The click coordinates (440, 375) assume an 816x1544 screen with Chrome maximized. If the RDP resolution changes, re-screenshot and adjust coordinates.

> [!CAUTION]
> If the upload fails due to image URLs not loading, this means Google Drive URLs are being blocked by Pinterest. Fall back to `/pinpost` for this batch and report the error.

### Step 4 — Verify scheduled pins

After the CSV upload completes:

1. Launch a quick browser subagent to navigate to your Pinterest profile.
2. Check the scheduled pins section — verify pin count matches the number in the CSV.
3. Spot-check 2-3 pins to confirm titles and descriptions are correct.

---

## Anti-Shadowban Rules

These rules are already baked into the CSV schedule, but verify they hold:

| Rule | Limit |
|------|-------|
| Max pins per day | **15** (growth phase), **20** (established 1000+ followers) |
| Min gap between pins | **1 hour** (EST-based timing with jitter) |
| Max pins per board per day | **3** (diversity enforced by scheduler) |
| Best posting windows (EST) | 6:00 AM - 10:00 PM (evenly spaced) |
| Max boards per pin | **1** (bulk CSV only supports primary board) |
| Smart shuffle | Character + board interleaving (never same back-to-back) |
| Batch memory | Auto-reads last scheduled date from previous CSV |

---

## Comparison: /bulkpin vs /pinpost

| Feature | /bulkpin (CSV) | /pinpost (Browser) |
|---------|---------------|-------------------|
| Speed | ~2 min total | ~40 min for 20 pins |
| Reliability | High (CSV upload) | Medium (subagent can fail) |
| Scheduling | Built into CSV | Manual toggle per pin |
| Max pins/batch | 200 | ~20 (before timeout) |
| Image source | Public URLs required | Local files |
| Board routing | Single board per pin | Can pin to 2 boards |
| Emoji support | Strip before CSV | Strip before typing |
| Fallback | /pinpost | Manual upload |

---

## Known Hurdles

| # | Hurdle | Fix |
|---|--------|-----|
| 1 | Pinterest rejects Drive URLs | Try `lh3.googleusercontent.com/d/FILE_ID` (direct image proxy). If still blocked, use alternative host. |
| 2 | CSV column names wrong | Download Pinterest's sample CSV from settings page and match headers exactly. |
| 3 | Boards don't exist | Create boards on Pinterest BEFORE bulk upload. CSV won't create boards. |
| 4 | Schedule dates in the past | Always start from tomorrow. Script defaults to tomorrow automatically. |
| 5 | Too many pins per day | Default is 3/day. Only increase with `--per-day` for established accounts. |
| 6 | Images too large | Pinterest prefers < 20MB. Our 2K PNGs are ~9MB which is fine. |
| 7 | PinCase ≠ aaronbrian78 confusion | PinCase IS aaronbrian78. Never log out if you see PinCase. |
| 8 | **Duplicate titles rejected** | Pinterest CSV upload rejects batches with identical `Title` values. `build_bulk_csv.js` auto-deduplicates by appending ` (2)`, ` (3)` etc. If generating prompts with repeated characters, ensure unique titles at prompt time. |
| 9 | **ISO date `T` separator rejected** | Pinterest requires `Publish date` as `YYYY-MM-DD HH:MM:SS` (space separator). ISO 8601 `T` separator (`2026-04-08T09:00:00`) causes a generic "formatting error." Fixed in `build_bulk_csv.js`. |
| 10 | **URL path mismatch** | `upload_drive.py` saves `pinterest_urls.json` to project root, but `build_bulk_csv.js` previously looked in `output/`. Both now read from project root. |

---

## Quick Reference

```powershell
# Full flow — 5 commands:
python scripts/save_bulkpin_mapping.py             # Vision-match images → prompts (Gemini 2.5 Flash, key rotation)
powershell scripts\strip.ps1                       # Strip AI metadata
python scripts/upload_drive.py --pinterest         # Upload images → public URLs
node scripts/build_bulk_csv.js                     # Generate scheduled CSV
# Then browser subagent uploads pinterest_bulk.csv to Pinterest
```
