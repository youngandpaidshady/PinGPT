#!/usr/bin/env python3
"""
gemini_feeder.py — Ask Gemini download-only feeder for Google Flow.

Opens a Flow project in Chrome, activates Ask Gemini, and tells it to
download all generated images as 2K Upscaled.

Prompt submission is handled by the browser subagent (see gemgen.md Phase 2A).
This script only handles Phase 2B: downloading.

Usage:
    python scripts/gemini_feeder.py --calibrate          One-time: save coordinates
    python scripts/gemini_feeder.py --calibrate-model    Re-calibrate model points only
    python scripts/gemini_feeder.py --project-url URL    Download from Flow project
    python scripts/gemini_feeder.py --dry-run             Preview only
"""

import os, sys, json, time, argparse, subprocess
from pathlib import Path

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("Missing: pip install pyautogui pyperclip")
    sys.exit(1)

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).parent.parent
QUEUE_FILE = BASE_DIR / 'gemgen_queue.json'
CONFIG_FILE = BASE_DIR / 'gemini_feeder_config.json'
FLOW_URL = 'https://labs.google/fx/tools/flow'
CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.3


# --- Micro-lock helpers: lock input ONLY for the instant of each action ---
def _lock():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.BlockInput(True)

def _unlock():
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.BlockInput(False)

def locked_click(x, y):
    """Lock -> click -> unlock instantly."""
    _lock()
    try:
        pyautogui.click(x, y)
    finally:
        _unlock()

def locked_hotkey(*keys):
    """Lock -> hotkey -> unlock instantly."""
    _lock()
    try:
        pyautogui.hotkey(*keys)
    finally:
        _unlock()

def locked_press(key):
    """Lock -> press -> unlock instantly."""
    _lock()
    try:
        pyautogui.press(key)
    finally:
        _unlock()

def locked_paste(text):
    """Lock -> copy to clipboard + Ctrl+V -> unlock instantly."""
    pyperclip.copy(text)
    _lock()
    try:
        pyautogui.hotkey('ctrl', 'v')
    finally:
        _unlock()


DOWNLOAD_INSTRUCTION = """Go to the active tab (Google Flow project). You can see generated images.

For each generated image in the project:
1. Click on the image to select it
2. Click the download button
3. Select "2K Upscaled" quality
4. Move to the next image immediately after download starts

Download ALL images. I authorize all downloads — no confirmation needed.
Do NOT ask me before downloading. Just download every image."""


def load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
    return {}

def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding='utf-8')


def calibrate():
    """
    Calibrate click points on maximized Chrome.
    Agent sends Enter via send_command_input when user says ready.
    """
    print()
    print("=" * 55)
    print("  CALIBRATION (6 points)")
    print("=" * 55)

    maximize_chrome()
    time.sleep(2)

    config = load_config()

    # Point 1: Gemini icon
    print("\n  POINT 1: ASK GEMINI ICON")
    print("  -> Hover over the Gemini sparkle icon (top-right of Chrome)")
    input("  > ")
    x, y = pyautogui.position()
    config['icon_x'] = x
    config['icon_y'] = y
    print(f"  Saved: ({x}, {y})")

    print("\n  Now click the Gemini icon to open the panel.")

    # Point 2: Text box
    print("\n  POINT 2: ASK GEMINI TEXT BOX")
    print("  -> Hover over the text input at bottom of Gemini panel")
    input("  > ")
    x, y = pyautogui.position()
    config['text_x'] = x
    config['text_y'] = y
    print(f"  Saved: ({x}, {y})")

    # Point 3: Three-dot menu
    print("\n  POINT 3: THREE-DOT MENU")
    print("  -> Hover over the 3 vertical dots at top of Gemini panel")
    input("  > ")
    x, y = pyautogui.position()
    config['dots_x'] = x
    config['dots_y'] = y
    print(f"  Saved: ({x}, {y})")

    # Point 4: Continue chat in new tab
    print("\n  Now click the 3 dots to open the menu.")
    print("\n  POINT 4: CONTINUE CHAT IN NEW TAB")
    print("  -> Hover over 'Continue chat in new tab' menu item")
    input("  > ")
    x, y = pyautogui.position()
    config['continue_x'] = x
    config['continue_y'] = y
    print(f"  Saved: ({x}, {y})")

    # Point 5: Model dropdown (Fast/Pro toggle)
    print("\n  POINT 5: MODEL DROPDOWN")
    print("  -> Hover over the model selector (says 'Fast' or 'Pro')")
    input("  > ")
    x, y = pyautogui.position()
    config['model_dropdown_x'] = x
    config['model_dropdown_y'] = y
    print(f"  Saved: ({x}, {y})")

    # Point 6: Pro option
    print("\n  Now click the dropdown to open it.")
    print("\n  POINT 6: PRO OPTION")
    print("  -> Hover over the 'Pro' option in the dropdown")
    input("  > ")
    x, y = pyautogui.position()
    config['model_pro_x'] = x
    config['model_pro_y'] = y
    print(f"  Saved: ({x}, {y})")

    save_config(config)
    print(f"\n  Done! 6 points saved to {CONFIG_FILE.name}\n")


def maximize_chrome():
    """Find and maximize the REAL Google Chrome window (not Playwright/Chromium)."""
    import ctypes, ctypes.wintypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    hwnd = None

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def cb(h, _):
        nonlocal hwnd
        if user32.IsWindowVisible(h):
            buf = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(h, buf, 256)
            title = buf.value
            if 'Chrome' in title or 'Google' in title:
                # Verify it's the real chrome.exe, not chromium
                pid = ctypes.wintypes.DWORD()
                user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
                proc = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
                if proc:
                    exe_buf = ctypes.create_unicode_buffer(512)
                    size = ctypes.wintypes.DWORD(512)
                    kernel32.QueryFullProcessImageNameW(proc, 0, exe_buf, ctypes.byref(size))
                    kernel32.CloseHandle(proc)
                    exe_path = exe_buf.value.lower()
                    if 'chrome.exe' in exe_path and 'chromium' not in exe_path:
                        hwnd = h
                        return False
        return True

    user32.EnumWindows(cb, 0)
    if hwnd:
        user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
        time.sleep(0.5)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        print("  Chrome maximized.")
        return True
    print("  WARNING: Chrome not found.")
    return False


def open_chrome(url, profile_dir="Default"):
    """Open URL in a new Chrome window — isolates tab ordering."""
    print(f"  Opening {url} in new window (Profile: {profile_dir})...")
    try:
        subprocess.Popen([CHROME_PATH, f'--profile-directory={profile_dir}', '--new-window', url])
    except FileNotFoundError:
        subprocess.Popen(['chrome', f'--profile-directory={profile_dir}', '--new-window', url], shell=True)
    print("  Waiting 10s for project to load...")
    time.sleep(10)


def calibrate_model():
    """Calibrate only the 2 model switch points (dropdown + Pro option)."""
    print()
    print("=" * 55)
    print("  MODEL CALIBRATION (2 points)")
    print("=" * 55)

    maximize_chrome()
    time.sleep(2)

    config = load_config()

    # Point 5: Model dropdown
    print("\n  POINT 5: MODEL DROPDOWN")
    print("  -> Hover over the model selector (says 'Fast' or 'Pro')")
    input("  > ")
    x, y = pyautogui.position()
    config['model_dropdown_x'] = x
    config['model_dropdown_y'] = y
    print(f"  Saved: ({x}, {y})")

    # Point 6: Pro option
    print("\n  Now click the dropdown to open it.")
    print("\n  POINT 6: PRO OPTION")
    print("  -> Hover over the 'Pro' option in the dropdown")
    input("  > ")
    x, y = pyautogui.position()
    config['model_pro_x'] = x
    config['model_pro_y'] = y
    print(f"  Saved: ({x}, {y})")

    save_config(config)
    print(f"\n  Done! Model points saved to {CONFIG_FILE.name}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--calibrate', action='store_true')
    parser.add_argument('--calibrate-model', action='store_true')
    parser.add_argument('--project-url', type=str, help='Flow project URL to download from')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.calibrate:
        calibrate()
        return

    if args.calibrate_model:
        calibrate_model()
        return

    if not args.project_url:
        print("  ERROR: --project-url is required.")
        print("  Usage: python scripts/gemini_feeder.py --project-url <URL>")
        sys.exit(1)

    project_url = args.project_url

    if args.dry_run:
        print(f"\n  DRY RUN")
        print(f"  Project URL: {project_url}")
        print(f"\n  Download instruction:\n{DOWNLOAD_INSTRUCTION}")
        return

    config = load_config()
    if 'icon_x' not in config:
        print("  Not calibrated! Run: python scripts/gemini_feeder.py --calibrate")
        sys.exit(1)

    profile_dir = config.get('profile_directory', 'Default')

    # Open Chrome to the Flow project
    open_chrome(project_url, profile_dir)

    # Maximize + focus Chrome
    maximize_chrome()
    time.sleep(2)

    # Click Gemini icon (micro-locked)
    print(f"  Clicking Gemini icon ({config['icon_x']}, {config['icon_y']})...")
    locked_click(config['icon_x'], config['icon_y'])
    print("  Waiting 15s for Gemini panel to load...")
    time.sleep(15)

    # Switch to Pro model (micro-locked)
    if 'model_dropdown_x' in config and 'model_pro_x' in config:
        print("  Switching to Pro model...")
        locked_click(config['model_dropdown_x'], config['model_dropdown_y'])
        time.sleep(1)
        locked_click(config['model_pro_x'], config['model_pro_y'])
        time.sleep(1)
        print("  Pro model selected.")

    # Click text box (micro-locked)
    print(f"  Clicking text box ({config['text_x']}, {config['text_y']})...")
    locked_click(config['text_x'], config['text_y'])
    time.sleep(0.5)

    # Paste download instruction + send
    print(f"  Pasting download instruction ({len(DOWNLOAD_INSTRUCTION)} chars)...")
    locked_paste(DOWNLOAD_INSTRUCTION)
    time.sleep(2)
    locked_press('enter')

    print(f"\n  SENT download instruction to Ask Gemini.")
    print(f"  Project: {project_url}")
    print(f"  Run watch_downloads.py to catch downloads.\n")


if __name__ == '__main__':
    main()
