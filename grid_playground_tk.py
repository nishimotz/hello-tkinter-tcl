"""Interactive grid options playground (pure tkinter version).

Left side: option menus for grid options (row, column, sticky, columnspan,
rowspan, padx, pady, ipadx, ipady) plus per-column and per-row weight
controls for columnconfigure/rowconfigure.
Right side: a 4×4 grid with a target button whose grid geometry is
controlled by those options.

Uses only ``tk`` widgets (no ``ttk``) so the demo stays visually consistent
regardless of the platform theme.

Run with:  python grid_playground_tk.py
"""

from __future__ import annotations

import tkinter as tk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROW_VALUES = ["0", "1", "2", "3"]
COL_VALUES = ["0", "1", "2", "3"]
STICKY_VALUES = ["", "n", "s", "e", "w", "ns", "ew", "nsew", "ne", "nw", "se", "sw"]
COLSPAN_VALUES = ["1", "2", "3", "4"]
ROWSPAN_VALUES = ["1", "2", "3", "4"]
PAD_VALUES = ["0", "10", "20", "30", "40", "50"]

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

state: dict[str, str] = {
    "row": "0",
    "column": "0",
    "sticky": "",
    "columnspan": "1",
    "rowspan": "1",
    "padx": "0",
    "pady": "0",
    "ipadx": "0",
    "ipady": "0",
}

# Per-column and per-row weight (0 or 1) for columnconfigure/rowconfigure.
col_weights: list[str] = ["1", "1", "1", "1"]
row_weights: list[str] = ["1", "1", "1", "1"]

target_button: tk.Button | None = None
cell_labels: list[list[tk.Label]] = []  # 4×4 grid of cell labels

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _highlight_occupied_cells() -> None:
    """Highlight cells occupied by the target button based on row/col/span."""
    if not cell_labels:
        return
    r = int(state["row"])
    c = int(state["column"])
    cs = int(state["columnspan"])
    rs = int(state["rowspan"])

    for ri in range(4):
        for ci in range(4):
            if r <= ri < r + rs and c <= ci < c + cs:
                cell_labels[ri][ci].configure(bg="lightblue", fg="black")
            else:
                cell_labels[ri][ci].configure(bg="white", fg="lightgray")


def _apply_grid_options(
    *,
    row: str | None = None,
    column: str | None = None,
    sticky: str | None = None,
    columnspan: str | None = None,
    rowspan: str | None = None,
    padx: str | None = None,
    pady: str | None = None,
    ipadx: str | None = None,
    ipady: str | None = None,
) -> None:
    """Re-grid the target button using the current option values."""
    if target_button is None:
        return
    r = int(row if row is not None else state["row"])
    c = int(column if column is not None else state["column"])
    s = sticky if sticky is not None else state["sticky"]
    cs = int(columnspan if columnspan is not None else state["columnspan"])
    rs = int(rowspan if rowspan is not None else state["rowspan"])
    px = int(padx if padx is not None else state["padx"])
    py = int(pady if pady is not None else state["pady"])
    ipx = int(ipadx if ipadx is not None else state["ipadx"])
    ipy = int(ipady if ipady is not None else state["ipady"])
    target_button.grid_configure(
        row=r,
        column=c,
        sticky=s,
        columnspan=cs,
        rowspan=rs,
        padx=px,
        pady=py,
        ipadx=ipx,
        ipady=ipy,
    )
    _highlight_occupied_cells()


def _apply_weights() -> None:
    """Apply columnconfigure/rowconfigure weights to the preview frame."""
    if target_button is None:
        return
    parent = target_button.master
    for ci, w in enumerate(col_weights):
        parent.columnconfigure(ci, weight=int(w))
    for ri, w in enumerate(row_weights):
        parent.rowconfigure(ri, weight=int(w))


def _make_weight_row(
    parent: tk.Widget,
    row: int,
    label_text: str,
    index: int,
    weight_list: list[str],
) -> None:
    """Create a label + OptionMenu row for a single column/row weight."""
    lbl = tk.Label(parent, text=label_text, anchor="e")
    lbl.grid(row=row, column=0, sticky="e", padx=(8, 4), pady=2)

    var = tk.StringVar(value=weight_list[index])
    om = tk.OptionMenu(parent, var, "0", "1", "2")
    om.grid(row=row, column=1, sticky="ew", padx=(0, 8), pady=2)

    def on_change(
        *_args: object,
        _i: int = index,
        _wl: list[str] = weight_list,
        _var: tk.StringVar = var,
    ) -> None:
        _wl[_i] = _var.get()
        _apply_weights()

    var.trace_add("write", on_change)


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

    def on_change(
        *_args: object, _key: str = key, _var: tk.StringVar = var
    ) -> None:
        val = _var.get()
        state[_key] = val
        _apply_grid_options(**{_key: val})  # type: ignore[arg-type]

    var.trace_add("write", on_change)


# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("grid options playground (pure tkinter)")
root.geometry("800x720")
root.minsize(560, 600)

# -- Main grid frame -------------------------------------------------------
grid_frame = tk.Frame(root)
grid_frame.pack(fill="both", expand=True)
grid_frame.columnconfigure(0, weight=0)  # labels
grid_frame.columnconfigure(1, weight=1)  # option menus
grid_frame.columnconfigure(2, weight=3)  # preview

TOTAL_ROWS = 19  # 9 options + 2 separators + 4 col weights + 4 row weights
for r in range(TOTAL_ROWS):
    grid_frame.rowconfigure(r, weight=1)

# -- Left side: label + OptionMenu rows ------------------------------------
_make_option_row(grid_frame, 0, "row:", ROW_VALUES, "row")
_make_option_row(grid_frame, 1, "column:", COL_VALUES, "column")
_make_option_row(grid_frame, 2, "sticky:", STICKY_VALUES, "sticky")
_make_option_row(grid_frame, 3, "columnspan:", COLSPAN_VALUES, "columnspan")
_make_option_row(grid_frame, 4, "rowspan:", ROWSPAN_VALUES, "rowspan")
_make_option_row(grid_frame, 5, "padx:", PAD_VALUES, "padx")
_make_option_row(grid_frame, 6, "pady:", PAD_VALUES, "pady")
_make_option_row(grid_frame, 7, "ipadx:", PAD_VALUES, "ipadx")
_make_option_row(grid_frame, 8, "ipady:", PAD_VALUES, "ipady")

# -- Column weight controls ------------------------------------------------
tk.Label(grid_frame, text="--- col weight ---", anchor="w").grid(
    row=9, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 2)
)
_make_weight_row(grid_frame, 10, "col 0:", 0, col_weights)
_make_weight_row(grid_frame, 11, "col 1:", 1, col_weights)
_make_weight_row(grid_frame, 12, "col 2:", 2, col_weights)
_make_weight_row(grid_frame, 13, "col 3:", 3, col_weights)

# -- Row weight controls ---------------------------------------------------
tk.Label(grid_frame, text="--- row weight ---", anchor="w").grid(
    row=14, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 2)
)
_make_weight_row(grid_frame, 15, "row 0:", 0, row_weights)
_make_weight_row(grid_frame, 16, "row 1:", 1, row_weights)
_make_weight_row(grid_frame, 17, "row 2:", 2, row_weights)
_make_weight_row(grid_frame, 18, "row 3:", 3, row_weights)

# -- Right side: preview frame with 4x4 grid + target button ---------------
target_frame = tk.Frame(grid_frame, relief="solid", borderwidth=1, bg="gray")
target_frame.grid(row=0, column=2, rowspan=TOTAL_ROWS, sticky="nsew", padx=8, pady=8)

# Configure 4x4 grid with initial weights (all 1)
for r in range(4):
    target_frame.rowconfigure(r, weight=1)
for c in range(4):
    target_frame.columnconfigure(c, weight=1)

# Create cell labels to show grid boundaries (placed first so they stay
# behind the target button).  Stored in cell_labels for highlight updates.
for r in range(4):
    row_labels: list[tk.Label] = []
    for c in range(4):
        cell = tk.Label(
            target_frame,
            text=f" {r},{c} ",
            relief="solid",
            borderwidth=1,
            bg="white",
            fg="lightgray",
            anchor="nw",
        )
        cell.grid(row=r, column=c, sticky="nsew")
        row_labels.append(cell)
    cell_labels.append(row_labels)

# Target button (placed after cell labels so it renders on top)
target_button = tk.Button(
    target_frame,
    text="target",
    relief="solid",
    bd=2,
    bg="lightblue",
)
target_button.grid(row=0, column=0)
_apply_grid_options()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root.mainloop()
