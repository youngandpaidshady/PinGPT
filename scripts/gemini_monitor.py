#!/usr/bin/env python3
"""
gemini_monitor.py — Send a message to Ask Gemini side panel via pyautogui.

Used by the agent to intervene when monitoring reveals issues.
NOT an automated loop — only called explicitly when the agent decides action is needed.

Usage:
    python scripts/gemini_monitor.py --send "retry prompt 5 with NanoBanana Pro"
    python scripts/gemini_monitor.py --send "you have my permission to download all files"
"""

import sys
import json
import time
import argparse
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
CONFIG_FILE = BASE_DIR / 'gemini_feeder_config.json'

pyautogui.FAILSAFE = True
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
    _lock()
    try:
        pyautogui.click(x, y)
    finally:
        _unlock()

def locked_hotkey(*keys):
    _lock()
    try:
        pyautogui.hotkey(*keys)
    finally:
        _unlock()

def locked_press(key):
    _lock()
    try:
        pyautogui.press(key)
    finally:
        _unlock()

def locked_paste(text):
    pyperclip.copy(text)
    _lock()
    try:
        pyautogui.hotkey('ctrl', 'v')
    finally:
        _unlock()


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
        user32.ShowWindow(hwnd, 3)
        time.sleep(0.5)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.5)
        return True
    return False


def send_message(message):
    """Focus Chrome, click Ask Gemini text box, paste message, send."""
    config = json.loads(CONFIG_FILE.read_text(encoding='utf-8')) if CONFIG_FILE.exists() else {}

    text_x = config.get('text_x')
    text_y = config.get('text_y')
    if text_x is None:
        print("Not calibrated. Run: python scripts/gemini_feeder.py --calibrate")
        sys.exit(1)

    # Focus Chrome
    if not maximize_chrome():
        print("Chrome not found!")
        sys.exit(1)
    time.sleep(0.5)

    # Switch to Flow tab (micro-locked)
    locked_hotkey('ctrl', '1')
    time.sleep(1)

    # Click Ask Gemini text box (micro-locked)
    locked_click(text_x, text_y)
    time.sleep(0.5)

    # Paste and send (micro-locked)
    locked_paste(message)
    time.sleep(1)
    locked_press('enter')

    print(f"Sent to Ask Gemini: {message[:80]}...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send', required=True, help='Message to send to Ask Gemini')
    args = parser.parse_args()
    send_message(args.send)


if __name__ == '__main__':
    main()
