"""
Fix auto-message bug:
1. Add update_id deduplication to prevent Telegram retry processing
2. Remove redundant send_model_scene_picker after prompt generation in mscene callback
3. Remove redundant send_model_scene_picker after MODEL_PENDING processing
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# ── 1. Add PROCESSED_UPDATES dedup cache near MODEL_PENDING ──
content = content.replace(
    'MODEL_PENDING = {}  # {chat_id: {"hash": str, "scene": str}} — awaiting product/context input',
    'MODEL_PENDING = {}  # {chat_id: {"hash": str, "scene": str}} — awaiting product/context input\n'
    'PROCESSED_UPDATES = {}  # {update_id: timestamp} — dedup Telegram retries\n'
    'DEDUP_TTL = 120  # seconds to remember processed updates'
)

# ── 2. Add dedup check at top of webhook handler ──
old_webhook_body = '''    update = request.get_json(force=True) or {}

    # ── Handle callback queries (inline button taps) ──'''

new_webhook_body = '''    update = request.get_json(force=True) or {}

    # ── Dedup: skip already-processed updates (Telegram retries on slow response) ──
    update_id = update.get("update_id")
    if update_id:
        now = time.time()
        # Cleanup old entries
        expired = [k for k, v in PROCESSED_UPDATES.items() if now - v > DEDUP_TTL]
        for k in expired:
            del PROCESSED_UPDATES[k]
        # Check if already processed
        if update_id in PROCESSED_UPDATES:
            logger.info(f"Skipping duplicate update_id: {update_id}")
            return Response("OK", status=200)
        PROCESSED_UPDATES[update_id] = now

    # ── Handle callback queries (inline button taps) ──'''

content = content.replace(old_webhook_body, new_webhook_body)

# ── 3. Remove send_model_scene_picker after prompt generation in mscene callback ──
# This was causing extra messages after every scene generation
content = content.replace(
    '''            send_model_scene_picker(token, cid, model_hash, model_data["name"])
        return

    # ACTION CALLBACKS''',
    '''        return

    # ACTION CALLBACKS'''
)

# ── 4. Remove send_model_scene_picker after MODEL_PENDING processing ──
content = content.replace(
    '''                # Show scene picker again for another round
                send_model_scene_picker(token, cid, model_hash, model_name)''',
    '''                # Done — user can type #hash for another scene'''
)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")
