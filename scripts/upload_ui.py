import pyautogui, time, ctypes, subprocess

user32 = ctypes.windll.user32

subprocess.Popen(['C:/Program Files/Google/Chrome/Application/chrome.exe', 'https://www.pinterest.com/settings/bulk-create-pins/'])
time.sleep(5)

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
chrome_hwnd = None
def find_chrome(hwnd, _):
    global chrome_hwnd
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if 'Pinterest' in buff.value or 'Google Chrome' in buff.value:
            chrome_hwnd = hwnd
    return True
user32.EnumWindows(EnumWindowsProc(find_chrome), 0)
user32.ShowWindow(chrome_hwnd, 9)
time.sleep(0.5)
user32.SetForegroundWindow(chrome_hwnd)
time.sleep(1)

pyautogui.click(440, 375)
time.sleep(3)

dialog_hwnd = None
def find_dialog(hwnd, _):
    global dialog_hwnd
    length = user32.GetWindowTextLengthW(hwnd)
    if length > 0:
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        if buff.value.strip() == 'Open':
            dialog_hwnd = hwnd
    return True
user32.EnumWindows(EnumWindowsProc(find_dialog), 0)
user32.SetForegroundWindow(dialog_hwnd)
time.sleep(1)

pyautogui.hotkey('alt', 'n')
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.2)
pyautogui.typewrite(r'C:\Users\Administrator\Desktop\PinGPT\output\pinterest_bulk.csv', interval=0.01)
time.sleep(0.5)
pyautogui.press('enter')
print('CSV submitted — check Pinterest for Upload successful dialog')
