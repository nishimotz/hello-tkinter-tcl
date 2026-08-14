# Python bundled Tcl/Tk version history and tkinter feature changes

> Python の Tkinter ラッパー、公式 CPython バイナリに同梱されてきた Tcl/Tk のバージョン、
> および実行時バージョンの確認方法についての簡潔な参照ガイド。
> 2026 年 8 月時点で、Python 3.13.x 公式バイナリは Tcl/Tk 8.6、Python 3.14.x 公式バイナリは Tcl/Tk 9.0.4 を同梱しています。

---

## TL;DR: 実際の Tcl/Tk バージョンを確認する

### Python / tkinter から

```python
import tkinter

# すべてのサポート対象 Python バージョンで動作
print(tkinter.Tcl().eval('info patchlevel'))

# Python 3.11+: sys.version_info のような named tuple を返す
print(tkinter.Tcl().info_patchlevel())
```

- `info patchlevel` は `8.6.18` や `9.0.4`、`9.1b0` などの文字列を返します。
- `tkinter.Tcl().info_patchlevel()` は `major`, `minor`, `micro`, `releaselevel`, `serial` のフィールドを持つ named tuple を返します。

### Tcl/Tk から

```tcl
puts [info patchlevel]
# または、より限定的な:
puts $tk_version
```

- `$tk_version` は短いバージョン（例: `8.6` や `9.0`）のみを返します。完全な patchlevel を得るには `info patchlevel` を使ってください。

出典:

- [docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)
- [docs.python.org/3/whatsnew/3.11.html#tkinter](https://docs.python.org/3/whatsnew/3.11.html#tkinter)

---

## 1. 公式 CPython バイナリに同梱されてきた Tcl/Tk バージョン

### 「公式バイナリ」の意味

[python.org](https://www.python.org/downloads/) から配布されている CPython の公式インストーラーは、
**Windows** および **macOS** 用に Tcl/Tk ライブラリを同梱しています。
ほとんどの **Linux** ディストリビューションでは、`python3-tk` / `tkinter` パッケージがシステムの Tcl/Tk ライブラリに対してビルドされるため、バージョンはディストリビューションが提供するものになります。

### 重要な注意事項

- Python 3.11 以降は Tcl/Tk 8.5.12 より古いバージョンをサポートしなくなりました。
- Python 3.13.x までの公式バイナリは Tcl/Tk 8.6 を同梱していましたが、**Python 3.14.x から公式バイナリは Tcl/Tk 9.0.4 に移行**しました。
- 正確な同梱バージョンは CPython のビルドスクリプトで確認できます:
  - Windows: `PCbuild/tcltk.props` 内の `TclVersion`（3.13.x は `8.6.15.0`、3.14.x は `9.0.4.0`）
  - macOS: `Mac/BuildScript/build-installer.py` 内の `tcl_tk_ver`（3.13.x は `8.6.18`、3.14.x は `9.0.4`）
- 参考 Issue: `gh-104399`（Tcl 9.0 へのビルド準備）、`gh-124111`（macOS/Windows ビルドを Tcl/Tk 9.0.4 に更新）
- 一部のドキュメント（`tkinter.rst` の 3.13/3.14 ブランチや `Mac/BuildScript/README.rst`）はまだ「8.6 同梱」と記述している箇所があり、ビルド設定より遅れている可能性があります。一次情報は上記のビルドスクリプトです。
- 自分のインストール環境では常に `info patchlevel` を使って確認してください。

### Python リリース別の概略マッピング

| CPython | リリース時期 | 公式 Windows/macOS バイナリに同梱された Tcl/Tk | 備考 |
|---|---|---|---|
| 3.9.x | 2020年10月 | 8.6.x（正確な patchlevel は未公開） | |
| 3.10.x | 2021年10月 | 8.6.x（正確な patchlevel は未公開） | macOS 3.10.0 インストーラは Monterey での Tk 問題修正のため後に再ビルドされた |
| 3.11.x | 2022年10月 | 8.6.x（正確な patchlevel は未公開） | サポート対象最低 Tcl/Tk を 8.5.12 に引き上げ |
| 3.12.x | 2023年10月 | 8.6.x（正確な patchlevel は未公開） | |
| 3.13.x | 2024年10月 | **8.6.x**（Windows 8.6.15、macOS 8.6.18） | Tcl/Tk 8 系の最終同梱系列 |
| 3.14.x | 2025年10月 | **9.0.4**（Windows 9.0.4.0、macOS 9.0.4） | Tcl/Tk 9 への移行；macOS では 3.14.0 beta/RC 頃に 8.6.16 → 9.0.4 に切り替わった |
| 3.15.x | 2026年10月（予定） | **9.0.4**（Windows 9.0.4.0、macOS 9.0.4） | Tcl/Tk 9 同梱を継続；3.15.0a1 では 9.0.2、a6 では 9.0.3 に更新、現行ビルドは 9.0.4 |
| 3.16.x | 2027年10月（予定） | **9.0.4**（Windows 9.0.4.0、macOS 9.0.4） | main ブランチ；今後 9.0.5 などのマイナー更新が入る可能性あり |

任意のインストール済みインタプリタで正確な値を調べるには:

```python
import tkinter
print(tkinter.Tcl().eval('info patchlevel'))
```

出典:

- [docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)
- [docs.python.org/3/whatsnew/3.11.html#build-changes](https://docs.python.org/3/whatsnew/3.11.html#build-changes)
- [python.org release pages](https://www.python.org/downloads/release/python-3130/)

---

## 2. Tcl/Tk バージョンのマイルストーン（tkinter 利用者に関係するハイライト）

### 凡例

各メジャー Tcl/Tk リリースについて、Python tkinter プログラマーに最も影響する 2〜5 項目を挙げています。
「Tcl」とマークされたものは言語レベル、「Tk」とマークされたものは GUI/ツールキットレベルです。

### Tcl/Tk 8.0（1997年、最終 8.0.5 は 1999-03-09）

- **Tk のネイティブルックアンドフィール**: Windows とクラシック Mac OS でネイティブな外観を提供。
- **Tcl バイトコードコンパイラ**: スクリプトをバイトコードにコンパイルし高速実行を実現。
- **Tcl に namespace を導入**: より良いモジュール性のため `namespace` を追加。
- **Tk の新しいフォント機構**: クロスプラットフォームのフォント制御のため `font` コマンドを導入。

出典: [tcl-lang.org/software/tcltk/8.0.html](https://www.tcl-lang.org/software/tcltk/8.0.html)

### Tcl/Tk 8.1（1999年、最終 8.1.1 は 1999-05-26）

- **スレッド安全性**: Tcl 8.1 でスレッドセーフなコアが導入された。
- **Unicode サポート**: Tcl における初期の Unicode 文字列サポート。
- **新しい正規表現エンジン**: 高度な正規表現サポートを追加。
- **Safe interps**: セーフ Tcl インタプリタの改善。

出典: [tcl-lang.org/software/tcltk/8.1.html](https://www.tcl-lang.org/software/tcltk/8.1.html)

### Tcl/Tk 8.2（1999年、最終 8.2.3 は 1999-12-16）

- **TEA（Tcl Extension Architecture）**: C 拡張のビルドを標準化。
- **スタック型 I/O チャネル**: レイヤー化されたチャネル変換を可能に。
- **パフォーマンス改善**: 文字列操作が特に高速化された。
- **Windows での DDE**: `dde` コマンドによる Dynamic Data Exchange。

出典: [tcl-lang.org/software/tcltk/8.2.html](https://www.tcl-lang.org/software/tcltk/8.2.html)

### Tcl/Tk 8.3（2000–2002年、最終 8.3.5 は 2002-10-18）

- **Entry バリデーション**: Tk の entry ウィジェットに `-validate` / `-validatecommand` が追加。
- **画像のアルファチャネル**: photo 画像における初期のアルファチャネル対応。
- **`lsort -unique`**: リストをソートし重複を除去。
- **Canvas タグの論理検索**: canvas タグに対するより豊かな検索表現。

出典: [tcl-lang.org/software/tcltk/8.3.html](https://www.tcl-lang.org/software/tcltk/8.3.html)

### Tcl/Tk 8.4（2002–2013年、最終 8.4.20 は 2013-06-01）

- **Spinbox, PanedWindow, LabelFrame**: 新しいコア Tk ウィジェット。
- **Text ウィジェットの undo/redo**: 組み込みの undo/redo サポート。
- **仮想ファイルシステム（VFS）/ Starkits**: パッケージングと実行時アーカイブ対応。
- **`lset` と `eq`/`ne` 演算子**: リスト代入と文字列等価演算子。
- **Aqua ポートの成熟**: macOS ネイティブ Tk がさらに改善。

出典: [tcl-lang.org/software/tcltk/8.4.html](https://www.tcl-lang.org/software/tcltk/8.4.html)

### Tcl/Tk 8.5（2007年、最終 8.5.19 は 2016-02-12）

- **Themed Tk（Ttk）**: Ttk が Tk コアの一部となったため、`tkinter.ttk` ウィジェットが利用可能に。Python tkinter ユーザーにとって最大の GUI 変更点。
- **X11 でのアンチエイリアスフォントとモダン外観**: Linux/Unix 上での外観が大幅に改善。
- **フルスクリーンサポート**: `wm attributes -fullscreen`。
- **Tcl に `dict` オブジェクト型と bignum 演算**。

出典:

- [tcl-lang.org/software/tcltk/8.5.html](https://www.tcl-lang.org/software/tcltk/8.5.html)
- [docs.python.org/3/library/tkinter.html#tkinter-modules](https://docs.python.org/3/library/tkinter.html#tkinter-modules)

### Tcl/Tk 8.6（2012年、最新 8.6.18 は 2026-05-11）

- **Tk での PNG 画像サポート**: Tk 8.6 以降、`tkinter.PhotoImage` で PNG の読み書きが可能。
- **`tk busy`**: ウィンドウのインタラクティビティを一時停止/復帰。Python 3.13 では `tk_busy_*` メソッドとして公開。
- **`tk fontchooser`**: ポータブルなフォント選択ダイアログ。
- **Canvas text の `-angle`**: canvas テキストアイテムを回転。
- **スレッド対応がデフォルトに**: 公式ビルドでスレッドが有効化される。

出典:

- [tcl-lang.org/software/tcltk/8.6.html](https://www.tcl-lang.org/software/tcltk/8.6.html)
- [docs.python.org/3/library/tkinter.html#images](https://docs.python.org/3/library/tkinter.html#images)

### Tcl/Tk 8.7（alpha、最新 8.7a5 は 2021-06-18）

- **拡張 Unicode サポート**。
- **Zip アーカイブ / VFS 統合の改善**。
- **`epoll`/`kqueue` notifier**: イベントループのスケーラビリティ向上。
- **`regsub -command`**: コマンドコールバックによる置換生成。
- **システムトレイ / 通知**: 初期のプラットフォーム通知サポート。

出典: [tcl-lang.org/software/tcltk/8.7.html](https://www.tcl-lang.org/software/tcltk/8.7.html)

### Tcl/Tk 9.0（2024年、最新 9.0.4 は 2026-06-26）

- **SVG 画像サポート**: Tk 9.0 以降、`tkinter.PhotoImage` で SVG ファイルを読み込み可能。
- **フルアルファチャネルと photo メタデータ**: アルファの読み書きと画像メタデータ。
- **ウィンドウマネージャ属性**: macOS で `appearance`, `class`, `stylemask`, `tabbingid`, `tabbingmode`；Windows で `appearance`。
- **OS 統合**: `tk sysnotify`, `tk systray`, `tk print`。
- **Tcl における 64 ビット容量、完全な Unicode コードポイント、zip ファイルシステム**。
- **重要な互換性注意**: Tcl/Tk 9 は意図的に Tcl/Tk 8 との完全な ABI 互換性を持たない。拡張モジュールは再ビルドが必要。

出典:

- [tcl-lang.org/software/tcltk/9.0.html](https://www.tcl-lang.org/software/tcltk/9.0.html)
- [docs.python.org/3/library/tkinter.html#images](https://docs.python.org/3/library/tkinter.html#images)
- [docs.python.org/3/library/tkinter.html#wm-mixin](https://docs.python.org/3/library/tkinter.html#wm-mixin)

### Tcl/Tk 9.1（beta、最新 9.1b0 は 2026-06-30）

- **Tcl における Unicode 正規化** サポート。
- **モノトニックタイマー** サポート。
- **`lfilter`**: リストフィルタリングコマンド。
- **`vsapi` toggleswitch**: 新しいテーマウィジェット機能。
- **アクセシビリティ / スクリーンリーダー** 改善。
- **RTL / bidi テキスト** サポート。
- **`tk attribtable`**: より豊かな属性イントロスペクション。
- **ラベルテキストの回転** サポート。

出典: [tcl-lang.org/software/tcltk/9.1.html](https://www.tcl-lang.org/software/tcltk/9.1.html)

---

## 3. Tcl/Tk バージョンに対応する Python tkinter の変更点

以下は、基盤となる Tcl/Tk の機能を Python 側から公開する tkinter 側の変更点です。
導入された Python リリース別にグループ化しています。

### Python 3.8

- `tkinter.Spinbox` に選択メソッドが追加（`selection_from`, `selection_present`, `selection_range`, `selection_to`）。
- `tkinter.Canvas.moveto(...)` が追加。

出典:

- [docs.python.org/3/library/tkinter.html#spinbox](https://docs.python.org/3/library/tkinter.html#spinbox)
- [docs.python.org/3/library/tkinter.html#canvas](https://docs.python.org/3/library/tkinter.html#canvas)

### Python 3.11

- `tkinter.Tcl().info_patchlevel()` が追加: 実行時の Tcl/Tk patchlevel を `sys.version_info` に似た named tuple で返す。
- サポート対象最低 Tcl/Tk を **8.5.12** に引き上げ、それより古いバージョンはサポート対象外に。
- POSIX で Tcl/Tk ヘッダー/ライブラリを検出するために `pkg-config` が必要に。古い `--with-tcltk-*` configure フラグは削除された。

出典:

- [docs.python.org/3/whatsnew/3.11.html#tkinter](https://docs.python.org/3/whatsnew/3.11.html#tkinter)
- [docs.python.org/3/whatsnew/3.11.html#build-changes](https://docs.python.org/3/whatsnew/3.11.html#build-changes)

### Python 3.12

- `tkinter.Canvas.coords()` がより柔軟な座標形式（個別の数値、単一シーケンス、またはグループ化されたペア）を受け入れるようになり、基盤の Tk コマンドに合わせた。

出典: [docs.python.org/3/library/tkinter.html#canvas](https://docs.python.org/3/library/tkinter.html#canvas)

### Python 3.13

- `tkinter.tix` を削除（Python 3.6 から非推奨；基盤の Tix ライブラリはメンテナンスされていない）。
- 新しい "busy" ウィンドウメソッド: `tk_busy_hold()`, `tk_busy_configure()`, `tk_busy_cget()`, `tk_busy_forget()`, `tk_busy_status()`, `tk_busy_current()`。
- `Wm.attributes()` / `wm_attributes()` の改善:
  - 属性名を先頭の `-` なしで問い合わせ可能（例: `w.wm_attributes('alpha')`）。
  - キーワード引数で属性を設定可能（例: `w.wm_attributes(alpha=0.5)`）。
  - 新しい `return_python_dict` パラメータ。
- `Text.count(..., return_ints=False)` に `return_ints` パラメータを追加。
- `Text.edit_undo()` / `Text.edit_redo()` が Tk 9.0 実行時には変更されたインデックスのタプルを返すように。
- `after_info(id=None)` を追加。
- `ttk.Style.element_create()` が "vsapi" 要素タイプをサポート。
- `PhotoImage` 強化:
  - 新しい `copy_replace()` メソッド。
  - `copy()`, `zoom()`, `subsample()` に `from_coords=` を追加。
  - `copy()` に `zoom=` と `subsample=` を追加。
  - 新しい `data()` と `read()` メソッド。
  - `write()` に `from_coords=`, `background=`, `grayscale=` を追加。
- `Misc.register(func, ...)` の引数が文字列に変換されなくなった。
- `Misc.unbind(sequence, funcid=None)` が `funcid` 指定時に指定したコールバックのみを削除するように。
- `tkinter.Variable.trace_variable()`, `trace_vdelete()`, `trace_vinfo()` が非推奨に（Tcl 9.0 で削除された機能をラップするため）。代わりに `trace_add()`, `trace_remove()`, `trace_info()` を使う。

出典:

- [docs.python.org/3/whatsnew/3.13.html#tkinter](https://docs.python.org/3/whatsnew/3.13.html#tkinter)
- [docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)

### Python 3.14

- `after(ms, func, *args, **kw)` と `after_idle(func, *args, **kw)` がキーワード引数をコールバックに渡すようになった。
- `tkinter.OptionMenu(..., name=...)` キーワード引数を追加。`ttk.OptionMenu` でも同様。
- 公式バイナリの同梱 Tcl/Tk を 8.6 から **9.0.4** に移行（Windows/macOS）。

出典:

- [docs.python.org/3/whatsnew/3.14.html#tkinter](https://docs.python.org/3/whatsnew/3.14.html#tkinter)
- [github.com/python/cpython/blob/3.14/PCbuild/tcltk.props](https://github.com/python/cpython/blob/3.14/PCbuild/tcltk.props)
- [github.com/python/cpython/blob/3.14/Mac/BuildScript/build-installer.py](https://github.com/python/cpython/blob/3.14/Mac/BuildScript/build-installer.py)

### Python 3.15 / 3.16

- Python 3.15 / 3.16 の公式バイナリも Tcl/Tk 9 系を同梱する見込みです。
- 2026 年 8 月時点の CPython `main`（3.16）および `3.15` ブランチでは、Windows/macOS ともに **Tcl/Tk 9.0.4** が設定されています。
- macOS では、ビルドホストが macOS 10.15 未満の場合のみ後方互換用に 8.6.8 が使われる分岐があります（`Mac/BuildScript/build-installer.py` の `useOldTk()`）。
- 主要な更新コミット:
  - main: `PCbuild/tcltk.props` 9.0.3 → 9.0.4 ([46e950f](https://github.com/python/cpython/commit/46e950fc0df8ad300497d612c4c9de3e5a1e87f3)) / `build-installer.py` 9.0.3 → 9.0.4 ([d478cf8](https://github.com/python/cpython/commit/d478cf81f770168e3fb512ce110a88774f04f549))
  - 3.15: `PCbuild/tcltk.props` 9.0.3 → 9.0.4 ([13e7aed](https://github.com/python/cpython/commit/13e7aedb59230f941419b5e64977e8f8b6db871f)) / `build-installer.py` 9.0.3 → 9.0.4 ([d87949b](https://github.com/python/cpython/commit/d87949b72b32529753e8fbd9f8be41914ce0a558))
- 参考 issue/PR: `gh-124111`, `gh-124156`, `gh-153901`, `gh-153990`, `gh-153868`, `gh-153871`
- リリース時期（PEP）:
  - Python 3.15: [PEP 790](https://peps.python.org/pep-0790/) — 3.15.0 final 予定 2026-10-01
  - Python 3.16: [PEP 826](https://peps.python.org/pep-0826/) — 3.16.0 final 予定 2027-10-05

出典:

- [github.com/python/cpython/blob/main/PCbuild/tcltk.props](https://github.com/python/cpython/blob/main/PCbuild/tcltk.props)
- [github.com/python/cpython/blob/main/Mac/BuildScript/build-installer.py](https://github.com/python/cpython/blob/main/Mac/BuildScript/build-installer.py)
- [PEP 790 – Python 3.15 Release Schedule](https://peps.python.org/pep-0790/)
- [PEP 826 – Python 3.16 Release Schedule](https://peps.python.org/pep-0826/)

---

## 4. 一般的な tkinter 機能に対する Tk/Ttk バージョン要件

| 機能 | 必要なバージョン | 備考 |
|---|---|---|
| `tkinter.ttk` テーマウィジェット | Tk 8.5+ | 8.5 から Tk コアに含まれる |
| `PhotoImage` PNG 読み書き | Tk 8.6+ | |
| `PhotoImage` SVG 読み込み | Tk 9.0+ | |
| `PhotoImage` フルアルファ/メタデータ | Tk 9.0+ | |
| Canvas text `-angle` | Tk 8.6+ | |
| Canvas text `-underline` | Tk 9.0+ | |
| `wm_attributes -type`（X11） | Tk 8.6+ | |
| `wm_attributes -appearance`（Windows/macOS）、`-class`/`-stylemask`/`-tabbingid`/`-tabbingmode`（macOS） | Tk 9.0+ | |
| `tk busy`（busy ウィンドウ状態） | Tk 8.6+ | Python 3.13 で `tk_busy_*` として公開 |
| `tk fontchooser` | Tk 8.6+ | |
| `Text` タグオプション `lmargincolor`, `overstrikefg`, `rmargincolor`, `selectbackground`, `selectforeground`, `underlinefg` | Tk 8.6+ | |

出典:

- [docs.python.org/3/library/tkinter.html](https://docs.python.org/3/library/tkinter.html)
- [docs.python.org/3/library/tkinter.html#tkinter-modules](https://docs.python.org/3/library/tkinter.html#tkinter-modules)
- [tcl-lang.org/software/tcltk/9.0.html](https://www.tcl-lang.org/software/tcltk/9.0.html)
- [tcl-lang.org/software/tcltk/8.6.html](https://www.tcl-lang.org/software/tcltk/8.6.html)

---

## 5. スレッドに関する注意

Tcl/Tk は単一スレッド/イベント駆動ですが、
現代の公式ビルド（CPython バイナリに同梱されている Tcl/Tk 8.6 を含む）はスレッド対応でビルドされています。
そのため、`tkinter` はあらゆる Python スレッドからの呼び出しを、Tcl インタプリタのイベントキューにイベントを投稿することで許可しています。

出典: [docs.python.org/3/library/tkinter.html#threading-model](https://docs.python.org/3/library/tkinter.html#threading-model)

---

## 6. 参考資料

- Python tkinter ドキュメント: <https://docs.python.org/3/library/tkinter.html>
- "What's New" tkinter セクション:
  - 3.11: <https://docs.python.org/3/whatsnew/3.11.html#tkinter>
  - 3.13: <https://docs.python.org/3/whatsnew/3.13.html#tkinter>
  - 3.14: <https://docs.python.org/3/whatsnew/3.14.html#tkinter>
- Tcl/Tk プロジェクトのバージョンページ:
  - 8.0: <https://www.tcl-lang.org/software/tcltk/8.0.html>
  - 8.1: <https://www.tcl-lang.org/software/tcltk/8.1.html>
  - 8.2: <https://www.tcl-lang.org/software/tcltk/8.2.html>
  - 8.3: <https://www.tcl-lang.org/software/tcltk/8.3.html>
  - 8.4: <https://www.tcl-lang.org/software/tcltk/8.4.html>
  - 8.5: <https://www.tcl-lang.org/software/tcltk/8.5.html>
  - 8.6: <https://www.tcl-lang.org/software/tcltk/8.6.html>
  - 8.7: <https://www.tcl-lang.org/software/tcltk/8.7.html>
  - 9.0: <https://www.tcl-lang.org/software/tcltk/9.0.html>
  - 9.1: <https://www.tcl-lang.org/software/tcltk/9.1.html>
- CPython リリースページ: <https://www.python.org/downloads/release/python-3130/>（3.9〜3.12 も同様）

---

*最終更新: 2026-08-14 時点の情報に基づく。特定の CPython リリースに同梱された Tcl/Tk の正確な patchlevel は、
`tkinter.Tcl().eval('info patchlevel')` で実行時に確認してください。最新のビルド設定は CPython リポジトリの
`PCbuild/tcltk.props`（Windows）および `Mac/BuildScript/build-installer.py`（macOS）で確認できます。*
