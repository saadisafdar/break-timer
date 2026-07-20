# Break Timer

A tiny, lightweight desktop break reminder. Runs quietly in the system tray
and shows a clean on-screen break card at whatever interval you set —
countdown, progress bar, break sound, and a one-click "Cancel Break" if you
need to skip it. Fully configurable through a Settings window, no editing
config files by hand.

## Install

### Option 1: Download and run (no Python needed)

Grab the zip for your OS from the [Releases page](../../releases):

- **Windows** — `break-timer-windows.zip`
- **macOS** — `break-timer-macos.zip`
- **Linux** — `break-timer-linux.zip`

Extract it, then run the `break-timer` (or `break-timer.exe`) file inside the
extracted folder. Keep the whole folder together — the executable needs the
files next to it.

> **Windows SmartScreen/Defender note:** this is a small, unsigned
> open-source tool, so Windows may show a warning the first time you run it
> since it doesn't yet have an established reputation. Click **More info →
> Run anyway** if that happens. If Defender blocks the download outright,
> that's a known false-positive some antivirus engines have with Python
> packaged apps in general — the source code is fully open here for you to
> verify nothing's actually wrong.

macOS may ask you to allow it in **System Settings → Privacy & Security**
the first time (Gatekeeper, since it's unsigned).

### Option 2: Install with pip (if you have Python)

```bash
pip install git+https://github.com/saadisafdar/break-timer.git
break-timer
```

## Usage

Just run it — it lives in your system tray (bottom-right on Windows, near
the clock). Right-click the tray icon for:

- **Settings** — configure everything: break frequency, break length, title,
  message, and break sound (with a preview button), all applied instantly,
  no restart needed
- **Take a break now** — trigger a break immediately
- **Quit** — exit the app

If there's no system tray available (or you pass `--no-tray`), the Settings
window opens automatically on launch instead.

```bash
break-timer            # normal run, with tray icon
break-timer --no-tray   # run without a tray icon
```

Settings are saved to a per-user config file and persist across restarts.

## Run it automatically at login (optional)

**Windows:** Press `Win+R` → `shell:startup` → Enter. Add a shortcut to
`break-timer.exe` inside your extracted folder (or, if installed via pip,
to `break-timer.exe` in your Python Scripts folder).

**macOS:** System Settings → General → Login Items → add the app.

**Linux:** Add a `.desktop` file to `~/.config/autostart/`:

```ini
[Desktop Entry]
Type=Application
Exec=/path/to/break-timer
Name=Break Timer
```

## Development

```bash
git clone https://github.com/saadisafdar/break-timer.git
cd break-timer
pip install -e .
break-timer
```

Requires Python 3.8+ with tkinter (bundled by default on Windows/macOS
installers; on Linux, `sudo apt install python3-tk` if it's missing).

## License

MIT — see [LICENSE](LICENSE).
