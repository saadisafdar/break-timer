import argparse
import sys
import threading

from .app import BreakTimerApp
from .tray import TRAY_AVAILABLE


def main():
    parser = argparse.ArgumentParser(description="Lightweight desktop break reminder timer")
    parser.add_argument("--work", type=float, default=20,
                         help="Minutes between breaks (default: 20)")
    parser.add_argument("--break-seconds", type=int, default=60,
                         help="How long the break screen stays up, in seconds (default: 60)")
    parser.add_argument("--lines", type=str, nargs="*", default=None,
                         help="Custom lines shown on the break screen")
    parser.add_argument("--no-tray", action="store_true",
                         help="Disable the system tray icon")
    args = parser.parse_args()

    app = BreakTimerApp(
        work_minutes=args.work,
        break_seconds=args.break_seconds,
        lines=args.lines,
    )

    tray_icon_holder = {}

    if TRAY_AVAILABLE and not args.no_tray:
        def quit_app():
            if tray_icon_holder.get("icon"):
                tray_icon_holder["icon"].stop()
            app.root.after(0, app.root.destroy)

        def break_now():
            app.root.after(0, app.start_break)

        def start_tray():
            icon = None
            try:
                import pystray
                from .tray import _make_icon_image
                menu = pystray.Menu(
                    pystray.MenuItem("Take a break now", lambda: break_now()),
                    pystray.MenuItem("Quit", lambda: quit_app()),
                )
                icon = pystray.Icon("break-timer", _make_icon_image(), "Break Timer", menu)
                tray_icon_holder["icon"] = icon
                icon.run()
            except Exception:
                pass  # No usable tray backend on this system - app still runs fine without it

        threading.Thread(target=start_tray, daemon=True).start()

    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)