"""
Download batch images from Drive, strip all metadata, delete old Drive copies, reupload clean.
Updates pinterest_urls.json with new file IDs.
"""
import os, json, io
from PIL import Image
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

BASE = r'C:\Users\Administrator\Desktop\PinGPT'
TOKEN = os.path.join(BASE, 'token.json')
URLS_FILE = os.path.join(BASE, 'pinterest_urls.json')
BATCH_DIR = os.path.join(BASE, 'output', 'gemgen_batch')

# Auth
creds = Credentials.from_authorized_user_file(TOKEN, ['https://www.googleapis.com/auth/drive.file'])
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
svc = build('drive', 'v3', credentials=creds)

# Load URL mapping
with open(URLS_FILE, 'r') as f:
    urls = json.load(f)

print(f"Processing {len(urls)} images...\n")
new_urls = {}

for filename, info in urls.items():
    file_id = info['id']
    print(f"  [{filename}]")

    # 1. Download from Drive
    print(f"    Downloading...", end=" ")
    request = svc.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buf.seek(0)
    print("OK")

    # 2. Strip metadata with Pillow
    print(f"    Stripping metadata...", end=" ")
    img = Image.open(buf)
    clean_buf = io.BytesIO()
    clean_img = Image.new(img.mode, img.size)
    clean_img.putdata(list(img.getdata()))
    clean_img.save(clean_buf, format='PNG')
    clean_buf.seek(0)
    clean_size = clean_buf.getbuffer().nbytes
    print(f"OK ({clean_size // 1024}KB)")

    # Also save locally
    local_path = os.path.join(BATCH_DIR, filename)
    with open(local_path, 'wb') as f:
        f.write(clean_buf.getvalue())
    clean_buf.seek(0)

    # 3. Delete old Drive copy
    print(f"    Deleting old Drive copy...", end=" ")
    try:
        svc.files().delete(fileId=file_id).execute()
        print("OK")
    except Exception as e:
        print(f"WARN: {e}")

    # 4. Upload clean version
    print(f"    Uploading clean...", end=" ")
    # Find the Pinterest Bulk folder
    parent_query = svc.files().list(
        q="name='Pinterest Bulk' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields='files(id)'
    ).execute().get('files', [])
    folder_id = parent_query[0]['id'] if parent_query else None

    media = MediaIoBaseUpload(clean_buf, mimetype='image/png', resumable=True)
    body = {'name': filename}
    if folder_id:
        body['parents'] = [folder_id]
    result = svc.files().create(body=body, media_body=media, fields='id').execute()
    new_id = result['id']

    # Set public sharing
    svc.permissions().create(
        fileId=new_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    new_urls[filename] = {
        'id': new_id,
        'url': f'https://lh3.googleusercontent.com/d/{new_id}',
        'drive_url': f'https://drive.google.com/uc?export=view&id={new_id}'
    }
    print(f"OK -> {new_id}")
    print()

# Save updated URL mapping
with open(URLS_FILE, 'w') as f:
    json.dump(new_urls, f, indent=2)
print(f"\nDone! {len(new_urls)} images stripped & reuploaded.")
print(f"Updated {URLS_FILE}")
print(f"Local copies saved to {BATCH_DIR}")
print(f"\nNext: run 'node scripts/build_bulk_csv.js' to regenerate CSV with new URLs")
