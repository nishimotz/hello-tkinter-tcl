# Tkinter と Python 定番ライブラリの連携ガイド

## はじめに

Python 標準の GUI ツールキットである `tkinter` は、データ分析・画像処理・マルチメディア・3D描画など、Python の様々な定番ライブラリと組み合わせて高度なデスクトップアプリケーションを構築できます。

この記事では、代表的な定番ライブラリと Tkinter の連携パターンとサンプルコードをまとめて紹介します。

---

## 1. Matplotlib（グラフ描画・データ可視化）

Matplotlib の `FigureCanvasTkAgg` ブリッジを使用することで、GUI 内にインタラクティブなグラフを埋め込むことができます。

* 📄 **詳細ガイド**: [Tkinter と Matplotlib 連携完全ガイド](matplotlib-integration-guide.md)
* 💻 **デモスクリプト**: `matplotlib_tk_playground.py`
* **実行方法**:
  ```bash
  uv run --extra matplotlib -- python matplotlib_tk_playground.py
  ```

---

## 2. Pillow / PIL（高度な画像処理）

Pillow の `PIL.ImageTk.PhotoImage` モジュールを使うことで、PNG, JPEG, WEBP などの画像を Tkinter ウィジェットにシームレスに表示・加工できます。

* 📄 **詳細ガイド**: [Tcl/Tk における画像の使い方完全ガイド](image-handling-guide.md)
* 💻 **デモスクリプト**: `image_playground.py`
* **実行方法**:
  ```bash
  uv run --extra pillow -- python image_playground.py
  ```

---

## 3. pandastable（Pandas データフレームの表表示）

Python のデータ分析定番である `pandas` の `DataFrame` を、Excel スプレッドシートのように Tkinter 上で対話的に表示・編集・ソート・検索できる専用パッケージです。

* 💻 **デモスクリプト**: `pandastable_playground.py`
* **実行方法**:
  ```bash
  uv run --extra pandastable -- python pandastable_playground.py
  ```

### コード例

```python
import tkinter as tk
import pandas as pd
from pandastable import Table

root = tk.Tk()
root.title("pandastable Simple Demo")
root.geometry("650x400")

# メインフレーム
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# サンプルデータフレーム作成
df = pd.DataFrame(
    {
        "Product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"],
        "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Audio"],
        "Price ($)": [1200.0, 25.5, 75.0, 300.0, 150.0],
        "Stock": [15, 120, 45, 8, 30],
    }
)

# Table ウィジェットを作成して表示
table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
table.show()

root.mainloop()
```

---

## 4. OpenCV（Webカメラ映像・画像認識）

OpenCV (`cv2`) のカメラ画像（NumPy 配列 / BGR 形式）は、`Pillow` を仲介して RGB 変換後 `ImageTk.PhotoImage` にすることで、`tk.Label` や `tk.Canvas` にリアルタイム描画（リアルタイム動画表示）が可能です。

### データ変換パイプライン

```
[ OpenCV (BGR NumPy 配列) ]
        │
        ▼ cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
[ RGB NumPy 配列 ]
        │
        ▼ PIL.Image.fromarray()
[ PIL Image オブジェクト ]
        │
        ▼ PIL.ImageTk.PhotoImage()
[ Tkinter 用 Image オブジェクト ] ──> Label.configure(image=...)
```

### コード例（Webカメラリアルタイム表示）

```python
import tkinter as tk
import cv2
from PIL import Image, ImageTk

root = tk.Tk()
root.title("OpenCV + Tkinter Camera Viewer")

label = tk.Label(root)
label.pack(fill=tk.BOTH, expand=True)

cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        # 1. BGR -> RGB 変換
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 2. PIL Image -> ImageTk に変換
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # 3. Label の画像を更新（ガベージコレクション対策で参照保持）
        label.imgtk = imgtk
        label.configure(image=imgtk)
    
    # 15ms 後に次のフレームを取得 (約 60 fps)
    root.after(15, update_frame)

update_frame()
root.mainloop()
cap.release()
```

---

## 5. python-vlc（動画再生）

`python-vlc` ライブラリを使用すると、Tkinter ウィジェットの「ウィンドウハンドル（`winfo_id()`）」を VLC プレイヤーに渡すことで、動画ファイルを Tkinter ウィジェット内部でスムーズに再生できます。

### コード例

```python
import tkinter as tk
import vlc

root = tk.Tk()
root.title("VLC Player in Tkinter")

# 動画表示用のパネルウィジェット
video_panel = tk.Frame(root, width=640, height=360, bg="black")
video_panel.pack(fill=tk.BOTH, expand=True)

# VLC インスタンスとプレイヤー作成
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new("sample.mp4") # 動画ファイルパス
player.set_media(media)

# Tkinter ウィジェットのウィンドウ ID を渡す
# (OS に応じて関数を使い分け)
# Windows: player.set_hwnd(video_panel.winfo_id())
# macOS:   player.set_nsobject(video_panel.winfo_id())
# Linux:   player.set_xwindow(video_panel.winfo_id())

player.play()
root.mainloop()
```

---

## 6. PyOpenGL / Pygame（3D・ゲームエンジン埋め込み）

### PyOpenGL (`pyopengltk`)
`pyopengltk` パッケージを使用すると、`pyopengltk.OpenGLFrame` を継承したウィジェット内で 3D OpenGL レンダリングを行えます。

### Pygame (SDL)
環境変数 `os.environ['SDL_WINDOWID'] = str(frame.winfo_id())` を設定してから `pygame.init()` を呼び出すことで、Pygame の描画画面を Tkinter の `Frame` 内に埋め込むことができます。

---

## まとめ

Tkinter は軽量かつ Python 標準添付の GUI でありながら、外部ライブラリとのブリッジ機能が豊富に揃っています。

* データの表表示 ➔ **`pandastable`** (`pandastable_playground.py`)
* グラフ可視化 ➔ **`matplotlib`** (`matplotlib_tk_playground.py`)
* 高度な画像処理 ➔ **`Pillow`** (`image_playground.py`)
* カメラ映像/画像認識 ➔ **`OpenCV` + `Pillow`**
* 動画再生 ➔ **`python-vlc`** (`winfo_id()`)

用途に応じて最適な定番ライブラリを組み合わせてデスクトップアプリケーションを開発してみてください。
