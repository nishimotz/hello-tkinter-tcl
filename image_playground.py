#!/usr/bin/env python3
"""
image_playground.py

「Tcl/Tk における画像の使い方完全ガイド」のデモアプリ。

以下の画像表示パターンを体験できます：
- Label 表示（静的アイコン）
- Button 表示（画像付きボタン）
- Canvas 表示（自由な位置・重ね合わせ）
- リサイズ（subsample / Pillow）
- 透過 PNG 表示
- 実行中の Tk patchlevel 確認

画像ファイル:
    images/lemonpy3.png  : 全バージョンで利用可能
    images/lemonpy3.svg  : Tk 9.0 以降で標準対応
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Pillow は任意依存。無くても動作するが、高品質リサイズは使えない。
try:
    from PIL import Image, ImageTk
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


ASSET_DIR = os.path.join(os.path.dirname(__file__), "images")
PNG_PATH = os.path.join(ASSET_DIR, "lemonpy3.png")
SVG_PATH = os.path.join(ASSET_DIR, "lemonpy3.svg")


def get_patchlevel():
    """実行時の Tcl/Tk patchlevel を返す。"""
    return tk.Tcl().eval("info patchlevel")


def tk_version_tuple(patchlevel: str):
    """patchlevel 文字列から (major, minor, micro) タプルを取り出す。"""
    parts = patchlevel.split(".")
    major = int(parts[0])
    minor = int(parts[1])
    micro_str = parts[2]
    # micro にベータ表記（a1/b1/rc1 など）が付く場合があるため数字部分だけ取る
    micro = ""
    for ch in micro_str:
        if ch.isdigit():
            micro += ch
        else:
            break
    micro = int(micro) if micro else 0
    return (major, minor, micro)


def supports_svg(patchlevel: str) -> bool:
    return tk_version_tuple(patchlevel) >= (9, 0, 0)


class ImagePlayground(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Playground — Tcl/Tk 画像の使い方ガイド")
        self.geometry("900x700")

        self.patchlevel = get_patchlevel()
        self.images = {}  # 参照保持用

        self._build_header()
        self._build_notebook()
        self._build_footer()

    def _build_header(self):
        header = ttk.Frame(self, padding=10)
        header.pack(fill=tk.X)

        ttk.Label(
            header,
            text="🖼 Tcl/Tk 画像デモ",
            font=("Helvetica", 18, "bold"),
        ).pack(anchor=tk.W)

        info = ttk.Label(
            header,
            text=f"Tk patchlevel: {self.patchlevel}  —  SVG 標準読み込み: {'✅' if supports_svg(self.patchlevel) else '❌'}  —  Pillow: {'✅' if HAS_PILLOW else '❌'}",
            font=("Helvetica", 10),
        )
        info.pack(anchor=tk.W, pady=(5, 0))

    def _build_notebook(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 各タブ
        notebook.add(self._tab_label(), text="Label")
        notebook.add(self._tab_button(), text="Button")
        notebook.add(self._tab_canvas(), text="Canvas")
        notebook.add(self._tab_resize(), text="Resize")
        notebook.add(self._tab_transparent(), text="Transparent")
        notebook.add(self._tab_svg(), text="SVG")

        # タブ切り替え時の macOS/Tk 描画アーティファクトを抑制
        notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event=None):
        """タブ切り替え時に再描画を強制し、macOS/Tk の黒い線アーティファクトを抑制する。"""
        self.update_idletasks()
        # 全 Canvas を再描画
        for widget in self.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Canvas):
                    child.update_idletasks()

    def _keep_ref(self, name, img):
        """PhotoImage オブジェクトをガベージコレクトされないように保持。"""
        self.images[name] = img
        return img

    def _load_png(self, scale=1):
        """PNG を PhotoImage として読み込む。"""
        img = tk.PhotoImage(file=PNG_PATH)
        if scale != 1:
            img = img.subsample(scale, scale)
        return img

    def _tab_label(self):
        frame = ttk.Frame(self)

        desc = ttk.Label(
            frame,
            text="Label による静的画像表示。PhotoImage オブジェクトは参照を保持してください。",
            wraplength=600,
        )
        desc.pack(pady=10)

        img = self._keep_ref("label", self._load_png(scale=4))
        lbl = ttk.Label(frame, image=img)
        lbl.pack(pady=20)

        return frame

    def _tab_button(self):
        frame = ttk.Frame(self)

        desc = ttk.Label(
            frame,
            text="Button に画像を設定。クリックでメッセージを出力します。",
            wraplength=600,
        )
        desc.pack(pady=10)

        img = self._keep_ref("button", self._load_png(scale=4))
        btn = tk.Button(
            frame,
            image=img,
            text="Click me!",
            compound=tk.BOTTOM,
            command=lambda: print("Button clicked!"),
        )
        btn.pack(pady=20)

        return frame

    def _tab_canvas(self):
        frame = ttk.Frame(self)

        desc = ttk.Label(
            frame,
            text="Canvas 上に画像を自由な位置に配置。create_image で配置座標を指定できます。",
            wraplength=600,
        )
        desc.pack(pady=10)

        canvas = tk.Canvas(frame, width=600, height=400, bg="lightyellow")
        canvas.pack(pady=10)

        img = self._keep_ref("canvas", self._load_png(scale=4))
        canvas.create_image(300, 200, image=img, anchor=tk.CENTER)
        canvas.create_text(
            300,
            360,
            text="Canvas create_image(300, 200)",
            font=("Helvetica", 14),
            fill="black",
        )

        return frame

    def _tab_resize(self):
        frame = ttk.Frame(self)

        desc = ttk.Label(
            frame,
            text="左: subsample による縮小（整数倍のみ） / 右: Pillow による高品質リサイズ。",
            wraplength=600,
        )
        desc.pack(pady=10)

        container = ttk.Frame(frame)
        container.pack(pady=10)

        # 左: Tk 標準 subsample
        left = ttk.Frame(container)
        left.pack(side=tk.LEFT, padx=20)
        ttk.Label(left, text="subsample(8, 8)").pack()
        small = self._keep_ref("resize_subsample", self._load_png(scale=8))
        ttk.Label(left, image=small).pack()

        # 右: Pillow リサイズ
        right = ttk.Frame(container)
        right.pack(side=tk.LEFT, padx=20)
        ttk.Label(right, text="Pillow LANCZOS 120x120").pack()
        if HAS_PILLOW:
            pil_img = Image.open(PNG_PATH)
            pil_img = pil_img.resize((120, 120), Image.Resampling.LANCZOS)
            pillow_img = self._keep_ref("resize_pillow", ImageTk.PhotoImage(pil_img))
            ttk.Label(right, image=pillow_img).pack()
        else:
            ttk.Label(right, text="Pillow がインストールされていません\npip install Pillow").pack()

        return frame

    def _tab_transparent(self):
        frame = ttk.Frame(self)

        desc = ttk.Label(
            frame,
            text="透過 PNG を様々な背景色の上に表示。透過部分は親ウィジェットの背景を透かして見えます。",
            wraplength=600,
        )
        desc.pack(pady=10)

        colors = ["white", "lightblue", "lightgreen", "salmon"]
        container = ttk.Frame(frame)
        container.pack(pady=10)

        for i, color in enumerate(colors):
            sub = tk.Frame(container, bg=color, width=160, height=160)
            sub.pack(side=tk.LEFT, padx=10)
            sub.pack_propagate(False)

            img = tk.PhotoImage(file=PNG_PATH)
            img = img.subsample(4, 4)
            self._keep_ref(f"trans_{color}", img)

            lbl = tk.Label(sub, image=img, bg=color)
            lbl.pack(expand=True)

        return frame

    def _tab_svg(self):
        frame = ttk.Frame(self)

        can_load_svg = supports_svg(self.patchlevel)
        desc_text = (
            "SVG 読み込み: Tk 9.0 以降で標準対応。\n"
            "この環境では SVG を直接読み込めます。"
            if can_load_svg
            else "SVG 読み込みには Tk 9.0 以降が必要です。\n"
                 "この環境では PNG 版を表示します。"
        )
        desc = ttk.Label(frame, text=desc_text, wraplength=600)
        desc.pack(pady=10)

        if can_load_svg:
            try:
                svg_img = tk.PhotoImage(file=SVG_PATH)
                svg_img = svg_img.subsample(2, 2)
                self._keep_ref("svg", svg_img)
                ttk.Label(frame, image=svg_img).pack(pady=20)
            except tk.TclError as e:
                ttk.Label(frame, text=f"SVG 読み込み失敗: {e}").pack(pady=20)
        else:
            img = self._keep_ref("svg_fallback", self._load_png(scale=4))
            ttk.Label(frame, image=img).pack(pady=20)

        return frame

    def _build_footer(self):
        footer = ttk.Frame(self, padding=10)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(
            footer,
            text="終了",
            command=self.destroy,
        ).pack(side=tk.RIGHT)


def main():
    print(f"Tk patchlevel: {get_patchlevel()}")
    print(f"Pillow available: {HAS_PILLOW}")
    print(f"PNG exists: {os.path.exists(PNG_PATH)}")
    print(f"SVG exists: {os.path.exists(SVG_PATH)}")

    if not os.path.exists(PNG_PATH):
        print(f"Error: {PNG_PATH} が見つかりません。", file=sys.stderr)
        sys.exit(1)

    app = ImagePlayground()
    app.mainloop()


if __name__ == "__main__":
    main()
