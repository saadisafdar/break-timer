"""Optional system tray icon for Break Timer.

Uses pystray + Pillow if available. If either is missing (e.g. a minimal
Linux box with no tray daemon), tray support is silently skipped and the
app still runs exactly as before - just without a tray icon.
"""

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except Exception:
    # Covers ImportError as well as backend-selection errors pystray can
    # raise on systems missing a tray backend (e.g. no GTK/AppIndicator).
    TRAY_AVAILABLE = False


def _make_icon_image():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, size - 4, size - 4), fill=(20, 184, 166, 255))
    draw.line((size // 2, size // 2, size // 2, 14), fill="white", width=4)
    draw.line((size // 2, size // 2, size - 18, size // 2), fill="white", width=4)
    return img


def run_tray(on_break_now, on_quit):
    """Blocks - call this on a background thread, never the main thread."""
    if not TRAY_AVAILABLE:
        return None

    menu = pystray.Menu(
        pystray.MenuItem("Take a break now", lambda: on_break_now()),
        pystray.MenuItem("Quit", lambda: on_quit()),
    )
    icon = pystray.Icon("break-timer", _make_icon_image(), "Break Timer", menu)
    icon.run()
    return icon