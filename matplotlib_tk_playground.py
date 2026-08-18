# /// script
# dependencies = [
#     "matplotlib>=3.10",
#     "numpy>=2.0",
# ]
# ///

"""Interactive Matplotlib & Tkinter Integration Playground.

Demonstrates how to embed Matplotlib plots into a Tkinter GUI application using
FigureCanvasTkAgg and NavigationToolbar2Tk. Provides interactive controls
(waveform selection, frequency, amplitude, noise) on the left panel that
dynamically update the plot on the right panel in real time.

Prerequisites:
    uv run --extra matplotlib -- python matplotlib_tk_playground.py
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

try:
    import numpy as np
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg,
        NavigationToolbar2Tk,
    )
    from matplotlib.figure import Figure
except ImportError as err:
    print(
        f"Missing required dependency: {err}\n"
        "Please run this script with uv:\n"
        "    uv run --extra matplotlib -- python matplotlib_tk_playground.py",
        file=sys.stderr,
    )
    # If run in a Tk environment, also show a graphical alert
    try:
        _root = tk.Tk()
        _root.withdraw()
        messagebox.showerror(
            "Missing Dependencies",
            "This script requires 'matplotlib' and 'numpy'.\n\n"
            "Please run via uv:\n"
            "uv run --extra matplotlib -- python matplotlib_tk_playground.py",
        )
    except Exception:
        pass
    sys.exit(1)


class MatplotlibTkPlayground:
    """Interactive GUI application showcasing Matplotlib + Tkinter integration."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tkinter + Matplotlib Integration Playground")
        self.root.geometry("900x600")
        self.root.minsize(700, 480)

        # Controls State
        self.wave_type_var = tk.StringVar(value="Sine")
        self.freq_var = tk.DoubleVar(value=2.0)
        self.amp_var = tk.DoubleVar(value=1.0)
        self.noise_var = tk.BooleanVar(value=False)

        self._build_ui()
        self._plot_signal()

    def _build_ui(self) -> None:
        # Main container with 2 columns
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel: Controls (Fixed width / side=left)
        controls_frame = tk.LabelFrame(
            main_frame, text=" Signal Controls ", padx=10, pady=10
        )
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # 1. Waveform selector
        tk.Label(controls_frame, text="Waveform Type:", anchor="w").pack(
            fill=tk.X, pady=(5, 2)
        )
        wave_options = ["Sine", "Cosine", "Square", "Sawtooth"]
        wave_menu = tk.OptionMenu(
            controls_frame,
            self.wave_type_var,
            *wave_options,
            command=lambda _: self._plot_signal(),
        )
        wave_menu.pack(fill=tk.X, pady=(0, 10))

        # 2. Frequency slider
        tk.Label(controls_frame, text="Frequency (Hz):", anchor="w").pack(
            fill=tk.X, pady=(5, 2)
        )
        freq_scale = tk.Scale(
            controls_frame,
            from_=0.5,
            to=10.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.freq_var,
            command=lambda _: self._plot_signal(),
        )
        freq_scale.pack(fill=tk.X, pady=(0, 10))

        # 3. Amplitude slider
        tk.Label(controls_frame, text="Amplitude:", anchor="w").pack(
            fill=tk.X, pady=(5, 2)
        )
        amp_scale = tk.Scale(
            controls_frame,
            from_=0.1,
            to=3.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.amp_var,
            command=lambda _: self._plot_signal(),
        )
        amp_scale.pack(fill=tk.X, pady=(0, 10))

        # 4. Add Noise Checkbutton
        noise_check = tk.Checkbutton(
            controls_frame,
            text="Add Random Noise",
            variable=self.noise_var,
            command=self._plot_signal,
        )
        noise_check.pack(anchor="w", pady=(5, 15))

        # 5. Reset Button
        reset_btn = tk.Button(
            controls_frame,
            text="Reset Parameters",
            command=self._reset_params,
            bg="#f0f0f0",
        )
        reset_btn.pack(fill=tk.X, pady=5)

        # Right panel: Matplotlib Canvas (Expandable / side=right)
        plot_frame = tk.Frame(main_frame, bg="white", relief=tk.SUNKEN, bd=1)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Matplotlib Figure & Subplot
        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # Embed Figure into Tkinter via FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add Matplotlib Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()

    def _generate_signal(self) -> tuple[np.ndarray, np.ndarray]:
        t = np.linspace(0, 2.0, 1000)
        freq = self.freq_var.get()
        amp = self.amp_var.get()
        wave = self.wave_type_var.get()

        if wave == "Sine":
            y = amp * np.sin(2 * np.pi * freq * t)
        elif wave == "Cosine":
            y = amp * np.cos(2 * np.pi * freq * t)
        elif wave == "Square":
            y = amp * np.sign(np.sin(2 * np.pi * freq * t))
        elif wave == "Sawtooth":
            y = amp * (2 * (t * freq - np.floor(0.5 + t * freq)))
        else:
            y = np.zeros_like(t)

        if self.noise_var.get():
            noise = np.random.normal(0, 0.2 * amp, size=t.shape)
            y += noise

        return t, y

    def _plot_signal(self, *_args: object) -> None:
        """Clear and redraw the plot with current parameter settings."""
        t, y = self._generate_signal()

        self.ax.clear()
        self.ax.plot(t, y, color="#1f77b4", linewidth=2, label=self.wave_type_var.get())
        self.ax.set_title(
            f"Signal Plot ({self.wave_type_var.get()} @ {self.freq_var.get():.1f} Hz)",
            fontsize=12,
            fontweight="bold",
        )
        self.ax.set_xlabel("Time [seconds]")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_ylim(-4.0, 4.0)
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend(loc="upper right")

        # Redraw canvas
        self.canvas.draw_idle()

    def _reset_params(self) -> None:
        self.wave_type_var.set("Sine")
        self.freq_var.set(2.0)
        self.amp_var.set(1.0)
        self.noise_var.set(False)
        self._plot_signal()


def main() -> None:
    root = tk.Tk()
    MatplotlibTkPlayground(root)
    root.mainloop()


if __name__ == "__main__":
    main()
