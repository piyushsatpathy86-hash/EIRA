# ============================================================
# EIRA — System Control (Apps, Hotkeys, Typing)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import os
import subprocess
import pyautogui
import time

# App shortcuts map
APPS = {
    "vscode":    "code",
    "vs code":   "code",
    "chrome":    "start chrome",
    "browser":   "start chrome",
    "notepad":   "notepad",
    "calculator":"calc",
    "explorer":  "explorer",
    "spotify":   "start spotify",
    "terminal":  "start cmd",
    "powershell":"start powershell",
    "task manager": "taskmgr",
    "paint":     "mspaint",
    "word":      "start winword",
    "excel":     "start excel",
}


def open_app(app_name: str) -> str:
    """Koi bhi app open karo"""
    try:
        app_lower = app_name.lower().strip()

        # Agar website mention hai toh website kholo
        websites = ["youtube", "google", "github",
                    "leetcode", "gmail", "linkedin"]
        for site in websites:
            if site in app_lower:
                return open_website(site)

        cmd = APPS.get(app_lower)
        if cmd:
            subprocess.Popen(cmd, shell=True)
            return f"Opened: {app_name} ✅"
        else:
            subprocess.Popen(app_name, shell=True)
            return f"Tried opening: {app_name}"

    except Exception as e:
        return f"Error: {str(e)}"

def open_website(url: str) -> str:
    """Browser mein website kholo"""
    try:
        # Common shortcuts
        shortcuts = {
            "youtube":  "https://www.youtube.com",
            "yt":       "https://www.youtube.com",
            "google":   "https://www.google.com",
            "github":   "https://www.github.com",
            "leetcode": "https://www.leetcode.com",
            "gmail":    "https://www.gmail.com",
            "linkedin": "https://www.linkedin.com",
            "netflix":  "https://www.netflix.com",
            "spotify":  "https://open.spotify.com",
            "chatgpt":  "https://chat.openai.com",
        }

        url_lower = url.lower().strip()

        # Shortcut check
        if url_lower in shortcuts:
            final_url = shortcuts[url_lower]
        elif not url.startswith("http"):
            final_url = "https://www." + url
        else:
            final_url = url

        os.startfile(final_url)
        return f"Opened: {final_url} ✅"

    except Exception as e:
        return f"Error: {str(e)}"

def type_text(text: str, delay: float = 0.05) -> str:
    """Keyboard se text type karo"""
    try:
        time.sleep(1)
        pyautogui.typewrite(text, interval=delay)
        return f"Typed: {text} ✅"
    except Exception as e:
        return f"Error: {str(e)}"


def press_hotkey(*keys) -> str:
    """Keyboard shortcut press karo"""
    try:
        pyautogui.hotkey(*keys)
        return f"Pressed: {'+'.join(keys)} ✅"
    except Exception as e:
        return f"Error: {str(e)}"


def get_volume(level: int) -> str:
    """Volume set karo 0-100"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level/100, None)
        return f"Volume set to {level}% ✅"
    except Exception:
        # Fallback
        os.system(f"nircmd.exe setsysvolume {int(level*655.35)}")
        return f"Volume command sent: {level}%"


def lock_screen() -> str:
    """Screen lock karo"""
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Screen locked ✅"


def shutdown(minutes: int = 0) -> str:
    """Shutdown schedule karo"""
    if minutes == 0:
        os.system("shutdown /s /t 0")
        return "Shutting down now..."
    else:
        seconds = minutes * 60
        os.system(f"shutdown /s /t {seconds}")
        return f"Shutdown in {minutes} minutes ✅"


def cancel_shutdown() -> str:
    """Shutdown cancel karo"""
    os.system("shutdown /a")
    return "Shutdown cancelled ✅"


def get_battery() -> str:
    """Battery status check karo"""
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Charging" if battery.power_plugged else "Not charging"
            return f"Battery: {battery.percent:.0f}% — {plugged}"
        return "Battery info nahi mili"
    except Exception as e:
        return f"Error: {str(e)}"

def open_youtube_video(url: str) -> str:
    """YouTube video seedha kholo"""
    try:
        # YT link fix karo
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={video_id}"
        elif "youtube.com" not in url:
            # Search karo YouTube pe
            query = url.replace(" ", "+")
            url   = f"https://www.youtube.com/results?search_query={query}"

        os.startfile(url)
        return f"YouTube video khul gaya! ✅"

    except Exception as e:
        return f"Error: {str(e)}"
# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("EIRA System Control Test")
    print("-" * 40)

    # Battery check
    print(get_battery())

    # Open app test
    app = input("\nKaunsa app kholu? (vscode/chrome/notepad): ")
    print(open_app(app))

    # Website test
    site = input("\nKaunsi website kholu?: ")
    print(open_website(site))