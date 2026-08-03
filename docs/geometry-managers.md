# Tcl/Tk ジオメトリマネージャー完全ガイド

## はじめに

Tcl/Tk（および Python の Tkinter）で GUI アプリケーションを開発する際、**ジオメトリマネージャー**の理解は避けて通れません。しかし、多くの開発者が以下の問題に直面します：

- 「なぜウィジェットが配置されないのか？」
- 「pack と grid を一緒に使ったらエラーが出た」
- 「リサイズするとレイアウトが崩れる」

この記事では、3 つのジオメトリマネージャー（pack, grid, place）の特性を整理し、実戦で使える知識を提供します。

**想定読者**: HTML/CSS の基礎知識がある方（`div`, `flexbox`, `grid` といった用語を知っているレベル）

---

## HTML/CSS 開発者への早見表

Tcl/Tk を初めて触る HTML/CSS 開発者のために、概念の対応関係を示します：

| Tcl/Tk | HTML/CSS | 類似点 | 相違点 |
|--------|----------|--------|--------|
| **ウィジェット** | HTML 要素 | UI の構成要素 | Tcl/Tk はツリー構造 |
| **pack** | `flexbox` | 縦/横の並び制御 | flexbox より機能が少ない |
| **grid** | `display: grid` | 行列表レイアウト | CSS Grid より単純 |
| **place** | `position: absolute` | 絶対座標配置 | ほぼ同じ |
| **sticky** | `justify-self`, `align-self` | セル内配置 | 方位で指定（n,s,e,w） |
| **fill** | `width: 100%` | 余白を埋める | 方向指定可能（x, y, both） |
| **expand** | `flex-grow: 1` | 余剰領域の分配 | 真偽値のみ |
| **columnconfigure** | `grid-template-columns` | 列の挙動定義 | 後から設定 |

### 重要な違い

**HTML/CSS**:
```css
.container {
  display: flex;  /* または grid */
  flex-direction: column;
}
```

**Tcl/Tk**:
```tcl
pack .widget -side top  ;# または grid
```

HTML/CSS では**親コンテナに `display` プロパティを設定**しますが、Tcl/Tk では**子ウィジェットごとにマネージャーを呼び出す**という違いがあります。

---

## そもそも「ジオメトリマネージャー」とは？

**ジオメトリマネージャー**は、GUI ウィジェットの**配置とサイズを自動的に計算する仕組み**です。

### なぜ「マネージャー」が必要か？

GUI ウィンドウでは、以下のような計算が必要です：

1. 各ウィジェットの位置（x, y 座標）
2. 各ウィジェットのサイズ（幅、高さ）
3. 親ウィジェットのリサイズ時の挙動
4. ウィジェット同士の重なり制御

これらを**手動で計算するのは大変**です。ウィンドウがリサイズされるたびに、全ての座標を再計算する必要があります。

### マネージャーの役割

ジオメトリマネージャーは、**宣言的な指定**から自動的にレイアウトを計算します：

```tcl
# 「上側に配置、横いっぱいに拡張」と宣言するだけ
pack .button -side top -fill x -expand true

# ウィンドウリサイズ時はマネージャーが自動で再計算
```

これは HTML/CSS の以下に相当します：

```css
.button {
  width: 100%;
  flex-shrink: 0;
}
```

---

## 3 つのジオメトリマネージャー

Tcl/Tk には 3 つのジオメトリマネージャーが存在します：

| マネージャー | 配置基準 | 主な用途 | 学習曲線 |
|-------------|---------|---------|---------|
| **pack** | 親コンテナ内の相対位置 | シンプルな縦/横並び | 易 |
| **grid** | 行列表（グリッド） | フォーム、表形式レイアウト | 中 |
| **place** | 絶対座標（ピクセル） | 固定配置、カスタムレイアウト | 難 |

---

## 基本概念：ウィジェットとコンテナ

Tcl/Tk の GUI は**ウィジェット**（部品）と**コンテナ**（入れ物）で構成されます。

### ウィジェットの種類

- **基本ウィジェット**: ボタン、ラベル、エントリー（入力フィールド）
- **コンテナウィジェット**: フレーム（他のウィジェットを格納できる）
- **複合ウィジェット**: ツリービュー、テキストエリア、キャンバス

### ツリー構造

GUI ウィンドウは**ツリー構造**で管理されます：

```
root（メインウィンドウ）
├── toolbar（フレーム）
│   ├── button1
│   ├── button2
│   └── button3
├── main_area（フレーム）
│   ├── label
│   └── entry
└── status_bar（ラベル）
```

**重要なポイント**:
- 各ウィジェットは**1 つの親**を持つ
- コンテナウィジェットは**子ウィジェット**を持てる
- ジオメトリマネージャーは**親→子**の関係を基準に配置を計算する

### HTML との比較

```html
<!-- HTML: 入れ子構造 -->
<div class="toolbar">
  <button>Button 1</button>
  <button>Button 2</button>
</div>
```

```tcl
; Tcl/Tk: 同様の入れ子構造
frame .toolbar
button .toolbar.button1 -text "Button 1"
button .toolbar.button2 -text "Button 2"
```

命名規則に注目してください：
- HTML: クラス名でグループ化
- Tcl/Tk: **ドット区切りの名前**で親子関係を表す（`.toolbar.button1` は `.toolbar` の子）

---

## pack：最もシンプルなマネージャー

### 基本構文

**Tcl (wish)**:
```tcl
# ウィジェット作成と配置を別々に行う場合
button .button -text "Click Me"
pack .button -side top -fill x -expand true

# 一行で記述する場合
pack [button .button -text "Click Me"] -side top -fill x -expand true
```

**Python (Tkinter)**:
```python
# ウィジェット作成と配置を別々に行う場合
button = ttk.Button(root, text="Click Me")
button.pack(side=tk.TOP, fill=tk.X, expand=True)

# 一行で記述する場合
ttk.Button(root, text="Click Me").pack(side=tk.TOP, fill=tk.X, expand=True)
```

### Tcl/Tk と Python の構文比較

| 項目 | Tcl (wish) | Python (Tkinter) |
|------|-----------|------------------|
| **ウィジェット作成** | `button .name -text "..."` | `ttk.Button(root, text="...")` |
| **配置メソッド** | `pack .name -option value` | `name.pack(option=value)` |
| **オプション接頭辞** | `-`（ハイフン） | なし（キーワード引数） |
| **真偽値** | `true`/`false` | `True`/`False` |
| **定数** | `top`, `x` など（文字列） | `tk.TOP`, `tk.X` など |

### 完全なコード例：Tcl (wish)

**例 1: 単純なボタン配置**

```tcl
#!/usr/bin/wish
# 基本的なボタン配置

# ウィンドウタイトルを設定
wm title . "My Application"

# ボタンを作成して配置
button .btn1 -text "Button 1" -command {puts "Clicked!"}
pack .btn1 -side top -padx 10 -pady 5

button .btn2 -text "Button 2"
pack .btn2 -side top -padx 10 -pady 5

# メインループ開始（wish では自動）
```

実行方法：
```bash
chmod +x script.tcl
./script.tcl
# または
wish script.tcl
```

**例 2: ツールバーレイアウト**

```tcl
#!/usr/bin/wish
# ツールバーのような横並びレイアウト

# フレームを作成（コンテナ）
frame .toolbar
pack .toolbar -side top -fill x -pady 2

# ボタンを横並びに配置
button .toolbar.new -text "New" -command {puts "New"}
button .toolbar.open -text "Open" -command {puts "Open"}
button .toolbar.save -text "Save" -command {puts "Save"}

# それぞれのボタンを左から配置
pack .toolbar.new .toolbar.open .toolbar.save -side left -padx 2

# ウィンドウサイズを設定
wm geometry . 400x300
```

**例 3: フォームレイアウト（pack のみ）**

```tcl
#!/usr/bin/wish
# pack を使ったフォームレイアウト

# ラベルとエントリーのペアを縦に配置
frame .form
pack .form -side top -fill x -padx 10 -pady 10

# 名前入力
frame .form.name_row
pack .form.name_row -side top -fill x -pady 2

label .form.name_row.label -text "Name:" -width 10 -anchor e
entry .form.name_row.entry
pack .form.name_row.label -side left
pack .form.name_row.entry -side left -fill x -expand true

# 年齢入力
frame .form.age_row
pack .form.age_row -side top -fill x -pady 2

label .form.age_row.label -text "Age:" -width 10 -anchor e
entry .form.age_row.entry
pack .form.age_row.label -side left
pack .form.age_row.entry -side left -fill x -expand true

# ボタン
button .form.submit -text "Submit" -command {puts "Submitted!"}
pack .form.submit -side top -pady 10
```

### 完全なコード例：Python (Tkinter)

**例 1: 単純なボタン配置**

```python
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("My Application")

# ボタンを作成して配置
btn1 = ttk.Button(root, text="Button 1", command=lambda: print("Clicked!"))
btn1.pack(side=tk.TOP, padx=10, pady=5)

btn2 = ttk.Button(root, text="Button 2")
btn2.pack(side=tk.TOP, padx=10, pady=5)

root.mainloop()
```

**例 2: ツールバーレイアウト**

```python
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Toolbar Demo")

# フレームを作成（コンテナ）
toolbar = ttk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X, pady=2)

# ボタンを横並びに配置
btn_new = ttk.Button(toolbar, text="New", command=lambda: print("New"))
btn_open = ttk.Button(toolbar, text="Open", command=lambda: print("Open"))
btn_save = ttk.Button(toolbar, text="Save", command=lambda: print("Save"))

btn_new.pack(side=tk.LEFT, padx=2)
btn_open.pack(side=tk.LEFT, padx=2)
btn_save.pack(side=tk.LEFT, padx=2)

root.geometry("400x300")
root.mainloop()
```

### オプション解説

| オプション | 値 | 説明 | HTML/CSS での対応 |
|-----------|-----|------|------------------|
| `-side` | `top`, `bottom`, `left`, `right` | 配置方向（デフォルト：`top`） | `flex-direction` + `order` |
| `-fill` | `none`, `x`, `y`, `both` | 余白の埋め方 | `width`, `height` |
| `-expand` | `true`/`false` | 親ウィジェットのリサイズに追随 | `flex-grow: 1` |
| `-padx`, `-pady` | 数値 | 外側の余白（external padding） | `margin` |
| `-ipadx`, `-ipady` | 数値 | 内側の余白（internal padding） | `padding` |

### マージンとパディングの違い

Tcl/Tk では、**padx/pady**（外側）と **ipadx/ipady**（内側）の 2 種類の余白を制御できます。

これは HTML/CSS の **margin** と **padding** に相当します。

- **padx/pady**: **external padding** - ウィジェットの外側に追加する余白
- **ipadx/ipady**: **internal padding** - ウィジェットの内側に追加する余白

```
ウィジェットの内容と余白の関係

┌─────────────────────────────┐
│  ← padx（外側の余白）→      │
│  ┌───────────────────────┐  │
│  │ ←ipadx│             │←│  │
│  │(内側) │  内容エリア  │  │  │
│  │ ←ipadx│             │←│  │
│  └───────────────────────┘  │
│  ← padx（外側の余白）→      │
└─────────────────────────────┘
       親コンテナの境界
```

**視覚的な例**:

```
ケース 1: padx=10（外側 10px）
┌─────────────────┐
│                 │  ← 10px の隙間
│  ┌───────────┐  │
│  │ widget    │  │  ← ウィジェット自体のサイズは変わらない
│  └───────────┘  │
│                 │
└─────────────────┘

ケース 2: ipadx=10（内側 10px）
┌─────────────────┐
│ ┌─────────────┐ │
│ │            │ │
│ │  widget    │ │  ← 内容の左右に 10px ずつ追加
│ │            │ │
│ └─────────────┘ │
└─────────────────┘
   ウィジェット全体が大きくなる
```

**HTML/CSS との比較**:

```css
/* padx=10 に相当 */
.widget {
  margin: 10px;
}

/* ipadx=10 に相当 */
.widget {
  padding: 10px;
}
```

### 方向別の指定

padx/pady は X 方向（水平）と Y 方向（垂直）を別々に指定できます：

| オプション | 方向 | HTML/CSS |
|-----------|------|----------|
| `padx` | 水平（左右） | `margin-left` + `margin-right` |
| `pady` | 垂直（上下） | `margin-top` + `margin-bottom` |
| `ipadx` | 水平（左右） | `padding-left` + `padding-right` |
| `ipady` | 垂直（上下） | `padding-top` + `padding-bottom` |

**タプルでの指定**:

```python
# 左 5px, 右 10px
widget.pack(padx=(5, 10))

# 上 5px, 下 10px
widget.pack(pady=(5, 10))
```

```css
/* CSS での同等の表現 */
.widget {
  margin-left: 5px;
  margin-right: 10px;
  margin-top: 5px;
  margin-bottom: 10px;
}
```

### 使用例：フォームの余白制御

```python
# ラベルとエントリーの間に余白を設ける
ttk.Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(frame).grid(row=0, column=1, padx=5, pady=5)

# エントリー内部にも余白を設ける（文字が端に寄らない）
ttk.Entry(frame).grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
```

視覚的なレイアウト：

```
pady=5（行間の余白）
┌──────────────────────┐
│ [Name:] [Entry]      │  ← 行 0
│   ↑ 5px ↑            │
│ [Age:]  [Entry]      │  ← 行 1
└──────────────────────┘

ipadx=5, ipady=5（エントリー内部の余白）
┌──────────────────────┐
│ [Name:] ┌──────────┐ │
│         │  内容    │ │  ← 左右上下に 5px の余白
│         └──────────┘ │
└──────────────────────┘
```

### side の仕組み

**side** は、ウィジェットを親コンテナのどの辺に配置するかを指定します。

```
side=top（デフォルト）
┌─────────────────┐
│ [widget1]       │  ← 上から順に配置
│ [widget2]       │
│ [widget3]       │
└─────────────────┘

side=left
┌─────────────────┐
│ [w1][w2][w3]    │  ← 左から順に配置
└─────────────────┘
```

**HTML/CSS との比較**:

```css
/* side=top に相当 */
.container {
  display: flex;
  flex-direction: column;
}

/* side=left に相当 */
.container {
  display: flex;
  flex-direction: row;
}
```

### fill と expand の関係

**fill** と **expand** は一緒に使用されることが多いですが、役割が異なります：

- **fill**: 割り当てられたセル内での拡張
- **expand**: 親コンテナの余剰領域の分配

視覚的な例：

```
親コンテナ（400x300）に 2 つのウィジェットを配置

ケース 1: fill=x, expand=false
┌─────────────────┐
│ [────widget1────] │  ← 横いっぱい（固定高）
│ [────widget2────] │
│                 │  ← 余白
└─────────────────┘

ケース 2: fill=both, expand=true
┌─────────────────┐
│ [────widget1────] │  ← 余剰領域を均等に分配
│ [──────────────] │
│ [────widget2────] │
│ [──────────────] │
└─────────────────┘
```

**HTML/CSS との比較**:

```css
/* fill=x, expand=false */
.widget {
  width: 100%;
  flex-grow: 0;
}

/* fill=both, expand=true */
.widget {
  width: 100%;
  height: 100%;
  flex-grow: 1;
}
```

### 使用例：ツールバー

**Tcl (wish)**:
```tcl
#!/usr/bin/wish
# ツールバーレイアウト

# フレーム（コンテナ）を作成
frame .toolbar
pack .toolbar -side top -fill x

# ボタンを横並びに配置
# 複数ウィジェットを一度に pack 可能
pack [button .toolbar.new -text "New"] \
     [button .toolbar.open -text "Open"] \
     [button .toolbar.save -text "Save"] \
     -side left -padx 2

# または個別に pack することも可能
# pack .toolbar.new -side left -padx 2
# pack .toolbar.open -side left -padx 2
# pack .toolbar.save -side left -padx 2
```

**Python (Tkinter)**:
```python
toolbar = ttk.Frame(root)
toolbar.pack(side=tk.TOP, fill=tk.X)

btn_new = ttk.Button(toolbar, text="New")
btn_open = ttk.Button(toolbar, text="Open")
btn_save = ttk.Button(toolbar, text="Save")

btn_new.pack(side=tk.LEFT, padx=2)
btn_open.pack(side=tk.LEFT, padx=2)
btn_save.pack(side=tk.LEFT, padx=2)
```

### pack のメリット

- ✅ 直感的：上から順に配置していくだけ
- ✅ コード量少ない
- ✅ シンプルなレイアウトに最適

### pack のデメリット

- ❌ 複雑な表形式レイアウトには不向き
- ❌ 後から特定の位置に挿入するのが困難
- ❌ 行またぎの配置ができない

---

## grid：表形式レイアウトの決定版

**HTML/CSS での対応**: `display: grid`

### 基本概念

grid マネージャーは、ウィジェットを**行（row）と列（column）のグリッド**に配置します。

```
行 0  ┌──────────┬──────────────┐
      │ Label    │ Entry        │
行 1  ├──────────┼──────────────┤
      │ Label    │ Entry        │
行 2  └──────────┴──────────────┘
         列 0        列 1
```

### 基本構文

**Tcl (wish)**:
```tcl
# ウィジェット作成
label .lbl -text "Username:"
entry .ent

# grid で配置
grid .lbl -row 0 -column 0 -sticky w
grid .ent -row 0 -column 1 -sticky ew

# または一行で
grid [label .lbl -text "Username:"] -row 0 -column 0 -sticky w
grid [entry .ent] -row 0 -column 1 -sticky ew
```

**Python (Tkinter)**:
```python
# ウィジェット作成
lbl = ttk.Label(frame, text="Username:")
ent = ttk.Entry(frame)

# grid で配置
lbl.grid(row=0, column=0, sticky=tk.W)
ent.grid(row=0, column=1, sticky=tk.EW)
```

### 完全なコード例：Tcl (wish)

**例 1: 基本的なフォーム**

```tcl
#!/usr/bin/wish
# 基本的なフォームレイアウト

# ラベルとエントリーを作成
label .name_label -text "Name:"
entry .name_entry

label .email_label -text "Email:"
entry .email_entry

# grid で配置
grid .name_label -row 0 -column 0 -sticky e -pady 5
grid .name_entry -row 0 -column 1 -sticky ew -pady 5
grid .email_label -row 1 -column 0 -sticky e -pady 5
grid .email_entry -row 1 -column 1 -sticky ew -pady 5

# 列 1 をリサイズ可能に
grid columnconfigure . 1 -weight 1

# ウィンドウタイトル
wm title . "Form Example"
```

**例 2: 複数列にまたがるボタン**

```tcl
#!/usr/bin/wish
# columnspan を使用したレイアウト

# 入力フィールド
label .user_label -text "Username:"
entry .user_entry

label .pass_label -text "Password:"
entry .pass_entry -show "*"

# ボタン
button .login_btn -text "Login" -command {puts "Login clicked"}
button .cancel_btn -text "Cancel" -command {exit}

# 配置
grid .user_label -row 0 -column 0 -sticky e -pady 5
grid .user_entry -row 0 -column 1 -sticky ew -pady 5
grid .pass_label -row 1 -column 0 -sticky e -pady 5
grid .pass_entry -row 1 -column 1 -sticky ew -pady 5

# ボタンは 2 列にまたがる（columnspan=2）
grid .login_btn -row 2 -column 0 -columnspan 2 -sticky ew -pady 10 -padx 20
grid .cancel_btn -row 3 -column 0 -columnspan 2 -sticky ew -pady 5 -padx 20

# 列設定
grid columnconfigure . 1 -weight 1
```

**例 3: 複雑なグリッドレイアウト**

```tcl
#!/usr/bin/wish
# 複雑なグリッドレイアウト

# ヘッダー
label .title -text "User Information" -font "Helvetica 14 bold"
grid .title -row 0 -column 0 -columnspan 2 -sticky nsew -pady 10

# 入力フィールド
label .fn_label -text "First Name:"
entry .fn_entry

label .ln_label -text "Last Name:"
entry .ln_entry

label .addr_label -text "Address:"
entry .addr_entry

# 配置
grid .fn_label -row 1 -column 0 -sticky e -pady 3
grid .fn_entry -row 1 -column 1 -sticky ew -pady 3
grid .ln_label -row 2 -column 0 -sticky e -pady 3
grid .ln_entry -row 2 -column 1 -sticky ew -pady 3
grid .addr_label -row 3 -column 0 -sticky ne -pady 3
grid .addr_entry -row 3 -column 1 -sticky ew -pady 3

# 列設定
grid columnconfigure . 1 -weight 1
```

### 完全なコード例：Python (Tkinter)

**例 1: 基本的なフォーム**

```python
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Form Example")

# ラベルとエントリーを作成
name_label = ttk.Label(root, text="Name:")
name_entry = ttk.Entry(root)

email_label = ttk.Label(root, text="Email:")
email_entry = ttk.Entry(root)

# grid で配置
name_label.grid(row=0, column=0, sticky=tk.E, pady=5)
name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
email_label.grid(row=1, column=0, sticky=tk.E, pady=5)
email_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

# 列 1 をリサイズ可能に
root.columnconfigure(1, weight=1)

root.mainloop()
```

### オプション解説

| オプション | 値 | 説明 |
|-----------|-----|------|
| `-row`, `-column` | 数値 | 配置位置（デフォルト: 0） |
| `-sticky` | `n`, `s`, `e`, `w` の組み合わせ | セル内での配置（方位） |
| `-columnspan`, `-rowspan` | 数値 | セルの跨がり |
| `-padx`, `-pady` | 数値 | 外側の余白 |
| `-ipadx`, `-ipady` | 数値 | 内側の余白 |

### 重要な追加設定：columnconfigure / rowconfigure

**grid の真価は `columnconfigure` と `rowconfigure` で発揮されます。**

この設定を忘れると、「ウィンドウをリサイズしてもウィジェットが拡張しない」という問題が発生します。

**Tcl (wish)**:
```tcl
# 列 0 のリサイズ重みを 1 に（均等に拡張）
grid columnconfigure . 0 -weight 1

# 列 0 の最小幅を 200 ピクセルに
grid columnconfigure . 0 -minsize 200

# 行 0 のリサイズ重みを 1 に
grid rowconfigure . 0 -weight 1

# 複数の列を一括設定（0 列目から順に weight 0, 1, 1）
grid columnconfigure . 0 -weight 0
grid columnconfigure . 1 -weight 1
grid columnconfigure . 2 -weight 1
```

**Python (Tkinter)**:
```python
# 列 0 のリサイズ重みを 1 に
root.columnconfigure(0, weight=1)

# 列 0 の最小幅を 200 ピクセルに
root.columnconfigure(0, minsize=200)

# 行 0 のリサイズ重みを 1 に
root.rowconfigure(0, weight=1)

# 複数の列を一括設定
for i in range(3):
    root.columnconfigure(i, weight=1)
```

### Tcl と Python の構文比較

| 操作 | Tcl (wish) | Python (Tkinter) |
|------|-----------|------------------|
| **列の設定** | `grid columnconfigure . 0 -weight 1` | `root.columnconfigure(0, weight=1)` |
| **行の設定** | `grid rowconfigure . 0 -weight 1` | `root.rowconfigure(0, weight=1)` |
| **複数設定** | 繰り返し呼び出す | ループで一括設定 |
| **親の指定** | `.`（ドット）で親を明示 | メソッド呼び出し元のウィジェット |

### weight（リサイズ重み）の仕組み

**weight** は、ウィンドウのリサイズ時に**余剰領域をどのように分配するか**を決定します。

```
初期状態：ウィンドウ幅 400px
┌──────────────┬──────────────┐
│   列 0       │   列 1       │
│   200px      │   200px      │
└──────────────┴──────────────┘

ウィンドウを 600px にリサイズ（+200px）

ケース 1: 両方の列に weight=1
┌──────────────┬──────────────┐
│   列 0       │   列 1       │
│   300px      │   300px      │  ← +100pxずつ分配
└──────────────┴──────────────┘

ケース 2: 列 0 のみ weight=1
┌──────────────────────┬──────┐
│   列 0               │ 列 1 │
│   400px              │200px │  ← 列 0 が全て吸収
└──────────────────────┴──────┘

ケース 3: weight 未設定（デフォルト 0）
┌──────────────┬──────────────┐
│   列 0       │   列 1       │
│   200px      │   200px      │  ← 拡張しない（余白は右側）
└──────────────┴──────────────┘
```

**HTML/CSS との比較**:

```css
/* CSS Grid */
.container {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* weight=1, weight=1 に相当 */
}

/* または */
.container {
  display: grid;
  grid-template-columns: 200px 1fr;  /* 列 0: 固定、列 1: 拡張 */
}
```

```tcl
# Tcl/Tk
grid columnconfigure . 0 -weight 1
grid columnconfigure . 1 -weight 1
```

### sticky の詳細

**sticky** は、セル内でのウィジェットの配置を制御します。方位（n, s, e, w）の組み合わせで指定します。

| 値 | 意味 | CSS での対応 |
|-----|------|-------------|
| `n` | 北（上）寄せ | `align-self: start` |
| `s` | 南（下）寄せ | `align-self: end` |
| `e` | 東（右）寄せ | `justify-self: end` |
| `w` | 西（左）寄せ | `justify-self: start` |
| `ew` | 東西に拡張 | `width: 100%` |
| `ns` | 南北に拡張 | `height: 100%` |
| `nsew` | 全方向に拡張 | `width: 100%; height: 100%` |

視覚的な例：

```
セル内にウィジェットを配置（sticky 指定なし）
┌──────────────┐
│  [widget]    │  ← 中央に配置
└──────────────┘

sticky=w
┌──────────────┐
│[widget]      │  ← 左寄せ
└──────────────┘

sticky=ew
┌──────────────┐
│[────widget────]│  ← 横に拡張
└──────────────┘

sticky=nsew
┌──────────────┐
│[───────────]│
│[──widget───]│  ← 全方向に拡張
│[───────────]│
└──────────────┘
```

### 使用例：ログインフォーム

```python
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# ラベルとエントリーをグリッド配置
ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
ttk.Entry(frame).grid(row=0, column=1, sticky=tk.EW, pady=5)

ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
ttk.Entry(frame, show="*").grid(row=1, column=1, sticky=tk.EW, pady=5)

# ボタンは 2 列にまたがる
ttk.Button(frame, text="Login").grid(row=2, column=0, columnspan=2, pady=10)

# 列 1 をリサイズ可能に
frame.columnconfigure(1, weight=1)
```

### grid のメリット

- ✅ 表形式レイアウトが直感的に記述可能
- ✅ 行またぎ、列またぎが簡単
- ✅ 後から特定のセルにウィジェットを追加可能

### grid のデメリット

- ❌ `columnconfigure`/`rowconfigure` を忘れるとレイアウトが崩れる
- ❌ pack と混在できない（同一コンテナ内）
- ❌ 複雑な階層構造では管理が困難

---

## place：絶対座標での配置

### 基本構文

**Tcl (wish)**:
```tcl
# 絶対座標で配置
place .button -x 100 -y 50 -width 80 -height 30

# 相対座標で配置（中央に配置）
place .button -relx 0.5 -rely 0.5 -anchor center

# ウィジェット作成と同時に行う
place [button .button -text "Click"] -x 50 -y 50
```

**Python (Tkinter)**:
```python
# 絶対座標で配置
button.place(x=100, y=50, width=80, height=30)

# 相対座標で配置（中央に配置）
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
```

### 絶対座標 vs 相対座標

place には 2 つの配置方法があります：

**絶対座標**（ピクセル単位）:

```tcl
; Tcl
place .button -x 100 -y 50 -width 80 -height 30
```

```python
# Python
button.place(x=100, y=50, width=80, height=30)
```

**相対座標**（0.0〜1.0 の比率）:

```tcl
; Tcl
place .button -relx 0.5 -rely 0.5 -anchor center
```

```python
# Python
button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
```

視覚的な例：

```
絶対座標（x=50, y=30）
┌────────────────────────┐
│ (0,0)                  │
│   +50px→               │
│   [button] ← (50,30)   │
│     ↑                  │
│    +30px               │
└────────────────────────┘

相対座標（relx=0.5, rely=0.5）
┌────────────────────────┐
│                        │
│         [button]       │  ← 中央に配置
│                        │
└────────────────────────┘
   ↑                ↑
  0.0              1.0
```

### オプション解説

| オプション | 値 | 説明 | HTML/CSS での対応 |
|-----------|-----|------|------------------|
| `-x`, `-y` | 数値 | 左上隅の座標（ピクセル） | `top`, `left` |
| `-width`, `-height` | 数値 | ウィジェットサイズ | `width`, `height` |
| `-relx`, `-rely` | 0.0〜1.0 | 親ウィジェットに対する相対位置 | `%`（パーセント） |
| `-relwidth`, `-relheight` | 0.0〜1.0 | 親ウィジェットに対する相対サイズ | `width: 50%` |
| `-anchor` | `n`, `s`, `e`, `w`, `center` など | 配置の基準点 | `transform-origin` |

### anchor の仕組み

**anchor** は、座標のどの位置をウィジェットの基準点とするかを指定します。

```
anchor の方位
      n
    nw ne
      +
    sw se
      s

例：anchor=nw（左上を基準）
┌────────────────────────┐
│  * (100, 50)           │
│  [────button────]      │  ← 左上隅が (100, 50)
└────────────────────────┘

例：anchor=center（中央を基準）
┌────────────────────────┐
│                        │
│      [────button────]  │
│            * (100, 50) │  ← 中央が (100, 50)
│                        │
└────────────────────────┘
```

**HTML/CSS との比較**:

```css
/* 絶対座標 */
.button {
  position: absolute;
  left: 100px;
  top: 50px;
  width: 80px;
  height: 30px;
}

/* 相対座標（中央配置）*/
.button {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);  /* anchor=center に相当 */
}
```

### 完全なコード例：Tcl (wish)

**例 1: 絶対座標での配置**

```tcl
#!/usr/bin/wish
# 絶対座標でウィジェットを配置

# 固定位置にボタンを配置
place [button .btn1 -text "Button 1"] -x 50 -y 50 -width 100 -height 30
place [button .btn2 -text "Button 2"] -x 200 -y 50 -width 100 -height 30
place [button .btn3 -text "Button 3"] -x 50 -y 150 -width 100 -height 30

# ウィンドウサイズを固定
wm geometry . 400x300
wm resizable . 0 0  # リサイズ禁止
```

**例 2: 相対座標での配置**

```tcl
#!/usr/bin/wish
# 相対座標でウィジェットを配置（リサイズ対応）

# 中央にボタンを配置
place [button .center -text "Center"] -relx 0.5 -rely 0.5 -anchor center

# 四隅にボタンを配置
place [button .tl -text "TL"] -relx 0.0 -rely 0.0 -anchor nw
place [button .tr -text "TR"] -relx 1.0 -rely 0.0 -anchor ne
place [button .bl -text "BL"] -relx 0.0 -rely 1.0 -anchor sw
place [button .br -text "BR"] -relx 1.0 -rely 1.0 -anchor se

# ウィンドウサイズ
wm geometry . 400x300
```

**例 3: オーバーレイ（ポップアップ風）**

```tcl
#!/usr/bin/wish
# place を使ったオーバーレイ表示

# メインウィンドウ
frame .main -width 300 -height 200
place .main -relx 0.5 -rely 0.5 -anchor center

# オーバーレイ（半透明風）
frame .overlay -width 200 -height 100 -bg gray
place .overlay -relx 0.5 -rely 0.5 -anchor center

# オーバーレイ内のラベル
label .overlay.msg -text "Popup Message" -bg gray -fg white
place .overlay.msg -relx 0.5 -rely 0.5 -anchor center
```

### 完全なコード例：Python (Tkinter)

**例 1: 絶対座標での配置**

```python
#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Place Demo - Absolute")

# 固定位置にボタンを配置
btn1 = ttk.Button(root, text="Button 1")
btn1.place(x=50, y=50, width=100, height=30)

btn2 = ttk.Button(root, text="Button 2")
btn2.place(x=200, y=50, width=100, height=30)

btn3 = ttk.Button(root, text="Button 3")
btn3.place(x=50, y=150, width=100, height=30)

root.geometry("400x300")
root.resizable(False, False)  # リサイズ禁止

root.mainloop()
```

### place のメリット

- ✅ 完全な制御：ピクセル単位で配置可能
- ✅ 相対座標でリサイズ対応も可能
- ✅ オーバーレイ、ポップアップに最適

### place のデメリット

- ❌ 手動調整が必要で保守性が低い
- ❌ ウィジェットサイズ変更時に再計算が必要
- ❌ 国際化（文字列の長さ変化）に弱い

---

## 重要な制約：同一コンテナ内での混在禁止

**これが最も重要なルールです：**

> ❌ **同一の親ウィジェット内で、複数のジオメトリマネージャーを混在させてはいけません。**

### エラー例

```python
frame = ttk.Frame(root)

# pack で配置
btn1 = ttk.Button(frame, text="Button 1")
btn1.pack(side=tk.LEFT)

# grid で配置 → TclError!
btn2 = ttk.Button(frame, text="Button 2")
btn2.grid(row=0, column=1)  # 💥 TclError: conflicting geometry managers
```

### 回避策：コンテナを分ける

```python
# pack 用コンテナ
pack_frame = ttk.Frame(root)
pack_frame.pack(side=tk.TOP)

ttk.Button(pack_frame, text="Button 1").pack(side=tk.LEFT)
ttk.Button(pack_frame, text="Button 2").pack(side=tk.LEFT)

# grid 用コンテナ
grid_frame = ttk.Frame(root)
grid_frame.pack(side=tk.BOTTOM)

ttk.Label(grid_frame, text="Name:").grid(row=0, column=0)
ttk.Entry(grid_frame).grid(row=0, column=1)
```

---

## リサイズ対応のベストプラクティス

### pack の場合

```python
# 親ウィジェットのリサイズに追随
frame.pack(fill=tk.BOTH, expand=True)

# 子ウィジェットも横方向に拡張
button.pack(fill=tk.X, expand=True)
```

### grid の場合

```python
# 列と行のリサイズ重みを設定
for i in range(3):
    root.columnconfigure(i, weight=1)
root.rowconfigure(0, weight=1)

# sticky でセル内での拡張を指定
widget.grid(row=0, column=0, sticky=tk.NSEW)
```

### 共通の原則

1. **最上位ウィジェットに `fill=BOTH, expand=True` を設定**
2. **中間コンテナも同様に設定**
3. **末端ウィジェットは適切な `sticky` または `fill` を設定**

---

## トラブルシューティング

### ウィジェットが表示されない

**チェックリスト:**

1. ジオメトリマネージャーを呼び出しているか？（`.pack()`, `.grid()`, `.place()`）
2. 同一コンテナ内で複数のマネージャーを混在させていないか？
3. 親ウィジェットが適切なサイズを持っているか？

### リサイズすると崩れる

**対処法:**

1. `expand=True` と `fill=BOTH` を確認
2. `columnconfigure(weight=1)` を確認
3. `sticky=NSEW` を確認

### grid で列幅が均等にならない

**対処法:**

```python
# 全ての列に weight を設定
for i in range(num_columns):
    frame.columnconfigure(i, weight=1)
```

---

## まとめ：選択の指針

| 要件 | 推奨 | 理由 |
|------|------|------|
| シンプルな配置 | pack | コード量少なく直感的 |
| フォーム | grid | 表形式が自然 |
| リサイズ対応 | grid | 細かい制御が可能 |
| 固定配置 | place | 絶対座標で正確 |
| 複合レイアウト | 入れ子構造 | pack + grid をコンテナで分離 |

**マネージャー別の適性:**

- **pack**: シンプルな縦/横並び、ツールバー、ステータスバー、階層構造が深いレイアウト、素早いプロトタイピング
- **grid**: フォーム（ラベル + 入力フィールド）、表形式、行/列またぎ、精密な位置制御
- **place**: 絶対座標の固定配置（ゲーム、キャンバス）、オーバーレイ、ポップアップ、カスタム描画

**実戦での推奨アプローチ:**

1. **大枠を pack で分割**（ツールバー、メインエリア、ステータスバー）
2. **メインエリア内は grid で精密配置**
3. **特殊な部分のみ place を使用**

このハイブリッドアプローチが、保守性と柔軟性のバランスに優れています。

---

## 参考文献

- [Tk packer manual](https://www.tcl.tk/man/tcl8.6/TkCmd/pack.htm)
- [Tk grid manual](https://www.tcl.tk/man/tcl8.6/TkCmd/grid.htm)
- [Tk place manual](https://www.tcl.tk/man/tcl8.6/TkCmd/place.htm)
- [Tkinter 8.5 reference](https://tkdocs.com/library/)

---

## 付録：実践チェックリスト

### レイアウト設計前の確認事項

- [ ] **どのマネージャーを使うか決定したか？**
  - シンプルな縦/横並び → pack
  - 表形式フォーム → grid
  - 固定配置 → place

- [ ] **コンテナ階層は明確か？**
  - 親子関係を図示できる
  - 各コンテナの役割が明確

- [ ] **リサイズ挙動は定義したか？**
  - どの列/行を拡張させるか（weight）
  - 最小サイズは何か（minsize）

### デバッグチェックリスト

**ウィジェットが表示されない場合**:

- [ ] ジオメトリマネージャーを呼び出しているか？（`.pack()`, `.grid()`, `.place()`）
- [ ] 親ウィジェットは存在するか？
- [ ] 親ウィジェットに十分なサイズがあるか？

**リサイズすると崩れる場合**:

- [ ] `expand=True` を設定しているか？
- [ ] `fill=BOTH` または `sticky=NSEW` を設定しているか？
- [ ] `columnconfigure(weight=1)` を設定しているか？

**エラー "conflicting geometry managers" が出た場合**:

- [ ] 同一コンテナ内で pack と grid を混在させていないか？
- [ ] 必要に応じてコンテナを分割したか？

### パフォーマンスヒント

- **place は控えめに**: 座標を手動管理するため保守性が低く、ウィジェットサイズや文字列長の変化に弱い
- **ネストは最小限に**: 深い階層はレイアウト計算を遅くする
- **columnconfigure/rowconfigure は一度だけ**: 繰り返し呼び出さない

---

## クイックリファレンス

### pack

```python
widget.pack(side=tk.TOP, fill=tk.X, expand=True)
```

### grid

```python
widget.grid(row=0, column=0, sticky=tk.NSEW)
parent.columnconfigure(0, weight=1)
```

### place

```python
widget.place(x=100, y=50, width=80, height=30)
# または
widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
```

