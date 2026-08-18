# /// script
# dependencies = [
#     "pandastable>=0.13.1",
#     "pandas>=2.0",
# ]
# ///

"""Simple Pandastable & Tkinter Integration Example.

Demonstrates how to embed a Pandas DataFrame into a Tkinter window using 'pandastable'.

Prerequisites (run with uv):
    uv run --extra pandastable -- python pandastable_playground.py
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox

try:
    import pandas as pd
    from pandastable import Table
except ImportError as err:
    print(
        f"Missing required dependency: {err}\n"
        "Please run this script with uv:\n"
        "    uv run --extra pandastable -- python pandastable_playground.py",
        file=sys.stderr,
    )
    try:
        _root = tk.Tk()
        _root.withdraw()
        messagebox.showerror(
            "Missing Dependencies",
            "This script requires 'pandastable' and 'pandas'.\n\n"
            "Please run via uv:\n"
            "uv run --extra pandastable -- python pandastable_playground.py",
        )
    except Exception:
        pass
    sys.exit(1)


def main() -> None:
    root = tk.Tk()
    root.title("pandastable Simple Demo")
    root.geometry("650x400")

    # Main frame
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Sample DataFrame
    df = pd.DataFrame(
        {
            "Product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
            "Category": [
                "Electronics",
                "Accessories",
                "Accessories",
                "Electronics",
                "Audio",
            ],
            "Price ($)": [1200.0, 25.5, 75.0, 300.0, 150.0],
            "Stock": [15, 120, 45, 8, 30],
        }
    )

    # Embed Pandastable
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

    root.mainloop()


if __name__ == "__main__":
    main()
