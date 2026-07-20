"""
Break Timer - core application.

Waits `work_seconds` between breaks, then shows a centered on-screen
break card (countdown + progress bar + Cancel Break button), styled
after a teal "time for a break" notification design. Driven by a
config dict (see config.py) so settings can be changed live from the
Settings window without restarting the app.
"""

import tkinter as tk
import time

from . import audio
from .config import DEFAULT_CONFIG

TEAL = "#14b8a6"
TEAL_DARK = "#0d9488"
TEAL_TRACK = "#3fc9b8"
WHITE = "#ffffff"


class BreakTimerApp:
    def __init__(self, config=None):
        self.config = dict(DEFAULT_CONFIG)
        if config:
            self.config.update(config)

        self.root = tk.Tk()
        self.root.withdraw()  # main window is never shown

        self.popup = None
        self.progress_canvas = None
        self.progress_bar_id = None
        self.time_label = None
        self.break_end_time = None
        self.tick_job = None
        self.next_break_job = None

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self._reschedule()

    # ---------- config ----------

    @property
    def lines(self):
        return [l for l in self.config["message"].split("\n") if l.strip()] or [""]

    def apply_config(self, new_config):
        """Called from the Settings window. Applies changes immediately."""
        was_enabled = self.config.get("enabled", True)
        self.config.update(new_config)
        now_enabled = self.config.get("enabled", True)

        if self.next_break_job is not None:
            try:
                self.root.after_cancel(self.next_break_job)
            except (ValueError, tk.TclError):
                pass
            self.next_break_job = None

        if now_enabled:
            self._reschedule()
        elif was_enabled and not now_enabled:
            # Turned off - also close any break in progress
            self._close_popup()

    # ---------- scheduling ----------

    def _reschedule(self, delay_ms=None):
        if not self.config.get("enabled", True):
            return
        if delay_ms is None:
            delay_ms = int(self.config["work_seconds"] * 1000)
        self.next_break_job = self.root.after(delay_ms, self.start_break)

    # ---------- break screen ----------

    def start_break(self):
        if self.popup is not None:
            try:
                self.popup.destroy()
            except tk.TclError:
                pass

        audio.play_sound(self.config.get("sound", "None"))

        popup = tk.Toplevel(self.root)
        self.popup = popup
        popup.title("Break Time")
        popup.attributes("-topmost", True)
        popup.overrideredirect(True)
        popup.configure(bg=TEAL)

        width = 500
        card = tk.Frame(popup, bg=TEAL, padx=28, pady=22)
        card.pack(fill="both", expand=True)

        top_row = tk.Frame(card, bg=TEAL)
        top_row.pack(fill="x")

        title = tk.Label(
            top_row, text=self.config.get("title", "Time for a break."),
            font=("Segoe UI", 20, "bold"),
            bg=TEAL, fg=WHITE, anchor="w"
        )
        title.pack(side="left")

        cancel_btn = tk.Button(
            top_row, text="Cancel Break", command=self.cancel_break,
            bg=WHITE, fg=TEAL_DARK, relief="flat", padx=12, pady=6,
            font=("Segoe UI", 9, "bold"), activebackground="#eafaf7",
            activeforeground=TEAL_DARK, cursor="hand2", bd=0
        )
        cancel_btn.pack(side="right")

        body = tk.Frame(card, bg=TEAL)
        body.pack(fill="x", pady=(18, 8))
        for line in self.lines:
            tk.Label(
                body, text=line, font=("Segoe UI", 12), bg=TEAL, fg=WHITE, anchor="w"
            ).pack(anchor="w", pady=1)

        bottom_row = tk.Frame(card, bg=TEAL)
        bottom_row.pack(fill="x", pady=(14, 0))

        break_seconds = self.config["break_seconds"]
        self.time_label = tk.Label(
            bottom_row, text=self._format_time(break_seconds),
            font=("Segoe UI", 11), bg=TEAL, fg=WHITE
        )
        self.time_label.pack(side="right")

        bar_wrap = tk.Frame(card, bg=TEAL_TRACK, height=6)
        bar_wrap.pack(fill="x", pady=(6, 0))
        bar_wrap.pack_propagate(False)

        self.progress_canvas = tk.Canvas(bar_wrap, bg=TEAL_TRACK, height=6, highlightthickness=0)
        self.progress_canvas.pack(fill="both", expand=True)
        self.progress_bar_id = self.progress_canvas.create_rectangle(
            0, 0, width - 56, 6, fill=WHITE, width=0
        )
        self._full_bar_width = width - 56

        popup.update_idletasks()
        height = card.winfo_reqheight()
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        self._break_total = break_seconds
        self.break_end_time = time.monotonic() + break_seconds
        self._tick()

    def _tick(self):
        remaining = self.break_end_time - time.monotonic()
        if remaining <= 0 or self.popup is None:
            self.end_break()
            return

        self.time_label.config(text=self._format_time(remaining))
        frac = remaining / self._break_total
        try:
            self.progress_canvas.coords(
                self.progress_bar_id, 0, 0, self._full_bar_width * frac, 6
            )
        except tk.TclError:
            return

        self.tick_job = self.root.after(200, self._tick)

    @staticmethod
    def _format_time(seconds):
        seconds = max(0, int(seconds))
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def cancel_break(self):
        self._close_popup()
        self._reschedule()

    def end_break(self):
        self._close_popup()
        self._reschedule()

    def _close_popup(self):
        if self.tick_job is not None:
            try:
                self.root.after_cancel(self.tick_job)
            except (ValueError, tk.TclError):
                pass
            self.tick_job = None
        if self.popup is not None:
            try:
                self.popup.destroy()
            except tk.TclError:
                pass
            self.popup = None

    def run(self):
        self.root.mainloop()
