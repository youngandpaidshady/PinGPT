"""Test the webhook module can import and the critical functions work."""
import sys, os
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test")
os.environ.setdefault("GEMINI_API_KEYS", "test")

# Read the file and extract just the functions we need
content = open(r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py', encoding='utf-8').read()

# Check for common issues
print("=== Checking for issues ===")

# 1. Check html_escape exists and is before usage
html_escape_line = None
for i, line in enumerate(content.split('\n'), 1):
    if 'def html_escape(' in line:
        html_escape_line = i
        break
print(f"html_escape defined at line: {html_escape_line}")

# 2. Check all html_escape references are AFTER the definition
refs = []
for i, line in enumerate(content.split('\n'), 1):
    if 'html_escape(' in line and 'def html_escape' not in line:
        refs.append(i)
print(f"html_escape used at lines: {refs}")

if html_escape_line and refs:
    before_def = [r for r in refs if r < html_escape_line]
    if before_def:
        print(f"ERROR: html_escape used BEFORE definition at lines: {before_def}")
    else:
        print("OK: all references are after definition")

# 3. Try importing the module
print("\n=== Trying module import ===")
try:
    sys.path.insert(0, r'c:\Users\Administrator\Desktop\PinGPT')
    from api import webhook
    print("Module import: OK")
    
    # Test html_escape
    result = webhook.html_escape("test & <value> OK")
    print(f"html_escape test: {result}")
    
    # Test build_model_prompt
    prompt = webhook.build_model_prompt("test DNA description", "smiling in a cafe")
    print(f"build_model_prompt: OK ({len(prompt)} chars)")
    
except Exception as e:
    print(f"Import ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
