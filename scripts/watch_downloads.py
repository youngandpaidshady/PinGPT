#!/usr/bin/env python3
"""
watch_downloads.py — Catch Google Flow downloads, strip metadata, create analysis copies.

Watches your Downloads folder for new image files from Flow.
When a new file lands:
  1. Waits for download to finish (no .crdownload)
  2. Strips ALL EXIF/IPTC/C2PA metadata (clean bitmap redraw)
  3. Saves full 2K original to output/gemgen_batch/ as dl_1.png, dl_2.png, ...
  4. Creates compressed analysis copy in output/gemgen_batch/analysis/ (800px JPEG)
  5. Agent visually compares analysis copies against prompts to rename originals

Usage:
    python scripts/watch_downloads.py
    python scripts/watch_downloads.py --watch "C:\\Users\\Administrator\\Downloads"
"""

import os
import sys
import time
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Missing Pillow. Run: pip install Pillow")
    sys.exit(1)

BASE_DIR = Path(__file__).parent.parent
QUEUE_FILE = BASE_DIR / 'gemgen_queue.json'
OUTPUT_DIR = BASE_DIR / 'output' / 'gemgen_batch'
ANALYSIS_DIR = OUTPUT_DIR / 'analysis'
DOWNLOAD_LOG = OUTPUT_DIR / 'download_map.json'
DEFAULT_WATCH = Path(os.path.expanduser('~')) / 'Downloads'

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
TEMP_EXTENSIONS = {'.crdownload', '.tmp', '.part', '.download'}


def load_queue_info():
    prefix = 'pin'
    target = 10
    if QUEUE_FILE.exists():
        try:
            data = json.loads(QUEUE_FILE.read_text(encoding='utf-8'))
            if data.get('items'):
                target = len(data['items'])
            sid = data.get('session_id', '')
            if sid and sid != 'gemgen_run':
                prefix = sid.replace('_run', '')
        except Exception:
            pass
    return prefix, target


def is_image(filepath):
    p = Path(filepath)
    if p.suffix.lower() in IMAGE_EXTENSIONS:
        return True
    if p.suffix == '':
        try:
            with open(filepath, 'rb') as f:
                h = f.read(8)
            return h[:3] == b'\xff\xd8\xff' or h[:8] == b'\x89PNG\r\n\x1a\n'
        except OSError:
            return False
    return False


def wait_ready(filepath, timeout=30):
    prev = -1
    for _ in range(timeout):
        try:
            curr = os.path.getsize(filepath)
            if curr == prev and curr > 0:
                return True
            prev = curr
        except OSError:
            pass
        time.sleep(1)
    return False


def strip_and_save(src, dst):
    """Redraw to clean bitmap (strips ALL metadata), save as PNG."""
    img = Image.open(src)
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))
    clean.save(dst, 'PNG')
    w, h = clean.size
    size_mb = os.path.getsize(dst) / (1024 * 1024)
    img.close()
    clean.close()
    return w, h, size_mb


def make_analysis_copy(src_png, name):
    """Create a small JPEG for agent visual matching."""
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    dst = ANALYSIS_DIR / name.replace('.png', '.jpg')
    try:
        img = Image.open(src_png)
        ratio = 800 / img.width
        small = img.resize((800, int(img.height * ratio)), Image.LANCZOS)
        small.save(dst, 'JPEG', quality=72)
        img.close()
        small.close()
    except Exception as e:
        print(f"  Analysis copy failed: {e}")


def load_download_map():
    if DOWNLOAD_LOG.exists():
        return json.loads(DOWNLOAD_LOG.read_text(encoding='utf-8'))
    return {}


def save_download_map(dmap):
    DOWNLOAD_LOG.write_text(json.dumps(dmap, indent=2), encoding='utf-8')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', default=str(DEFAULT_WATCH))
    parser.add_argument('--count', type=int, help='Override target count')
    args = parser.parse_args()

    watch_dir = Path(args.watch)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    prefix, target = load_queue_info()
    if args.count:
        target = args.count

    print(f"\n{'=' * 55}")
    print(f"  PinGPT Download Watcher")
    print(f"{'=' * 55}")
    print(f"  Watching:  {watch_dir}")
    print(f"  Output:    {OUTPUT_DIR}")
    print(f"  Target:    {target} images")
    print(f"{'=' * 55}")
    print(f"  Waiting for downloads... (Ctrl+C to stop)\n")

    # Snapshot current files
    known = set()
    for f in watch_dir.iterdir():
        if f.is_file():
            known.add(f.name)

    # Load existing download map
    dmap = load_download_map()
    # Dynamically find next counter based on existing files to avoid overwriting
    existing_pngs = [f for f in OUTPUT_DIR.iterdir() if f.suffix == '.png' and f.stem.startswith('dl_')]
    max_num = 0
    for f in existing_pngs:
        try:
            num = int(f.stem.replace('dl_', ''))
            max_num = max(max_num, num)
        except ValueError:
            pass
    counter = max_num + 1
    caught = 0

    try:
        while caught < target:
            time.sleep(2)
            current = {f.name for f in watch_dir.iterdir() if f.is_file()}
            new_files = current - known

            for fname in sorted(new_files):
                fpath = watch_dir / fname

                if fpath.suffix.lower() in TEMP_EXTENSIONS:
                    continue
                if not is_image(fpath):
                    known.add(fname)
                    continue
                if not wait_ready(fpath):
                    print(f"  Timeout: {fname}")
                    known.add(fname)
                    continue

                # Process
                temp_name = f"dl_{counter}.png"
                dst = OUTPUT_DIR / temp_name

                try:
                    w, h, mb = strip_and_save(fpath, dst)
                    os.remove(fpath)

                    # Log original filename for fuzzy matching
                    dmap[temp_name] = {
                        "original_name": fname,
                        "dimensions": f"{w}x{h}",
                        "size_mb": round(mb, 1),
                    }
                    save_download_map(dmap)

                    # Create compressed analysis copy for agent vision
                    make_analysis_copy(dst, temp_name)

                    print(f"  dl_{counter}.png ({w}x{h}, {mb:.1f}MB) <- {fname}")
                    counter += 1
                    caught += 1
                except Exception as e:
                    print(f"  FAILED {fname}: {e}")

                known.add(fname)

            if caught > 0 and caught < target:
                sys.stdout.write(f"\r  {caught}/{target} caught...   ")
                sys.stdout.flush()

    except KeyboardInterrupt:
        print(f"\n\n  Stopped.")

    # Summary
    print(f"\n{'=' * 55}")
    print(f"  Caught: {caught}/{target}")
    pngs = [f for f in OUTPUT_DIR.iterdir() if f.suffix == '.png' and f.stem.startswith('dl_')]
    print(f"  Files:  {len(pngs)} in {OUTPUT_DIR}")
    if caught < target:
        print(f"  Missing {target - caught} images")
    else:
        print(f"  All {target} images caught!")
    print(f"  Analysis copies: {ANALYSIS_DIR}")
    print(f"  Agent can now view analysis/ to match images to prompts.")
    print(f"{'=' * 55}\n")


if __name__ == '__main__':
    main()
