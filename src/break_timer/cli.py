import argparse
import sys

from .app import BreakTimerApp


def main():
    parser = argparse.ArgumentParser(description="Lightweight desktop break reminder timer")
    parser.add_argument("--work", type=float, default=20,
                         help="Minutes between breaks (default: 20)")
    parser.add_argument("--break-seconds", type=int, default=60,
                         help="How long the break screen stays up, in seconds (default: 60)")
    parser.add_argument("--lines", type=str, nargs="*", default=None,
                         help="Custom lines shown on the break screen")
    args = parser.parse_args()

    app = BreakTimerApp(
        work_minutes=args.work,
        break_seconds=args.break_seconds,
        lines=args.lines,
    )
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
