"""Interactive pack options playground (pure tkinter version).

Left side: eight option menus to choose pack options (side, fill, expand,
anchor, padx, pady, ipadx, ipady).
Right side: a frame containing a button whose pack geometry is controlled
by those options.

Uses only ``tk`` widgets (no ``ttk``) so the demo stays visually consistent
regardless of the platform theme.

Run with:  python pack_playground.py
"""

from __future__ import annotations

import tkinter as tk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SIDE_VALUES = ["top", "bottom", "left", "right"]
FILL_VALUES = ["none", "x", "y", "both"]
EXPAND_VALUES = ["False", "True"]
ANCHOR_VALUES = [
    "n", "s", "e", "w", "center",
    "ne", "nw", "se", "sw",
]
PAD_VALUES = ["0", "10", "20", "30", "40", "50"]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

state: dict[str, str] = {
    "side": "top",
    "fill": "none",
    "expand": "False",
    "anchor": "center",
    "padx": "0",
    "pady": "0",
    "ipadx": "0",
    "ipady": "0",
}

target_button: tk.Button | None = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _apply_pack_options(
    *,
    side: str | None = None,
    fill: str | None = None,
    expand: str | None = None,
    anchor: str | None = None,
    padx: str | None = None,
    pady: str | None = None,
    ipadx: str | None = None,
    ipady: str | None = None,
) -> None:
    """Re-pack the target button using the current combobox values."""
    if target_button is None:
        return
    s = side if side is not None else state["side"]
    f = fill if fill is not None else state["fill"]
    e = (expand if expand is not None else state["expand"]) == "True"
    a = anchor if anchor is not None else state["anchor"]
    px = int(padx if padx is not None else state["padx"])
    py = int(pady if pady is not None else state["pady"])
    ipx = int(ipadx if ipadx is not None else state["ipadx"])
    ipy = int(ipady if ipady is not None else state["ipady"])
    target_button.pack_configure(
        side=s, fill=f, expand=e, anchor=a,
        padx=px, pady=py, ipadx=ipx, ipady=ipy,
    )


def _make_option_row(
    parent: tk.Widget,
    row: int,
    label_text: str,
    values: list[str],
    key: str,
) -> None:
    """Create a label + OptionMenu row in *parent* at grid *row*."""
    lbl = tk.Label(parent, text=label_text, anchor="e")
    lbl.grid(row=row, column=0, sticky="e", padx=(8, 4), pady=4)

    var = tk.StringVar(value=state[key])
    om = tk.OptionMenu(parent, var, *values)
    om.grid(row=row, column=1, sticky="ew", padx=(0, 8), pady=4)

    def on_change(*_args: object, _key: str = key, _var: tk.StringVar = var) -> None:
        val = _var.get()
        state[_key] = val
        _apply_pack_options(**{_key: val})  # type: ignore[arg-type]

    var.trace_add("write", on_change)

# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("pack options playground (pure tkinter)")
root.geometry("720x560")
root.minsize(480, 400)

# -- Main grid frame -------------------------------------------------------
grid_frame = tk.Frame(root)
grid_frame.pack(fill="both", expand=True)
grid_frame.columnconfigure(0, weight=0)  # labels
grid_frame.columnconfigure(1, weight=1)  # option menus
grid_frame.columnconfigure(2, weight=3)  # preview
for r in range(8):
    grid_frame.rowconfigure(r, weight=1)

# -- Left side: label + OptionMenu rows ------------------------------------
_make_option_row(grid_frame, 0, "side:", SIDE_VALUES, "side")
_make_option_row(grid_frame, 1, "fill:", FILL_VALUES, "fill")
_make_option_row(grid_frame, 2, "expand:", EXPAND_VALUES, "expand")
_make_option_row(grid_frame, 3, "anchor:", ANCHOR_VALUES, "anchor")
_make_option_row(grid_frame, 4, "padx:", PAD_VALUES, "padx")
_make_option_row(grid_frame, 5, "pady:", PAD_VALUES, "pady")
_make_option_row(grid_frame, 6, "ipadx:", PAD_VALUES, "ipadx")
_make_option_row(grid_frame, 7, "ipady:", PAD_VALUES, "ipady")

# -- Right side: preview frame + target button -----------------------------
target_frame = tk.Frame(grid_frame, relief="solid", borderwidth=1, bg="gray")
target_frame.grid(row=0, column=2, rowspan=8, sticky="nsew", padx=8, pady=8)
target_frame.columnconfigure(0, weight=1)
target_frame.rowconfigure(0, weight=1)

target_button = tk.Button(
    target_frame,
    text="target button",
    relief="solid",
    bd=1,
)
target_button.pack()
_apply_pack_options()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root.mainloop()
