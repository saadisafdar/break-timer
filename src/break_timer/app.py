"""
Break Timer - core application.

Waits `work_minutes` between breaks, then shows a centered on-screen
break card (countdown + progress bar + Cancel Break button), styled
after a teal "time for a break" notification design.
"""

import tkinter as tk
import time

TEAL = "#14b8a6"
TEAL_DARK = "#0d9488"
TEAL_TRACK = "#3fc9b8"
WHITE = "#ffffff"


class BreakTimerApp:
    def __init__(self, work_minutes=20, break_seconds=60, lines=None):
        self.work_ms = int(work_minutes * 60 * 1000)
        self.break_seconds = break_seconds
        self.lines = lines or ["Rest your eyes.", "Stretch your legs.", "Breathe. Relax."]

        self.root = tk.Tk()
        self.root.withdraw()  # main window is never shown

        self.popup = None
        self.progress_canvas = None
        self.progress_bar_id = None
        self.time_label = None
        self.break_end_time = None
        self.tick_job = None

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.schedule_next_break()

    # ---------- scheduling ----------

    def schedule_next_break(self, delay_ms=None):
        self.root.after(delay_ms if delay_ms is not None else self.work_ms, self.start_break)

    # ---------- break screen ----------

    def start_break(self):
        if self.popup is not None:
            try:
                self.popup.destroy()
            except tk.TclError:
                pass

        popup = tk.Toplevel(self.root)
        self.popup = popup
        popup.title("Break Time")
        popup.attributes("-topmost", True)
        popup.overrideredirect(True)
        popup.configure(bg=TEAL)

        width, height = 500, 210
        popup.update_idletasks()
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        card = tk.Frame(popup, bg=TEAL, padx=28, pady=22)
        card.pack(fill="both", expand=True)

        top_row = tk.Frame(card, bg=TEAL)
        top_row.pack(fill="x")

        title = tk.Label(
            top_row, text="Time for a break.", font=("Segoe UI", 20, "bold"),
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

        self.time_label = tk.Label(
            bottom_row, text=self._format_time(self.break_seconds),
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

        self.break_end_time = time.monotonic() + self.break_seconds
        self._tick()

    def _tick(self):
        remaining = self.break_end_time - time.monotonic()
        if remaining <= 0 or self.popup is None:
            self.end_break()
            return

        self.time_label.config(text=self._format_time(remaining))
        frac = remaining / self.break_seconds
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
        self.schedule_next_break()

    def end_break(self):
        self._close_popup()
        self.schedule_next_break()

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
