"""Upload tiktok_captions.txt to the 'Tiktok ready' Drive folder."""
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE = r'C:\Users\Administrator\Desktop\PinGPT'
TOKEN = os.path.join(BASE, 'token.json')
FOLDER_ID = '1hGKOtWbET3cmPMZ6zK85-heFQRq9s5k8'
TXT = os.path.join(BASE, 'tiktok_captions.txt')

creds = Credentials.from_authorized_user_file(TOKEN, ['https://www.googleapis.com/auth/drive.file'])
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
svc = build('drive', 'v3', credentials=creds)

# Delete old copies first
old = svc.files().list(
    q=f"name='tiktok_captions.txt' and '{FOLDER_ID}' in parents and trashed=false",
    fields='files(id)'
).execute().get('files', [])
for f in old:
    svc.files().delete(fileId=f['id']).execute()
    print(f"Deleted old copy: {f['id']}")

r = svc.files().create(
    body={'name': 'tiktok_captions.txt', 'parents': [FOLDER_ID]},
    media_body=MediaFileUpload(TXT, mimetype='text/plain'),
    fields='id, name'
).execute()
print(f"Uploaded: {r['name']} -> id: {r['id']}")
