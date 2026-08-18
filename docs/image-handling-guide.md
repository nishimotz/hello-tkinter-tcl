# Tcl/Tk における画像の使い方ガイド

## はじめに

Tcl/Tk（および Python の Tkinter）で GUI アプリケーションを開発する際、**画像を扱う**ことは必須になります。しかし、多くの開発者が以下の問題に直面します：

- 「なぜ画像が表示されないのか？」
- 「画像がガビガビになってしまう」
- 「透過 PNG を使いたい」
- 「アニメーション GIF を表示したい」
- 「画像のサイズを変更したい」

この記事では、Tcl/Tk での画像表示方法を基礎から応用まで整理し、実戦で使える知識を提供します。

> **想定読者**: Tcl/Tk または tkinter の基礎的な知識がある方（ウィジェットの作成や配置に慣れているレベル）

---

## Tcl/Tk の画像サポート概要

Tcl/Tk は標準で以下の画像形式を扱えます：

| 形式 | 読み込み | 透過 | 備考 |
|------|---------|------|------|
| **GIF** | ✅ | ✅ | アニメーション GIF 対応 |
| **PNG** | ✅ | ✅ | Tk 8.6 以降で標準対応 |
| **PGM/PPM** | ✅ | ❌ | 単純なフォーマット |
| **BMP** | ✅ | ❌ | 古い Windows 形式 |
| **JPEG** | 拡張が必要 | ❌ | `Img` 拡張が必要な場合あり |
| **SVG** | ✅ (読み込み) | ✅ | **Tk 9.0 以降で標準対応** |

> **重要**: 標準の Tcl/Tk では **JPEG は直接読み込めません**。`Img` 拡張をインストールするか、外部ライブラリで変換してください。SVG も Tk 9.0 から標準で読み込み可能になりました（完全な仕様ではありません）。

---

## 基本概念：photo image

Tcl/Tk で画像を扱う際、主に **`image`** コマンドを使います。特にビットマップ画像には **`photo`** タイプを使います。

```tcl
# 画像オブジェクトを作成
image create photo my_image -file "path/to/image.png"

# ラベルに画像を表示
label .lbl -image my_image
pack .lbl
```

Python (tkinter) では `PhotoImage` クラスを使います：

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# 画像を読み込む
img = tk.PhotoImage(file="path/to/image.png")

# ラベルに表示
label = ttk.Label(root, image=img)
label.pack()

root.mainloop()
```

> **注意**: `PhotoImage` オブジェクトは**参照を保持する必要があります**。ローカル変数に入れたまま関数を抜けると、ガベージコレクションで画像が消えて表示されなくなることがあります。

---

## 画像の作成と読み込み

### ファイルから読み込む

**Tcl (wish)**:
```tcl
image create photo logo -file "images/logo.png"
label .logo_label -image logo
pack .logo_label
```

**Python (Tkinter)**:
```python
from tkinter import PhotoImage

logo = PhotoImage(file="images/logo.png")
label = tk.Label(root, image=logo)
label.pack()

# 参照を保持（重要）
label.image = logo
```

### 埋め込み（Base64）データから読み込む

画像をスクリプト内に埋め込みたい場合、Base64 エンコードしたデータを使えます。

**Tcl (wish)**:
```tcl
set image_data "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
image create photo embedded -data $image_data
label .lbl -image embedded
pack .lbl
```

**Python (Tkinter)**:
```python
import base64

# 画像ファイルを Base64 エンコード
with open("images/logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("ascii")

img = PhotoImage(data=encoded)
label = tk.Label(root, image=img)
label.pack()
```

### 実行中に動的に生成する

Tcl/Tk の `photo` はピクセル単位で操作できます。

```tcl
image create photo generated -width 100 -height 100
generated put red -to 0 0 50 50
generated put blue -to 50 50 100 100

label .lbl -image generated
pack .lbl
```

Python では `PhotoImage` の `put` メソッドを使います：

```python
img = PhotoImage(width=100, height=100)
img.put("red", to=(0, 0, 50, 50))
img.put("blue", to=(50, 50, 100, 100))

label = tk.Label(root, image=img)
label.pack()
```

---

## 画像の表示先

画像は主に以下のウィジェットに表示できます：

| ウィジェット | 用途 | 例 |
|-------------|------|-----|
| `label` | 静的な画像表示 | アイコン、ロゴ |
| `button` | 画像付きボタン | ツールバーボタン |
| `canvas` | 自由な位置・重ね合わせ | ゲーム、図形、カスタム描画 |

### Label で表示

```tcl
label .icon -image my_image
pack .icon
```

### Button で表示

```tcl
button .btn -image my_image -command {puts "clicked"}
pack .btn
```

### Canvas で表示

```tcl
canvas .c -width 400 -height 300
pack .c

.c create image 200 150 -image my_image -tag bg
```

---

## 画像のリサイズ

Tcl/Tk の標準 `photo` にはリサイズ機能がありません。以下の方法を使います。

### 方法 1: ` subsample` で縮小

`subsample` は画像を縮小表示するための機能です。整数倍のみ対応です。

```tcl
image create photo original -file "image.png"
image create photo small
small copy original -subsample 2 2

label .lbl -image small
pack .lbl
```

Python:
```python
original = PhotoImage(file="image.png")
small = original.subsample(2, 2)  # 1/2 サイズ
label = tk.Label(root, image=small)
label.pack()
```

### 方法 2: PIL/Pillow を使う（Python）

Python では `Pillow`（PIL）を使って柔軟にリサイズできます。

```python
from PIL import Image, ImageTk

# Pillow で開いてリサイズ
pil_img = Image.open("image.png")
pil_img = pil_img.resize((100, 100), Image.Resampling.LANCZOS)

# Tkinter 用に変換
tk_img = ImageTk.PhotoImage(pil_img)

label = tk.Label(root, image=tk_img)
label.pack()
label.image = tk_img  # 参照保持
```

### 方法 3: Tcl の Img 拡張を使う

Tcl では `Img` パッケージを使うと高品質なリサイズが可能です。

```tcl
package require Img
image create photo resized
resized copy original -shrink -zoom 50 50
```

---

## 透過画像（PNG/GIF）

透過 GIF や PNG は、`photo` 画像で自然に扱えます。

```tcl
image create photo transparent -file "icon.png"
label .lbl -image transparent -bg "SystemTransparent"
pack .lbl
```

Python:
```python
img = PhotoImage(file="icon.png")
label = tk.Label(root, image=img, bg="SystemTransparent")
label.pack()
label.image = img
```

> **注意**: 透過部分が正しく表示されない場合は、親ウィジェットやウィンドウの背景色を確認してください。

---

## アニメーション GIF

Tcl/Tk 8.6 以降では `PhotoImage` でアニメーション GIF を扱えます。

### Tcl (wish)

```tcl
image create photo anim -file "animation.gif"
label .lbl -image anim
pack .lbl

proc update_animation {} {
    global anim
    anim configure -format "gif -index 0"
    # アニメーションを次のフレームへ進めるロジックが必要
    after 100 update_animation
}
```

### Python (Tkinter)

```python
import tkinter as tk

root = tk.Tk()

# アニメーション GIF を読み込む
anim = tk.PhotoImage(file="animation.gif")

label = tk.Label(root, image=anim)
label.pack()

frame_index = 0

def update_frame():
    global frame_index, anim
    try:
        anim.configure(format=f"gif -index {frame_index}")
        frame_index += 1
    except tk.TclError:
        frame_index = 0  # ループ再生

    root.after(100, update_frame)

root.after(100, update_frame)
root.mainloop()
```

> **注意**: 上記は単純な例です。実際のフレーム数や遅延時間は GIF ファイルによって異なります。`Image.open().n_frames` などで取得できます。

---

## 画像の参照保持（最重要）

Tkinter では `PhotoImage` オブジェクトがガベージコレクトされると、画像が表示されなくなります。**必ず参照を保持してください**。

```python
def load_image(path):
    img = PhotoImage(file=path)
    label = tk.Label(root, image=img)
    label.pack()
    # これだけでは画像が表示されないことがある
    return img

# グローバル変数やウィジェットに保持
root.my_image = load_image("logo.png")
```

安全なパターン：

```python
img = PhotoImage(file="logo.png")
label = tk.Label(root, image=img)
label.pack()
label.image = img  # ウィジェットに参照を保存
```

---

## よくあるトラブルシューティング

### 画像が表示されない

- `PhotoImage` オブジェクトへの参照を保持しているか確認
- ファイルパスが正しいか確認
- 対応している画像形式か確認（JPEG は標準非対応）
- ウィジェットが配置されているか確認

### ガビガビになった

- 縮小には `subsample` または Pillow を使う
- 拡大は品質が落ちるため、元画像を大きくしておく

### 透過部分が黒くなる

- 親ウィジェットの背景色を確認
- `-bg "SystemTransparent"` を指定する

### アニメーション GIF が動かない

- 手動でフレームを切り替える実装が必要
- `after` メソッドを使って定期更新

---

## まとめ

| 用途 | 推奨方法 |
|------|---------|
| 静的画像表示 | `label` + `photo` |
| ボタンアイコン | `button` + `photo` |
| 自由な描画・重ね合わせ | `canvas` + `photo` |
| 画像リサイズ | Pillow（Python）または Img 拡張（Tcl） |
| 透過画像 | PNG/GIF を `photo` で読み込む |
| アニメーション GIF | フレームを手動で切り替える |

---

## Tk 8 と Tk 9 の画像処理の違い

Tcl/Tk 9.0 では画像処理が大幅に強化されています。主な差分は以下のとおりです。

### 1. SVG 読み込み対応

**Tk 9.0** からは、標準で SVG を `photo` 画像として読み込めるようになりました。ただし、**読み込み専用**で、仕様の一部のみサポートしています。

```tcl
# Tk 9.0 以降
image create photo svg_icon -file "icon.svg"
label .lbl -image svg_icon
pack .lbl
```

読み込み時に解像度やサイズを指定できます：

```tcl
image create photo svg_icon -file "icon.svg" \
    -format "svg -scale 2.0"
```

### 2. フルアルファチャンネル（半透明）

**Tk 8** では透過は「透明/不透明」の2値が中心で、`transparency get/set x y` は boolean を返します。

```tcl
# Tk 8.x
$img transparency get x y   ;# 0 または 1
$img transparency set x y 1 ;# 完全透明にする
```

**Tk 9.0** では 0〜255 の完全なアルファチャンネルを扱えます。

```tcl
# Tk 9.0
$img transparency get x y -alpha   ;# 0 から 255 の値
$img transparency set x y 128 -alpha ;# 半透明に設定

$img get x y -withalpha ;# {r g b alpha} の4要素リストを返す
```

Python tkinter でも同じように利用できます。ただし、tkinter の機能は Tcl/Tk のバージョンに依存するため、実行時の Tk バージョンを確認してください。

```python
import tkinter as tk

print(tk.Tcl().eval("info patchlevel"))  # 例: 9.0.x
```

### 3. メタデータ辞書

**Tk 9.0** では、画像にメタデータ辞書を持たせることができます。これにより、ファイルから読み込んだ付加情報や、書き出す画像のプロパティを扱えます。

```tcl
# 読み込み時にメタデータを取得
image create photo img -file "photo.png" -metadata {} -format png
set meta [img cget -metadata]
# meta は dict 形式。DPI、aspect、comment などを含む可能性がある
```

代表的なメタデータキー：

| キー | 内容 | 対応形式 |
|------|------|---------|
| `DPI` | 水平方向の解像度 | PNG |
| `aspect` | アスペクト比（横/縦） | GIF、PNG |
| `comment` | 画像コメント | GIF、PNG |

アニメーション GIF の場合、フレームごとに以下のようなメタデータが取得できます：

- `delay time time` — 次フレームまでの遅延（10ms単位）
- `disposal method method` — 前フレームの処理方法
- `update region X0, Y0, width, height` — 更新領域

### 4. Python tkinter での注意

Python tkinter は Tcl/Tk ライブラリのラッパーです。そのため、画像機能の多くは **インストールされている Tcl/Tk のバージョン** に依存します。

```python
import tkinter as tk

patch = tk.Tcl().eval("info patchlevel")
print(patch)  # 8.6.x なら Tk 8, 9.0.x なら Tk 9
```

- Pillow を併用すれば、PNG/GIF/SVG/JPEG などほとんどの形式を扱えます。
- ただし、Tk 9 からネイティブで SVG やフルアルファが使えるため、外部ライブラリへの依存が減ります。

---

## まとめ

| 用途 | 推奨方法 |
|------|---------|
| 静的画像表示 | `label` + `photo` |
| ボタンアイコン | `button` + `photo` |
| 自由な描画・重ね合わせ | `canvas` + `photo` |
| 画像リサイズ | Pillow（Python）または Img 拡張（Tcl） |
| 透過画像 | PNG/GIF を `photo` で読み込む |
| アニメーション GIF | フレームを手動で切り替える |
| SVG 読み込み | **Tk 9.0 以降なら標準対応** |
| フルアルファ・メタデータ | **Tk 9.0 以降で利用可能** |

Tcl/Tk の画像機能はシンプルですが、組み合わせることで多くの用途をカバーできます。特に **参照保持** と **同一親でのマネージャー混在禁止**（[geometry-managers.md](geometry-managers.md) 参照）を意識すれば、画像関連の問題はほとんど解決します。
