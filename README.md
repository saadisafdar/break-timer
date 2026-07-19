# Break Timer

A tiny, lightweight desktop break reminder. Runs quietly in the background and
shows a clean on-screen break card at whatever interval you set — countdown,
progress bar, and a one-click "Cancel Break" if you need to skip it.

## Install

### Option 1: Download and run (no Python needed)

Grab the file for your OS from the [Releases page](../../releases):

- **Windows** — `break-timer-windows.exe`
- **macOS** — `break-timer-macos`
- **Linux** — `break-timer-linux`

Double-click to run (macOS/Linux may need `chmod +x break-timer-macos` first,
and macOS Gatekeeper may ask you to allow it in System Settings → Privacy & Security).

### Option 2: Install with pip (if you have Python)

```bash
pip install git+https://github.com/saadisafdar/break-timer.git
break-timer
```

## Usage

```bash
break-timer                          # default: break every 20 minutes, 60s break screen
break-timer --work 25 --break-seconds 90
break-timer --lines "Look away." "Drink water." "Sit up straight."
```

| Flag | Description | Default |
|---|---|---|
| `--work` | Minutes between breaks | 20 |
| `--break-seconds` | How long the break screen stays up | 60 |
| `--lines` | Custom message lines on the break screen | Rest your eyes. / Stretch your legs. / Breathe. Relax. |

## Run it automatically at login (optional)

**Windows:** Press `Win+R` → `shell:startup` → Enter. Add a shortcut targeting
the `.exe`, or if installed via pip, targeting `break-timer.exe` in your
Python Scripts folder.

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
