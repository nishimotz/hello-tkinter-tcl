"""Interactive pack options playground (pure tkinter, 3 buttons).

Three buttons are packed into a frame in order.  Each button has its own
``side``, ``fill``, ``expand`` and ``anchor`` option menus, so you can watch
how pack consumes the available space one widget at a time: every time a
button is packed, the remaining area shrinks and the next options are applied
to that *remaining* area.

Run with:  python pack_side_playground.py
"""

from __future__ import annotations

import tkinter as tk

SIDE_VALUES = ["top", "bottom", "left", "right"]
FILL_VALUES = ["none", "x", "y", "both"]
EXPAND_VALUES = ["False", "True"]
ANCHOR_VALUES = [
    "n", "s", "e", "w", "center",
    "ne", "nw", "se", "sw",
]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

# pack options for each of the three buttons, in pack order.
options: list[dict[str, str]] = [
    {"side": "top", "fill": "none", "expand": "False", "anchor": "center"},
    {"side": "top", "fill": "none", "expand": "False", "anchor": "center"},
    {"side": "left", "fill": "none", "expand": "False", "anchor": "center"},
]

buttons: list[tk.Button] = []


def _repack() -> None:
    """Re-pack all buttons in order using the current option values."""
    for btn, opt in zip(buttons, options):
        btn.pack_configure(
            side=opt["side"],
            fill=opt["fill"],
            expand=opt["expand"] == "True",
            anchor=opt["anchor"],
        )


def _make_option_row(
    parent: tk.Widget,
    row: int,
    label_text: str,
    index: int,
    key: str,
    values: list[str],
) -> None:
    """Create a label + OptionMenu row controlling button *index*'s *key*."""
    lbl = tk.Label(parent, text=label_text, anchor="e")
    lbl.grid(row=row, column=0, sticky="e", padx=(8, 4), pady=2)

    var = tk.StringVar(value=options[index][key])
    om = tk.OptionMenu(parent, var, *values)
    om.grid(row=row, column=1, sticky="ew", padx=(0, 8), pady=2)

    def on_change(*_args: object, _i: int = index, _k: str = key, _var: tk.StringVar = var) -> None:
        options[_i][_k] = _var.get()
        _repack()

    var.trace_add("write", on_change)


# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("pack options playground (pure tkinter, 3 buttons)")
root.geometry("760x560")
root.minsize(560, 480)

# -- Left side: option menus for each button -------------------------------
controls = tk.Frame(root)
controls.pack(side="left", fill="y", padx=8, pady=8)
controls.columnconfigure(0, weight=0)
controls.columnconfigure(1, weight=1)

row = 0
for i in range(3):
    tk.Label(controls, text=f"--- button {i + 1} ---", anchor="w").grid(
        row=row, column=0, columnspan=2, sticky="w", pady=(8, 2)
    )
    row += 1
    _make_option_row(controls, row, "side:", i, "side", SIDE_VALUES); row += 1
    _make_option_row(controls, row, "fill:", i, "fill", FILL_VALUES); row += 1
    _make_option_row(controls, row, "expand:", i, "expand", EXPAND_VALUES); row += 1
    _make_option_row(controls, row, "anchor:", i, "anchor", ANCHOR_VALUES); row += 1

# -- Right side: preview frame with three buttons --------------------------
preview = tk.Frame(root, relief="solid", borderwidth=1, bg="gray")
preview.pack(side="left", fill="both", expand=True, padx=8, pady=8)

buttons = [
    tk.Button(preview, text="button 1", bg="#ffd0d0"),
    tk.Button(preview, text="button 2", bg="#d0ffd0"),
    tk.Button(preview, text="button 3", bg="#d0d0ff"),
]
_repack()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root.mainloop()
