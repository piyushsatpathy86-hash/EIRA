# ============================================================
# EIRA — Desktop Control (Wallpaper + Screenshot)
# ============================================================

import sys
sys.path.append("C:/EIRA")

import ctypes
import os
import subprocess
import requests
from datetime import datetime

os.makedirs("C:/EIRA/data/screenshots", exist_ok=True)
os.makedirs("C:/EIRA/eira_assets/wallpapers", exist_ok=True)


def change_wallpaper(image_path: str) -> str:
    """Change wallpaper from local file path"""
    abs_path = os.path.abspath(image_path)
    if not os.path.exists(abs_path):
        return f"File nahi mili: {abs_path}"
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
    return f"Wallpaper change ho gayi: {abs_path}"


def download_and_set_wallpaper(query: str) -> str:
    """Internet se wallpaper download karke set karo"""
    try:
        # Picsum — 100% free, no redirect
        url       = "https://picsum.photos/1920/1080"
        print(f"Downloading wallpaper...")
        response  = requests.get(
            url, timeout=15, allow_redirects=True)

        if response.status_code == 200:
            save_path = (
                f"C:/EIRA/eira_assets/wallpapers/"
                f"{query[:20].replace(' ','_')}.jpg"
            )
            with open(save_path, "wb") as f:
                f.write(response.content)
            result = change_wallpaper(save_path)
            return f"Wallpaper set ho gayi!\n{result}"
        else:
            return f"Download failed: {response.status_code}"

    except Exception as e:
        return f"Error: {str(e)}"


def take_screenshot(filename: str = "") -> str:
    """Screenshot lo"""
    try:
        import pyautogui
        if not filename:
            ts       = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"C:/EIRA/data/screenshots/ss_{ts}.png"
        img = pyautogui.screenshot()
        img.save(filename)
        return f"Screenshot saved: {filename}"
    except Exception as e:
        return f"Screenshot error: {str(e)}"


def get_screen_size() -> str:
    """Screen size check karo"""
    try:
        import pyautogui
        w, h = pyautogui.size()
        return f"Screen size: {w}x{h}"
    except Exception as e:
        return f"Error: {str(e)}"


# ── Test ────────────────────────────────────────────────────
if __name__ == "__main__":
    print("EIRA Desktop Control Test")
    print("-" * 40)

    # Screenshot test
    result = take_screenshot()
    print(result)

    # Wallpaper test
    query  = input("\nWallpaper keyword (jaise 'nature dark'): ")
    result = download_and_set_wallpaper(query)
    print(result)