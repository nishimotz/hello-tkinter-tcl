# Tcl/Tk テーマとスタイルガイド

## はじめに

Tcl/Tk（および Python の Tkinter）で GUI の**見た目**を制御するには、`tk` ウィジェットと `ttk` ウィジェットの違い、そして**テーマ**の仕組みを理解する必要があります。

この記事では、以下のトピックを扱います：

- `tk` と `ttk` の違い（色制御の基本）
- `ttk.Style().configure()`（静的色）と `style.map()`（状態別色）の使い分け
- プラットフォーム別のテーマと制約（macOS / Windows / Linux）
- テーマ切り替えの実装方法

> **インタラクティブデモ**: このリポジトリには、テーマとスタイルの挙動を
> 実際に触って確認できる `theme_playground.py` が含まれています。
> `uv run theme_playground.py` で起動し、テーマを切り替えながら
> tk.Button と ttk.Button の色の挙動を比較できます。

**想定読者**: Tkinter で GUI を作ったことがあるが、色や見た目が思うように
ならないと感じている方。

---

## 1. tk と ttk の違い

Tkinter には 2 種類のウィジェットセットがあります。

| 項目 | `tk` ウィジェット | `ttk` ウィジェット |
|------|------------------|--------------------|
| 例 | `tk.Button`, `tk.Label`, `tk.Frame` | `ttk.Button`, `ttk.Label`, `ttk.Frame` |
| 描画 | 各ウィジェットが独自に描画 | テーマ（スタイル）が描画 |
| 色の指定 | `bg` / `fg` を直接指定 | `style` 経由で指定 |
| 見た目 | プラットフォーム依存が強い | テーマで統一・変更可能 |
| モダンさ | 古い | 新しい（Tk 8.5+） |

### 色の指定方法の違い

**`tk` ウィジェット**は、コンストラクタや `config()` で直接色を指定します：

```python
import tkinter as tk

root = tk.Tk()
lbl = tk.Label(root, text="label", bg="#ffd54f", fg="black")
```

**`ttk` ウィジェット**は、`background` をコンストラクタ引数に**受け付けません**。
色を変えるには必ず `ttk.Style()` でスタイルを定義し、`style=` で適用します：

```python
from tkinter import ttk

style = ttk.Style()
style.configure("Amber.TButton", background="#ffd54f", foreground="black")

btn = ttk.Button(root, text="button", style="Amber.TButton")
```

> ⚠️ **注意**: `ttk.Button(root, background="red")` は
> `TclError: unknown option "-background"` になります。

---

## 2. テーマとは

**テーマ**は、`ttk` ウィジェットの見た目をまとめて定義したものです。
テーマを切り替えると、アプリ全体の `ttk` ウィジェットの見た目が一括で変わります。

### 利用可能なテーマを確認する

```python
from tkinter import ttk

style = ttk.Style()
print(style.theme_names())   # 利用可能なテーマ一覧
print(style.theme_use())     # 現在のテーマ
```

### プラットフォーム別のテーマ

| プラットフォーム | デフォルト | 利用可能なテーマの例 |
|------------------|-----------|----------------------|
| **macOS** | `aqua` | `aqua`, `clam`, `alt`, `default`, `classic` |
| **Windows** | `vista` | `vista`, `winnative`, `xpnative`, `clam`, `alt`, `default`, `classic` |
| **Linux** | 環境依存 | `clam`, `alt`, `default`, `classic` など |

### テーマを切り替える

```python
style.theme_use("clam")
```

> ⚠️ **注意**: テーマを切り替えると、それまで定義したカスタムスタイルが
> **リセット**されます。テーマ切り替え後はスタイルを再定義する必要があります。

### Tk 9.0 のテーマと SVG

Tk 9.0 では、テーマ/ウィジェットの外観をスケーラブルにするために **SVG を広く活用**しています（公式リリースノートより）。

- **正確な理解**: 「テーマがベクター描画になった」のではなく、**「SVG をテーマ/ウィジェットの外観に活用してスケーラブルにした」** が正確です。
- **画像**: `photo` 画像で SVG を**部分的にサポート**。
- **スケーリング**: 組み込みウィジェットとテーマは**スケーリング対応**（scaling-aware）。
- **注意**: `ttk` のテーマエンジン自体（`style configure` / `style map` / 要素）の基本構造は Tk 8.5 から変わっていません（TIP #48 ベース）。

---

## 3. プラットフォームごとの色の制約

**最も重要なポイント**: 一部のプラットフォームでは、`tk` や `ttk` の
ウィジェットが**ネイティブ描画**されるため、指定した色が**無視**されます。

### macOS（Aqua テーマ）

macOS の Tk は **Aqua テーマ**でウィジェットをネイティブ描画します。

| ウィジェット | `bg` / `background` の挙動 |
|--------------|---------------------------|
| `tk.Button` | ❌ **無視される**（常に macOS 標準のグレー） |
| `ttk.Button` | ❌ **無視される**（ネイティブ描画） |
| `tk.Label` | ✅ **尊重される**（色が表示される） |
| `tk.Frame` | ✅ **尊重される**（色が表示される） |

```python
import tkinter as tk

root = tk.Tk()

# ❌ macOS では常にネイティブのグレーで描画される
btn = tk.Button(root, text="button", bg="#ffd54f")

# ✅ 背景色が表示される
lbl = tk.Label(root, text="label", bg="#ffd54f", relief="solid", bd=1)
```

### Windows（vista テーマ）

Windows のデフォルト `vista` テーマもネイティブ描画のため、`ttk` の
`background` は無視されます。ただし `tk.Button` の `bg` は**表示されます**
（macOS と逆）。

| ウィジェット | vista（デフォルト） | clam / alt |
|--------------|--------------------|------------|
| `tk.Button` `bg` | ✅ 表示 | ✅ 表示 |
| `ttk.Button` `background` | ❌ 無視 | ✅ 表示 |

### Linux

Linux はネイティブテーマがなく、`clam` や `alt` などのテーマを使うため、
`ttk` の `background` が比較的素直に効きます。

### まとめ

| カラム | macOS (aqua) | Windows (vista) | Windows (clam/alt) |
|---|---|---|---|
| `tk.Button` `bg` | ❌ 無視 | ✅ 表示 | ✅ 表示 |
| `ttk.Button` `style.configure` | ❌ 無視 | ❌ 無視 | ✅ 表示 |
| `ttk.Button` `style.map` ホバー | ❌ 無視 | ❌ 無視 | ✅ 色変化 |

---

## 4. スタイルの定義方法

### `style.configure()`：静的色

ウィジェットの**通常状態**の色を定義します。

```python
style.configure("Red.TButton", background="red", foreground="white")
style.configure("Amber.TButton", background="#ffd54f", foreground="black")
```

### `style.map()`：状態別の色

ウィジェットの**状態**（ホバー、押下、無効など）に応じて色を変えます。

```python
style.configure("HoverRed.TButton", background="red", foreground="white")
style.map(
    "HoverRed.TButton",
    background=[
        ("pressed", "#8b0000"),   # 押下中: 濃い赤
        ("active", "#ff6666"),    # ホバー中: 明るい赤
        ("disabled", "#cccccc"),  # 無効: グレー
    ],
)
```

主な状態:

| 状態 | 意味 |
|------|------|
| `active` | マウスが乗っている（ホバー） |
| `pressed` | 押下中 |
| `disabled` | 無効 |
| `focus` | フォーカス中 |
| `readonly` | 読み取り専用 |

### スタイル名の命名規則

スタイル名は `ベース名.ウィジェットクラス` の形式が慣例です。

```python
style.configure("Red.TButton", ...)      # ttk.Button 用
style.configure("Custom.TLabel", ...)     # ttk.Label 用
style.configure("Custom.TEntry", ...)     # ttk.Entry 用
```

---

## 5. テーマ切り替えの実装例

テーマを動的に切り替えるデモの実装パターンです。

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

# カスタムスタイルを定義（テーマ切り替え時に再適用する）
def _configure_styles() -> None:
    style.configure("Red.TButton", background="red", foreground="white")
    style.configure("HoverRed.TButton", background="red", foreground="white")
    style.map(
        "HoverRed.TButton",
        background=[("pressed", "#8b0000"), ("active", "#ff6666")],
    )

_configure_styles()

# テーマ選択コンボボックス
theme_var = tk.StringVar(value=style.theme_use())
combo = ttk.Combobox(
    root,
    textvariable=theme_var,
    values=list(style.theme_names()),
    state="readonly",
)
combo.pack()

def _on_theme_change(*_args: object) -> None:
    style.theme_use(theme_var.get())
    _configure_styles()  # テーマ切り替えでリセットされるため再適用

theme_var.trace_add("write", _on_theme_change)

root.mainloop()
```

---

## 6. 実践的な指針

### 色付きウィジェットが必要な場合

- **表示専用**（内部パディングの可視化など）: `tk.Label` を使う（`bg` が尊重される）
- **クリック可能なボタン**: `tk.Button` は macOS で `bg` が効かないため、
  ネイティブな見た目を受け入れるか、`ttk` のスタイルで対応する

> ⚠️ **注意**: `tk.Label` は**ボタンの代用にはなりません**（クリック操作が
> できない）。「色付きのウィジェットで内部パディングを可視化する」といった
> **表示専用の用途**に限って `tk.Label` を使うのが適切です。

### クロスプラットフォームで色を確実に出すには

- `tk.Label` や `tk.Frame` など `bg` を尊重するウィジェットを選ぶ
- `ttk` を使う場合は `clam` / `alt` テーマを前提にする（ネイティブテーマでは色が無視される）

### ネイティブな見た目が目的なら

- `ttk` を使い、テーマのデフォルトの見た目を活かす
- 色の細かい制御は `ttk.Style()` 経由で行う

---

## 参考文献

- [Tcl/Tk 9.0 リリースノート](https://www.tcl-lang.org/software/tcltk/9.0.html) — Tk 9.0 の新機能（SVG 活用、スケーリング対応など）
- [ttk::intro（テーマエンジン入門）](https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_intro.html) — テーマ・要素・状態・スタイルの概念
- [ttk::style（スタイルデータベース）](https://www.tcl-lang.org/man/tcl9.0/TkCmd/ttk_style.html) — `style configure` / `style map` の公式リファレンス
- [Tkinter 8.5 reference (ttk)](https://tkdocs.com/tutorial/styles.html)
