"""
Upload overlaid images + TikTok metadata to Google Drive "Tiktok ready" folder.
Uses Google Drive API (OAuth 2.0).

Flags:
  --clean         Delete all existing files in Drive folder before uploading
  --dir PATH      Override upload directory (default: output/gemgen_batch/overlaid)
  --include-raw   Also upload uncaptioned images from gemgen_batch/ as wallpapers
  --pinterest     Upload raw images to a PUBLIC Drive folder for Pinterest bulk CSV.
                  Generates pinterest_urls.json with {filename: public_url} mapping.
"""

import os
import sys
import json
import glob
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
CREDS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')
FOLDER_ID = '1hGKOtWbET3cmPMZ6zK85-heFQRq9s5k8'  # "Tiktok ready" folder
PINTEREST_FOLDER_NAME = 'Pinterest Bulk'  # Auto-created public folder
OVERLAID_DIR = os.path.join(BASE_DIR, 'output', 'gemgen_batch', 'overlaid')
RAW_DIR = os.path.join(BASE_DIR, 'output', 'gemgen_batch')
PINTEREST_URLS_FILE = os.path.join(BASE_DIR, 'pinterest_urls.json')

MIME_MAP = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.txt': 'text/plain',
}


def get_drive_service():
    """Authenticate and return Drive API service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting local server for authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
        print("Token saved.\n")

    return build('drive', 'v3', credentials=creds)


def list_drive_files(service, folder_id):
    """List all files in the Drive folder. Returns list of {id, name, size}."""
    results = []
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='nextPageToken, files(id, name, size)',
            pageToken=page_token
        ).execute()
        results.extend(resp.get('files', []))
        page_token = resp.get('nextPageToken')
        if not page_token:
            break
    return results


def clean_drive_folder(service, folder_id):
    """Delete all files in the Drive folder (#2: auto-clean before upload)."""
    existing = list_drive_files(service, folder_id)
    if not existing:
        print("  Drive folder already empty.\n")
        return 0

    print(f"  Deleting {len(existing)} existing file(s)...")
    deleted = 0
    for f in existing:
        try:
            service.files().delete(fileId=f['id']).execute()
            deleted += 1
        except Exception as e:
            print(f"    ⚠️  Could not delete {f['name']}: {e}")
    print(f"  Cleared {deleted} file(s).\n")
    return deleted


def upload_file(service, filepath, folder_id, existing_files=None):
    """Upload a file. Skips if identical file exists (#6: dedup)."""
    filename = os.path.basename(filepath)
    local_size = str(os.path.getsize(filepath))

    # Dedup check
    if existing_files:
        for ef in existing_files:
            if ef['name'] == filename and ef.get('size') == local_size:
                return None  # Skip — identical file exists

    ext = os.path.splitext(filepath)[1].lower()
    mimetype = MIME_MAP.get(ext, 'application/octet-stream')

    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filepath, mimetype=mimetype, resumable=True)

    result = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name'
    ).execute()
    return result


def collect_raw_images(raw_dir):
    """Collect raw (uncaptioned) PNGs from gemgen_batch/, excluding subdirectories."""
    raw_files = sorted(glob.glob(os.path.join(raw_dir, '*.png')))
    if not raw_files:
        raw_files = sorted(glob.glob(os.path.join(raw_dir, '*.jpg')))
    return raw_files


# ── Pinterest Bulk Upload Functions ──────────────────────────────────────────

def get_or_create_pinterest_folder(service):
    """Find or create the 'Pinterest Bulk' folder in Drive root. Returns folder ID."""
    # Search for existing folder
    resp = service.files().list(
        q=f"name='{PINTEREST_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id, name)',
        spaces='drive'
    ).execute()
    existing = resp.get('files', [])
    if existing:
        folder_id = existing[0]['id']
        print(f"  Found existing '{PINTEREST_FOLDER_NAME}' folder: {folder_id}")
        return folder_id

    # Create new folder
    metadata = {
        'name': PINTEREST_FOLDER_NAME,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=metadata, fields='id').execute()
    folder_id = folder['id']
    print(f"  Created '{PINTEREST_FOLDER_NAME}' folder: {folder_id}")

    # Make folder itself publicly viewable
    service.permissions().create(
        fileId=folder_id,
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()
    print(f"  Folder set to public (anyone with link)")
    return folder_id


def make_file_public(service, file_id):
    """Set a Drive file to 'anyone with link can view'."""
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'},
        fields='id'
    ).execute()


def get_direct_url(file_id):
    """Get a direct-access URL for a Drive file (for Pinterest CSV)."""
    # Primary: lh3 proxy (fast, no redirect, works for images)
    # Fallback in CSV comments: drive.google.com/uc?export=view&id=...
    return f"https://lh3.googleusercontent.com/d/{file_id}"


def run_pinterest_mode(service, source_dir=None):
    """Upload images to public Drive folder and generate pinterest_urls.json."""
    print("=" * 50)
    print("  Pinterest Bulk Upload — Public Image Hosting")
    print("=" * 50 + "\n")

    # Determine source directory
    if not source_dir:
        source_dir = RAW_DIR

    # Collect images
    files = sorted(glob.glob(os.path.join(source_dir, '*.png')))
    if not files:
        files = sorted(glob.glob(os.path.join(source_dir, '*.jpg')))
    if not files:
        print(f"No images found in {source_dir}")
        sys.exit(1)

    print(f"Found {len(files)} images to upload:\n")
    total_size = 0
    for f in files:
        size_mb = os.path.getsize(f) / (1024 * 1024)
        total_size += size_mb
        print(f"  {os.path.basename(f)} — {size_mb:.1f}MB")
    print(f"\n  Total: {total_size:.1f}MB\n")

    # Get or create the Pinterest folder
    print("Setting up Pinterest folder...")
    pinterest_folder_id = get_or_create_pinterest_folder(service)

    # Clean existing files in Pinterest folder
    existing = list_drive_files(service, pinterest_folder_id)
    if existing:
        print(f"\n  Clearing {len(existing)} old file(s) from Pinterest folder...")
        clean_drive_folder(service, pinterest_folder_id)

    # Upload each image, make public, collect URLs
    url_map = {}  # {filename: {id, url, drive_url}}
    uploaded = 0
    failed = 0

    print(f"\nUploading {len(files)} images...\n")
    for i, filepath in enumerate(files):
        basename = os.path.basename(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  [{i+1}/{len(files)}] {basename} ({size_mb:.1f}MB)...", end=" ", flush=True)

        try:
            result = upload_file(service, filepath, pinterest_folder_id)
            if result:
                file_id = result['id']
                # Make publicly accessible
                make_file_public(service, file_id)
                direct_url = get_direct_url(file_id)
                url_map[basename] = {
                    'id': file_id,
                    'url': direct_url,
                    'drive_url': f"https://drive.google.com/uc?export=view&id={file_id}"
                }
                print(f"OK")
                uploaded += 1
            else:
                print("SKIP (duplicate)")
        except Exception as e:
            print(f"FAIL: {str(e)[:80]}")
            failed += 1

    # Write URL mapping
    with open(PINTEREST_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(url_map, f, indent=2)

    print(f"\n{'=' * 50}")
    print(f"  Uploaded: {uploaded} | Failed: {failed}")
    print(f"  URL map saved to: {PINTEREST_URLS_FILE}")
    print(f"{'=' * 50}\n")

    # Print sample URLs for verification
    if url_map:
        sample_key = list(url_map.keys())[0]
        sample = url_map[sample_key]
        print(f"Sample URL (paste in browser to test):")
        print(f"  {sample['url']}\n")

    return url_map




def main():
    args = sys.argv[1:]
    do_clean = '--clean' in args
    if do_clean:
        args.remove('--clean')

    include_raw = '--include-raw' in args
    if include_raw:
        args.remove('--include-raw')

    pinterest_mode = '--pinterest' in args
    if pinterest_mode:
        args.remove('--pinterest')

    upload_dir = OVERLAID_DIR
    if '--dir' in args:
        idx = args.index('--dir')
        upload_dir = args[idx + 1]

    # Authenticate first (shared across modes)
    service = get_drive_service()

    # Pinterest mode: upload to public folder + generate URL mapping
    if pinterest_mode:
        source_dir = upload_dir if '--dir' in sys.argv else None
        run_pinterest_mode(service, source_dir)
        return

    print("=" * 50)
    print("  Google Drive Upload — TrendTok Pipeline")
    print("=" * 50 + "\n")

    # Find overlaid upload files
    files = sorted(glob.glob(os.path.join(upload_dir, '*.png')))
    if not files:
        files = sorted(glob.glob(os.path.join(upload_dir, '*.jpg')))
    if not files:
        print(f"❌ No images found in {upload_dir}")
        sys.exit(1)

    # Collect raw wallpaper images if requested
    raw_files = []
    if include_raw:
        raw_files = collect_raw_images(RAW_DIR)
        if raw_files:
            print(f"🖼️  --include-raw: Found {len(raw_files)} uncaptioned wallpaper images\n")
        else:
            print("ℹ️  --include-raw: No raw images found in gemgen_batch/\n")

    # Check for metadata
    metadata_txt = os.path.join(upload_dir, 'tiktok_metadata.txt')
    if not os.path.exists(metadata_txt):
        metadata_txt = None
        print("ℹ️  No tiktok_metadata.txt found — uploading images only\n")
    else:
        print("📝 Found tiktok_metadata.txt — will upload alongside images\n")

    # List overlaid files
    total_size = 0
    print(f"Found {len(files)} overlaid (captioned) images to upload:\n")
    for f in files:
        size_mb = os.path.getsize(f) / (1024 * 1024)
        total_size += size_mb
        print(f"  📝 {os.path.basename(f)} — {size_mb:.1f}MB")

    # List raw wallpaper files
    if raw_files:
        print(f"\nFound {len(raw_files)} raw (wallpaper) images to upload:\n")
        for f in raw_files:
            size_mb = os.path.getsize(f) / (1024 * 1024)
            total_size += size_mb
            print(f"  🖼️  {os.path.basename(f)} — {size_mb:.1f}MB")

    if metadata_txt:
        print(f"  tiktok_metadata.txt — {os.path.getsize(metadata_txt) / 1024:.1f}KB")
    print(f"\n  Total: {total_size:.1f}MB + metadata\n")


    # Clean old files if requested (#2)
    existing_files = []
    if do_clean:
        print("🧹 --clean: Clearing Drive folder before upload...")
        clean_drive_folder(service, FOLDER_ID)
    else:
        # Load existing for dedup (#6)
        existing_files = list_drive_files(service, FOLDER_ID)
        if existing_files:
            print(f"📂 {len(existing_files)} file(s) already in Drive — will skip duplicates\n")

    # Upload
    uploaded = 0
    skipped = 0
    failed = 0

    # Build full file list: overlaid + raw wallpapers + metadata
    all_files = files + raw_files + ([metadata_txt] if metadata_txt else [])
    total_files = len(all_files)

    for i, filepath in enumerate(all_files):
        basename = os.path.basename(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)

        if filepath == metadata_txt:
            label = "META"
        elif filepath in raw_files:
            label = f"RAW {raw_files.index(filepath)+1}/{len(raw_files)}"
        else:
            label = f"{files.index(filepath)+1}/{len(files)}"

        print(f"[{label}] {basename} ({size_mb:.1f}MB)...", end=" ", flush=True)

        try:
            result = upload_file(service, filepath, FOLDER_ID,
                                 existing_files if not do_clean else None)
            if result is None:
                print("⏭️  (duplicate, skipped)")
                skipped += 1
            else:
                print(f"✅ (id: {result['id']})")
                uploaded += 1
        except Exception as e:
            print(f"❌ {str(e)[:100]}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Uploaded: {uploaded} | Skipped: {skipped} | Failed: {failed} | Total: {total_files}")
    if include_raw and raw_files:
        print(f"  (includes {len(raw_files)} uncaptioned wallpaper images)")
    print(f"{'=' * 50}")


if __name__ == '__main__':
    main()

