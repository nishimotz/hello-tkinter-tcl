# /// script
# dependencies = []
# ///

"""tk.Button vs ttk.Button とテーマ切り替えの比較デモ。

macOS の Aqua テーマでは tk.Button の bg が無視される問題を、
テーマを切り替えながら視覚的に確認するためのデモ。

- 左側: テーマ選択（aqua / clam / alt / default / classic）
- 中央: tk.Button と ttk.Button の比較（bg 指定の有無）
- 右側: ttk のスタイルで色を変えたボタン

Run with:  python theme_playground.py
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("tk.Button vs ttk.Button / theme playground")
root.geometry("760x420")
root.minsize(600, 360)

# -- 上部: テーマ選択バー ---------------------------------------------------
theme_bar = ttk.Frame(root, padding=(8, 8))
theme_bar.pack(fill="x")

ttk.Label(theme_bar, text="Theme:").pack(side="left", padx=(0, 6))

theme_var = tk.StringVar(value=ttk.Style().theme_use())
theme_combo = ttk.Combobox(
    theme_bar,
    textvariable=theme_var,
    values=list(ttk.Style().theme_names()),
    state="readonly",
    width=12,
)
theme_combo.pack(side="left")

# 現在のテーマを表示するラベル
theme_info = ttk.Label(theme_bar, text="", foreground="#666666")
theme_info.pack(side="left", padx=(12, 0))

# -- メイン: 3 つの比較カラム ------------------------------------------------
main = ttk.Frame(root, padding=(8, 8))
main.pack(fill="both", expand=True)

for c in range(3):
    main.columnconfigure(c, weight=1)

# 各カラムの見出し
ttk.Label(main, text="tk.Button (bg 指定)", font=("Helvetica", 12, "bold")).grid(
    row=0, column=0, pady=(0, 8)
)
ttk.Label(main, text="ttk.Button (style で色)", font=("Helvetica", 12, "bold")).grid(
    row=0, column=1, pady=(0, 8)
)
ttk.Label(main, text="ttk.Button (style.map で状態別色)", font=("Helvetica", 12, "bold")).grid(
    row=0, column=2, pady=(0, 8)
)

# 各カラムの説明
ttk.Label(
    main,
    text="bg は macOS では無視される",
    foreground="#888888",
    wraplength=200,
    justify="center",
).grid(row=1, column=0, pady=(0, 8), padx=4)
ttk.Label(
    main,
    text="style.configure で静的色を定義\n（赤 / アンバー / 青）",
    foreground="#888888",
    wraplength=200,
    justify="center",
).grid(row=1, column=1, pady=(0, 8), padx=4)
ttk.Label(
    main,
    text="style.map で状態別の色を定義\n（赤 / アンバー / 青、ホバーで色が変わる）",
    foreground="#888888",
    wraplength=200,
    justify="center",
).grid(row=1, column=2, pady=(0, 8), padx=4)

# -- カラム 0: tk.Button ----------------------------------------------------
col0 = ttk.Frame(main, padding=8)
col0.grid(row=2, column=0, sticky="nsew", padx=4)

tk.Button(col0, text="tk.Button (bg=red)", bg="red").pack(fill="x", pady=4)
tk.Button(col0, text="tk.Button (bg=#ffd54f)", bg="#ffd54f").pack(fill="x", pady=4)
tk.Button(col0, text="tk.Button (bg=lightblue)", bg="lightblue").pack(fill="x", pady=4)
tk.Button(col0, text="tk.Button (bg なし)").pack(fill="x", pady=4)

# -- カラム 1: ttk.Button (style で色) -------------------------------------
col1 = ttk.Frame(main, padding=8)
col1.grid(row=2, column=1, sticky="nsew", padx=4)

# カスタムスタイルを定義（テーマ切り替え時に再適用する）
def _configure_styles() -> None:
    style = ttk.Style()
    # カラム 1: style.configure で静的色を定義
    style.configure("Red.TButton", background="red", foreground="white")
    style.configure("Amber.TButton", background="#ffd54f", foreground="black")
    style.configure("Blue.TButton", background="lightblue", foreground="black")
    # カラム 2: style.map で状態別の色を定義（ホバー/押下で色が変わる）
    # カラム 1 と同じ Red/Amber/Blue の色を使う
    style.configure("HoverRed.TButton", background="red", foreground="white")
    style.map(
        "HoverRed.TButton",
        background=[
            ("pressed", "#8b0000"),   # 押下中: 濃い赤
            ("active", "#ff6666"),    # ホバー中: 明るい赤
            ("disabled", "#cccccc"),  # 無効: グレー
        ],
    )
    style.configure("HoverAmber.TButton", background="#ffd54f", foreground="black")
    style.map(
        "HoverAmber.TButton",
        background=[
            ("pressed", "#b8860b"),   # 押下中: 濃いアンバー
            ("active", "#ffe082"),    # ホバー中: 明るいアンバー
            ("disabled", "#cccccc"),  # 無効: グレー
        ],
    )
    style.configure("HoverBlue.TButton", background="lightblue", foreground="black")
    style.map(
        "HoverBlue.TButton",
        background=[
            ("pressed", "#4682b4"),   # 押下中: 濃い青
            ("active", "#b0e0e6"),    # ホバー中: 明るい青
            ("disabled", "#cccccc"),  # 無効: グレー
        ],
    )


_configure_styles()

ttk.Button(col1, text="Red.TButton", style="Red.TButton").pack(fill="x", pady=4)
ttk.Button(col1, text="Amber.TButton", style="Amber.TButton").pack(fill="x", pady=4)
ttk.Button(col1, text="Blue.TButton", style="Blue.TButton").pack(fill="x", pady=4)
ttk.Button(col1, text="default style").pack(fill="x", pady=4)

# -- カラム 2: ttk.Button (style.map で状態別色) -----------------------------
col2 = ttk.Frame(main, padding=8)
col2.grid(row=2, column=2, sticky="nsew", padx=4)

ttk.Button(col2, text="HoverRed.TButton", style="HoverRed.TButton").pack(fill="x", pady=4)
ttk.Button(col2, text="HoverAmber.TButton", style="HoverAmber.TButton").pack(fill="x", pady=4)
ttk.Button(col2, text="HoverBlue.TButton", style="HoverBlue.TButton").pack(fill="x", pady=4)
ttk.Button(col2, text="default style").pack(fill="x", pady=4)

# -- テーマ切り替え ---------------------------------------------------------


def _on_theme_change(*_args: object) -> None:
    theme = theme_var.get()
    ttk.Style().theme_use(theme)
    # テーマを切り替えるとスタイル定義がリセットされるため再適用
    _configure_styles()
    theme_info.config(text=f"current: {theme}")


theme_var.trace_add("write", _on_theme_change)
_on_theme_change()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    root.mainloop()
