"""
Fix: HTML-escape all prompt content before wrapping in <code> tags.
Telegram's HTML parser rejects messages with unescaped &, <, > inside tags.
"""

filepath = r'c:\Users\Administrator\Desktop\PinGPT\api\webhook.py'
content = open(filepath, 'r', encoding='utf-8').read()

# Add html_escape helper after the imports
import_marker = 'import hashlib'
if 'def html_escape(' not in content:
    content = content.replace(
        import_marker,
        import_marker + '\nimport html as html_module'
    )

# Add html_escape function after tg_answer_callback
if 'def html_escape(' not in content:
    content = content.replace(
        'def cleanup_photo_cache():',
        'def html_escape(text):\n'
        '    """Escape HTML special chars for safe embedding in Telegram HTML messages."""\n'
        '    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")\n\n\n'
        'def cleanup_photo_cache():'
    )

# Fix ALL places where prompt is wrapped in <code>{prompt}</code>
# 1. #hash routing
content = content.replace(
    'f"<code>{prompt}</code>\\n\\n"\n'
    '                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_data[\'hash\']} \\u2192 paste into Gemini!</i>"',
    'f"<code>{html_escape(prompt)}</code>\\n\\n"\n'
    '                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_data[\'hash\']} \\u2192 paste into Gemini!</i>"'
)

# 2. /model use section
content = content.replace(
    'f"<code>{prompt}</code>\\n\\n"\n'
    '                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                f"\\U0001f512 <i>DNA locked \\u2014 #{model_data[\'hash\']} \\u2192 paste into Gemini!</i>"',
    'f"<code>{html_escape(prompt)}</code>\\n\\n"\n'
    '                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                f"\\U0001f512 <i>DNA locked \\u2014 #{model_data[\'hash\']} \\u2192 paste into Gemini!</i>"'
)

# 3. mscene callback
content = content.replace(
    'f"<code>{prompt}</code>\\n\\n"\n'
    '                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"',
    'f"<code>{html_escape(prompt)}</code>\\n\\n"\n'
    '                f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"'
)

# 4. MODEL_PENDING handler
content = content.replace(
    'f"<code>{prompt}</code>\\n\\n"\n'
    '                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"',
    'f"<code>{html_escape(prompt)}</code>\\n\\n"\n'
    '                    f"\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\n"\n'
    '                    f"\\U0001f512 <i>DNA locked \\u2014 #{model_hash} \\u2192 paste into Gemini!</i>"'
)

# Also escape the DNA preview in model creation
content = content.replace(
    'f"<i>{dna_preview}</i>',
    'f"<i>{html_escape(dna_preview)}</i>'
)

# And escape initial_prompt in reference prompt
content = content.replace(
    'f"<code>{initial_prompt}</code>"',
    'f"<code>{html_escape(initial_prompt)}</code>"'
)

# Write
open(filepath, 'w', encoding='utf-8', newline='\n').write(content)
print(f"Done! {len(content.splitlines())} lines")

# Verify syntax
import py_compile
py_compile.compile(filepath, doraise=True)
print("Syntax OK")

# Count remaining unescaped <code>{...} patterns
import re
matches = re.findall(r'<code>\{(?!html_escape)', content)
print(f"Remaining unescaped <code> wraps: {len(matches)}")
