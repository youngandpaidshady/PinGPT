"""
TrendTok Pipeline — One-Command Runner (#1)

Chains: overlay → preview → upload (with Drive cleanup) → summary.

Usage:
  python scripts/pipeline.py                    → full pipeline (overlay + upload)
  python scripts/pipeline.py --clean            → clean Drive folder before upload
  python scripts/pipeline.py --overlay-only     → only run overlay, skip upload
  python scripts/pipeline.py --upload-only      → only upload, skip overlay
  python scripts/pipeline.py --preview          → open contact sheet after overlay
  python scripts/pipeline.py --kill-stale       → kill stale node processes first (#9)
"""

import os
import sys
import subprocess
import time
import glob
import signal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
OVERLAID_DIR = os.path.join(BASE_DIR, 'output', 'gemgen_batch', 'overlaid')
PREVIEW_HTML = os.path.join(OVERLAID_DIR, 'preview.html')


def header(text):
    print(f"\n{'═' * 50}")
    print(f"  {text}")
    print(f"{'═' * 50}\n")


def kill_stale_processes():
    """Kill stale node processes older than 10 minutes (#9)."""
    print("🔪 Checking for stale node processes...")
    try:
        result = subprocess.run(
            ['powershell', '-Command',
             'Get-Process node -ErrorAction SilentlyContinue | '
             'Where-Object { (New-TimeSpan $_.StartTime).TotalMinutes -gt 10 } | '
             'ForEach-Object { '
             '  Write-Host "  Killing PID $($_.Id) (running $(([int](New-TimeSpan $_.StartTime).TotalMinutes))m): $($_.MainWindowTitle)"; '
             '  Stop-Process -Id $_.Id -Force '
             '}'],
            capture_output=True, text=True, cwd=BASE_DIR
        )
        output = result.stdout.strip()
        if output:
            print(output)
        else:
            print("  No stale processes found.")
    except Exception as e:
        print(f"  ⚠️  Could not check processes: {e}")


def run_overlay():
    """Run overlay_text.js."""
    header("Phase 1: Text Overlays (v2.0)")
    result = subprocess.run(
        ['node', os.path.join(SCRIPTS_DIR, 'overlay_text.js')],
        cwd=BASE_DIR
    )
    if result.returncode != 0:
        print("❌ Overlay failed!")
        sys.exit(1)
    return True


def generate_preview():
    """Generate a 2x5 contact sheet HTML for visual QA (#5)."""
    header("Phase 2: Overlay Preview")
    images = sorted(glob.glob(os.path.join(OVERLAID_DIR, '*.png')))
    if not images:
        print("⚠️  No overlaid images found for preview.")
        return

    # Build HTML contact sheet
    cells = ""
    for img in images:
        basename = os.path.basename(img)
        abs_path = os.path.abspath(img).replace("\\", "/")
        cells += f'''
        <div class="cell">
            <img src="file:///{abs_path}" alt="{basename}">
            <span>{basename}</span>
        </div>'''

    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>TrendTok Overlay Preview</title>
<style>
    body {{ background: #111; color: #fff; font-family: Arial; margin: 20px; }}
    h1 {{ text-align: center; color: #0ff; }}
    .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 1400px; margin: 0 auto; }}
    .cell {{ text-align: center; }}
    .cell img {{ width: 100%; border-radius: 8px; border: 2px solid #333; }}
    .cell span {{ display: block; margin-top: 4px; font-size: 11px; color: #888; }}
</style></head><body>
<h1>🎬 TrendTok Overlay Preview — {len(images)} slides</h1>
<div class="grid">{cells}</div>
</body></html>'''

    with open(PREVIEW_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"  📋 Contact sheet saved: {PREVIEW_HTML}")
    # Auto-open in browser
    os.startfile(PREVIEW_HTML)
    print("  🌐 Opened in browser for visual QA.\n")


def run_upload(clean=False):
    """Run upload_drive.py."""
    header("Phase 3: Google Drive Upload")
    cmd = ['python', os.path.join(SCRIPTS_DIR, 'upload_drive.py')]
    if clean:
        cmd.append('--clean')
    result = subprocess.run(cmd, cwd=BASE_DIR)
    if result.returncode != 0:
        print("❌ Upload failed!")
        sys.exit(1)
    return True


def main():
    args = set(sys.argv[1:])
    do_clean = '--clean' in args
    overlay_only = '--overlay-only' in args
    upload_only = '--upload-only' in args
    do_preview = '--preview' in args
    do_kill = '--kill-stale' in args

    header("TrendTok Pipeline — One-Command Runner")
    print(f"  Flags: clean={do_clean} preview={do_preview} kill-stale={do_kill}")
    print(f"  Output: {OVERLAID_DIR}\n")

    # #9: Kill stale processes
    if do_kill:
        kill_stale_processes()

    # Phase 1: Overlay
    if not upload_only:
        run_overlay()

    # Phase 2: Preview
    if do_preview:
        generate_preview()

    # Phase 3: Upload
    if not overlay_only:
        run_upload(clean=do_clean)

    header("✅ Pipeline Complete")


if __name__ == '__main__':
    main()
