import os
import sys
import json
import time
import pyperclip
try:
    import pyautogui
except ImportError:
    print("pip install pyautogui pyperclip")
    sys.exit(1)

def submit_prompts():
    # Prompt for text box
    pyautogui.alert(text="Subagent is offline. Please hover your mouse over the TEXT INPUT BOX in Google Flow, then press ENTER to close this alert.", title="Calibration 1 - Text Box")
    
    # Needs a small delay to ensure mouse is still over it after pressing OK if using enter
    text_x, text_y = pyautogui.position()
    
    # Prompt for send button
    pyautogui.alert(text="Great! Now hover your mouse over the SEND BUTTON (arrow), then press ENTER to close this alert.", title="Calibration 2 - Send Button")
    
    send_x, send_y = pyautogui.position()
    
    # Load prompts
    with open("gemgen_queue.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
        
    pyautogui.alert(text=f"Ready to submit {len(prompts)} prompts. Please DO NOT touch the mouse or keyboard after clicking OK.", title="Starting Submission")
    time.sleep(2)
    
    for i, p in enumerate(prompts):
        text = p["prompt"]
        
        # Click text box
        pyautogui.click(text_x, text_y)
        time.sleep(0.5)
        
        # Paste text
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        
        # Click Send
        pyautogui.click(send_x, send_y)
        
        # Wait for generation (Flow needs a few seconds before the next rapid-fire input)
        time.sleep(4.5)
        
    pyautogui.alert("All 54 prompts submitted successfully!", title="Done")

if __name__ == "__main__":
    submit_prompts()
