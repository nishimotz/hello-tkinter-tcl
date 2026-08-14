# Tkinter と Matplotlib 連携完全ガイド

## はじめに

Python でデスクトップ GUI アプリケーションを開発する際、GUI にグラフやデータ可視化機能を埋め込みたいケースは多々あります。

**`tkinter`（標準 GUI ツールキット）** と **`matplotlib`（標準的描画ライブラリ）** の組み合わせは、Python エコシステムにおいて最も安定しており、かつ追加の重いフレームワーク（PyQt など）を必要としない軽量でポピュラーな選択肢です。

> **インタラクティブデモ**: このリポジトリには、パラメータを動的に変更してグラフをリアルタイム更新するデモスクリプトが含まれています。
> - `matplotlib_tk_playground.py` — 波形・周波数・振幅・ノイズを GUI で操作できるプレイグラウンド
>
> 実行方法: `uv run --extra matplotlib -- python matplotlib_tk_playground.py`

---

## なぜ Matplotlib を Tkinter に埋め込むのか？

### 単体実行（`plt.show()`）と GUI 埋め込みの違

| 項目 | 単体実行 (`pyplot.show()`) | Tkinter GUI 埋め込み (`FigureCanvasTkAgg`) |
|---|---|---|
| **ウィンドウ制御** | Matplotlib が独自の独立ウィンドウを生成 | Tkinter ウィンドウの一部（Canvas ウィジェット）として統合 |
| **画面レイアウト** | グラフのみが表示される | ボタン、入力フォーム、テキスト等の自由なレイアウトが可能 |
| **イベント連携** | 限界がある | ボタン押下やスライダー操作と連動した即時再描画 |
| **アプリケーション化** | スクリプトの可視化用 | 製品レベルのデスクトップダッシュボード |

---

## 核心となる 2 つのバックエンドクラス

`matplotlib.backends.backend_tkagg` モジュールから提供される以下の 2 つのクラスが橋渡しをします：

1. **`FigureCanvasTkAgg(fig, master=parent)`**
   - Matplotlib の `Figure`（描画オブジェクト）を受け取り、`tkinter` の Canvas ウィジェットに変換します。
   - `.get_tk_widget()` メソッドで取得したウィジェットは、通常の `tk.Frame` や `tk.Label` と同じように `pack()` や `grid()` で配置できます。

2. **`NavigationToolbar2Tk(canvas, parent)`**
   - Matplotlib でおなじみの「拡大・縮小（ズーム）」「移動（パン）」「画像保存」ボタンが並んだツールバーを `tkinter` 上に生成します。

---

## 内部アーキテクチャ：ブリッジ（TkAgg）の仕組み

「描画は誰が行い、どのように Tkinter へ渡されているのか？」という低レイヤーの仕組みは以下の通りです。

### 1. `TkAgg` の正体
* **`Agg` (Anti-Grain Geometry)**: C++ で実装された高度な 2D ソフトウェア・ラスタライズ（ピクセル描画）エンジン。
* **`Tk`**: Tkinter / Tcl/Tk GUI ツールキット。

つまり `TkAgg` は **「Agg エンジンで描画したピクセルデータを、Tk の画像として表示する」** ブリッジです。

### 2. データフロー
```
[ Matplotlib (Python) ] ── (描画命令) ──> [ Agg エンジン (C++) ]
                                               │
                                  (RAM 上に RGBA バッファ生成)
                                               ▼
[ Tkinter (tk.Canvas) ] <── (C拡張 _tkagg) ── [ ピクセルバッファ転送 ]
```

1. **描画**: Matplotlib の C++ レンダラー（Agg）がメモリ上に RGBA ピクセル配列（ビットマップ）を描画します。
2. **転送**: C 拡張モジュール（`_tkagg`）がピクセルバッファを高速にメモリコピーします。
3. **表示**: `canvas.get_tk_widget()`（中身は通常の `tk.Canvas`）上に `PhotoImage` として一括貼り付けされます。

> 💡 **なぜ Tk のベクター描画（`create_line` 等）を使わないのか？**  
> Tkinter 標準の図形オブジェクトを個別作成するよりも、Agg で描画した 1 枚のビットマップ画像を転送する方がアンチエイリアス・数式描画・透過処理などの品質が高く、パフォーマンス面でも圧倒的に高速なためです。

---

## 基本的な実装ステップ

以下は最小限の構成で Tkinter に Matplotlib グラフを埋め込む手順です。

```python
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

# 1. Tkinter メインウィンドウの作成
root = tk.Tk()
root.title("Matplotlib in Tkinter")
root.geometry("600x450")

# 2. Matplotlib Figure & Subplot の作成 (plt は使わない)
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y, label="Sin Wave", color="blue")
ax.set_title("Embedded Plot")
ax.grid(True)

# 3. Canvas ウィジェットに変換して配置
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 4. ツールバーの追加 (オプション)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

root.mainloop()
```

---

## 実践テクニック

### 1. グラフのリアルタイム更新（再描画）

ユーザーがスライダーを動かした時やデータを取得した時にグラフを更新するには、以下の手順を踏みます：

1. 軸オブジェクトをクリア: `ax.clear()`
2. 新しいデータで再描画: `ax.plot(...)`
3. キャンバスの再描画命令: `canvas.draw_idle()`（※ `draw()` よりも非同期でUIの応答性を損なわないため推奨）

```python
def update_plot(freq_val):
    freq = float(freq_val)
    y = np.sin(freq * x)
    
    ax.clear()  # 以前のプロットを消去
    ax.plot(x, y, color="red")
    ax.grid(True)
    
    canvas.draw_idle()  # UIスレッドに負担をかけずに再描画
```

### 2. メインスレッド（`root.after`）による定期更新アニメーション

センサー値やシミュレーション結果を一定時間ごとに更新したい場合、Python の `threading` 直接操作ではなく Tkinter の `root.after()` を使うのが最も安全です。

```python
def animate():
    # データを更新
    global x_data, y_data
    x_data.append(x_data[-1] + 0.1)
    y_data.append(np.random.randn())
    
    # 描画更新
    ax.clear()
    ax.plot(x_data[-50:], y_data[-50:]) # 最新50件を表示
    canvas.draw_idle()
    
    # 100ms 後に再実行
    root.after(100, animate)

# アニメーション開始
root.after(100, animate)
```

---

## よくある落とし穴と回避策

### ❌ `import matplotlib.pyplot as plt` と `plt.show()` を使ってしまう
* **問題**: `plt.show()` を呼ぶと、Tkinter の `root.mainloop()` と衝突し、ウィンドウがフリーズしたり意図しない別ウィンドウが開いたりします。
* **解決策**: オブジェクト指向スタイル（`from matplotlib.figure import Figure`）を使用し、`plt` のグローバル状態管理に依存しないようにします。

### ❌ リサイズ時にグラフが小さく固まってしまう
* **問題**: `canvas_widget.pack()` の際に `fill=tk.BOTH, expand=True` を指定し忘れると、ウィンドウを広げてもグラフサイズが追従しません。
* **解決策**: 親コンテナと `canvas_widget` の両方に適切な伸縮設定（`expand=True` や `columnconfigure(..., weight=1)`）を適用してください。

---

## まとめ

Tkinter と Matplotlib の併用は、**`FigureCanvasTkAgg`** というブリッジクラスを使うことで驚くほどシンプルに実現できます。

* データ分析ツールの GUI 化
* リアルタイム波形モニター
* パラメータシミュレータ

といった高度なデスクトップアプリケーションを、外部の巨大なフレームワークなしに完全な Python 標準標準＋Matplotlib だけで構築することが可能です。ぜひ `matplotlib_tk_playground.py` を実行して挙動を試してみてください。
