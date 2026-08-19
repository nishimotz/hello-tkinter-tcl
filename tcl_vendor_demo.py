# /// script
# dependencies = []
# ///

"""Tcl パッケージ（demobox）を vendoring して使うデモ（純 tkinter 版）。

素の tkinter だけで「Tcl エコシステムの拡張を vendoring して使う」
仕組みを示す。

1. **拡張性**: リポジトリ内の ``vendor/demobox`` に置いた Tcl パッケージを
   ``package require demobox`` で読み込み、tkinter の Canvas ウィジェットに
   アニメーション機能を追加する。素の tkinter には無い機能を、
   Tcl エコシステムのパッケージ流通（pkgIndex.tcl + .tm）で補っている。

   - ``pkgIndex.tcl`` 経由のパッケージ方式: auto_path に追加したディレクトリの
     pkgIndex.tcl が ``package ifneeded demobox 1.0`` でロード方法を提供する。
   - 実は ``.tm`` モジュール単体でも動く: ファイル名の命名規則
     ``<name>-<version>.tm``（ここでは demobox-1.0.tm）に従っていれば、
     ``::tcl::tm::path`` にディレクトリを追加するだけで ``package require``
     が解決できる。pkgIndex.tcl は「パッケージ」として配布する際の
     索引であり、必須ではない。

2. **性能改善**: アニメーションループは ``demobox`` 内部の Tcl ``after``
   で回す。Python のイベントループをブロックせず、canvas アニメも
   Tcl 側に置けば滑らか。

レイアウトは pack で「上 = Canvas、中 = ボタン横一列、下 = ステータス」。
demobox はその既存 Canvas を再利用してボールを描画する。

Run with:  python tcl_vendor_demo.py
"""

from __future__ import annotations

from pathlib import Path

import tkinter as tk

# リポジトリルートからの vendor ディレクトリの絶対パス。
_VENDOR = str(Path(__file__).resolve().parent / "vendor" / "demobox")

# ---------------------------------------------------------------------------
# Build UI
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("Tcl パッケージを vendoring して使う（demobox）")
root.geometry("720x600")
root.minsize(600, 480)

# -- 上: Canvas（demobox が描画するボールの舞台） ---------------------------
stage = tk.Canvas(root, width=640, height=400, bg="white", highlightthickness=0)
stage.pack(fill="both", expand=True, padx=8, pady=(8, 4))

# -- 中: ボタン横一列 -------------------------------------------------------
button_bar = tk.Frame(root)
button_bar.pack(fill="x", padx=8, pady=4)

start_btn = tk.Button(button_bar, text="開始", command=lambda: _start())
add_btn = tk.Button(button_bar, text="ボール追加 +30", command=lambda: _add())
stop_btn = tk.Button(button_bar, text="停止", command=lambda: _stop())
speed_btn = tk.Button(button_bar, text="高速化 (120fps)", command=lambda: _speed())
for b in (start_btn, add_btn, stop_btn, speed_btn):
    b.pack(side="left", padx=(0, 8))

# -- 下: ステータス ----------------------------------------------------------
status = tk.Label(
    root,
    text="開始で60個のボールをアニメーション。追加でさらに増やす",
    anchor="w",
    fg="#666666",
)
status.pack(fill="x", padx=8, pady=(4, 8))

# ---------------------------------------------------------------------------
# Tcl 呼び出しヘルパー
# ---------------------------------------------------------------------------

def _tcl_canvas_path() -> str:
    """stage Canvas に対応する Tcl パス名を返す。"""
    return str(stage.winfo_pathname(stage.winfo_id()))


def _run_tcl(script: str, **subst: str) -> None:
    """Tcl インタープリタ上でスクリプトを実行する（{key} を置換）。"""
    for key, val in subst.items():
        script = script.replace("{" + key + "}", val)
    root.tk.eval(script)


def _set_status(text: str) -> None:
    status.config(text=text)


def _start() -> None:
    _run_tcl("demobox::start {path} 60 60", path=_tcl_canvas_path())
    _set_status("アニメーション開始（Tcl after 60fps / 60ボール）")


def _add() -> None:
    _run_tcl("demobox::add {path} 30", path=_tcl_canvas_path())
    _set_status("ボールを30個追加")


def _stop() -> None:
    _run_tcl("demobox::stop {path}", path=_tcl_canvas_path())
    _set_status("停止")


def _speed() -> None:
    _run_tcl("demobox::speed {path} 120", path=_tcl_canvas_path())
    _set_status("120fps に変更")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # vendored パッケージを auto_path に追加して require する。
    # ここは pkgIndex.tcl 経由（パッケージ）の読み込み。
    root.tk.eval(f"lappend auto_path {{{_VENDOR}}}")
    root.tk.eval("package require demobox")
    # モジュール（.tm）だけで動かすなら、pkgIndex.tcl は不要で下記で足りる:
    #   root.tk.eval(f"lappend ::tcl::tm::path {{{_VENDOR}}}")
    #   root.tk.eval("package require demobox")
    root.lift()
    root.focus_force()
    root.mainloop()
