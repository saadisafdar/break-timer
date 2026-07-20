"""
Plays break-sound WAV files, cross-platform, non-blocking.

Windows: winsound (stdlib)
macOS:   afplay (bundled with the OS)
Linux:   paplay or aplay, whichever is present
"""
import os
import sys
import subprocess
import shutil

SOUND_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")

SOUND_FILES = {
    "None": None,
    "Gong": "gong.wav",
    "Blip": "blip.wav",
    "Bloop": "bloop.wav",
    "Ping": "ping.wav",
    "Sci-fi": "scifi.wav",
}


def available_sounds():
    return list(SOUND_FILES.keys())


def play_sound(name):
    filename = SOUND_FILES.get(name)
    if not filename:
        return
    path = os.path.join(SOUND_DIR, filename)
    if not os.path.exists(path):
        return

    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", path],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            player = shutil.which("paplay") or shutil.which("aplay")
            if player:
                subprocess.Popen([player, path],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Never let a sound failure crash the app
