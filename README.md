# tkinter で学ぶ Tcl 言語

対象: Python 初心者〜中級者  
時間: 2時間  
Takeaway:

1. Tcl は言語仕様が Lisp に似てシンプル
2. tkinter から Tcl を使いこなせると爆速 GUI が作れる

---

## Part 1: Tcl とは何か（30分）

### Tcl の位置づけ

- Tcl = Tool Command Language
- 1988年に John Ousterhout によって作られた
- Tk = Tcl の GUI ツールキット
- Python の `tkinter` は Tcl/Tk へのラッパー

### 一切皆字符串

Tcl の最大の特徴: **すべてが文字列**。

```tcl
set name "takuya"
set age 42
set flag 1
```

見た目は型があるように見えるが、内部では全部文字列。

```tcl
set x 10
set y 20
set sum [expr {$x + $y}]   ;# 30
```

`expr` コマンドを明示的に呼ぶと、文字列が数値として評価される。

### コマンド・引数・クォート

Tcl は「コマンド 引数1 引数2 ...」の並び。

```tcl
puts hello
puts "hello world"
puts {hello world}
```

- `""` : 変数展開とコマンド置換あり
- `{}` : 生の文字列、展開なし
- `[]` : コマンド置換

```tcl
set name "takuya"
puts "hello $name"         ;# hello takuya
puts {hello $name}         ;# hello $name
puts "hello [string length $name]"   ;# hello 6
```

### 変数とスコープ

```tcl
set x 1
unset x

# 配列風
set user(name) "takuya"
set user(age) 42
puts $user(name)
```

Tcl の「配列」は連想配列。インデックスアクセスではない。

### 制御構文

```tcl
if {$x > 0} {
    puts positive
} elseif {$x < 0} {
    puts negative
} else {
    puts zero
}

foreach item {a b c} {
    puts $item
}

set i 0
while {$i < 3} {
    puts $i
    incr i
}

switch $cmd {
    a { puts alpha }
    b { puts beta }
    default { puts unknown }
}
```

注意: `{ }` で囲まないと引数が展開されて壊れる。

### proc

```tcl
proc greet {name} {
    return "hello $name"
}

puts [greet takuya]
```

デフォルト値と可変長:

```tcl
proc log {message {level info}} {
    puts "[$level] $message"
}

proc sum args {
    set total 0
    foreach n $args {
        incr total $n
    }
    return $total
}

puts [sum 1 2 3 4]
```

---

## Part 2: Tcl = Lisp っぽい（20分）

### 前置関数呼び出し

Tcl のコマンドは Lisp の S 式に似ている。

```lisp
(+ 1 2 3)        ; Lisp
```

```tcl
expr {1 + 2 + 3} ; Tcl
sum 1 2 3        ; Tcl ならもっと近い
```

違い: Tcl はカッコではなく空白区切り。カッコの代わりに `{}` や `""` でグルーピング。

### リストがコードとデータの両方

```tcl
set code {puts hello}
eval $code          ;# puts hello を実行
```

リストは文字列としても扱えるし、コマンドとして評価もできる。

```tcl
set cmd puts
$cmd hello          ;# puts hello と同じ
```

### eval / uplevel / apply

```tcl
set x 1
set script {incr x}
eval $script        ;# x = 2
```

`uplevel` は呼び出し元のスコープで実行。

```tcl
proc add_x {val} {
    uplevel 1 "incr x $val"
}

set x 10
add_x 5
puts $x             ;# 15
```

`apply` は無名関数。

```tcl
set f {{x} {expr {$x * 2}}}
puts [apply $f 5]   ;# 10
```

### 遅延評価とコマンド置換

Tcl は引数を文字列として受け取り、必要な時だけ評価する。

```tcl
proc unless {cond body} {
    if {![expr $cond]} {
        eval $body
    }
}

set x 0
unless {$x > 0} {puts "x is not positive"}
```

これが Tcl をマクロ言語として使える理由。

---

## Part 3: tkinter と Tcl/Tk（40分）

### tkinter の中身は Tcl/Tk

```python
import tkinter as tk
root = tk.Tk()
root.title("Hello")
root.mainloop()
```

Python 側で書いている `root.title(...)` は内部で Tcl コマンドを呼んでいる。

### .tcl.eval() で直接 Tcl を実行

```python
import tkinter as tk
root = tk.Tk()
root.tk.eval('puts {hello from Tcl}')
root.tk.eval('set x 42')
print(root.tk.eval('set x'))
```

これがポイント: **Python から Tcl インタープリタを直接触れる**。

### tkinter.Tcl() インタープリタ

GUI を作らずに純粋な Tcl を動かせる。

```python
import tkinter as tk
tcl = tk.Tcl()
tcl.eval('''
    proc greet {name} {
        return "hello $name"
    }
''')
print(tcl.eval('greet takuya'))
```

### Tcl スクリプトをファイルから読み込む

```tcl
# app.tcl
pack [button .b -text "Click" -command {puts clicked}]
```

```python
import tkinter as tk
root = tk.Tk()
root.tk.eval(open('app.tcl').read())
root.mainloop()
```

GUI のレイアウトを Tcl 側に任せられる。

### bind / after / event の Tcl 側理解

`bind` はイベントとコマンドを結びつける。

```tcl
bind .b <Button-1> {puts "button clicked"}
```

`after` は遅延実行。

```tcl
after 1000 {puts "1 second later"}
```

`event generate` はイベントを人工的に発火。

```tcl
event generate .b <Button-1>
```

これらは Python 側の `widget.bind()`、`root.after()`、`widget.event_generate()` の裏にある Tcl コマンド。

---

## 休憩（10分）

---

## Part 4: 爆速 GUI 実習 — canvas アニメ（40分）

### なぜ canvas アニメか

- tkinter の Canvas は Tcl/Tk ネイティブ機能
- `.create_oval()` / `.coords()` / `.move()` を Tcl 側で直接叩ける
- アニメーションループは `after` で実現
- 視覚的に「爆速 GUI」が実感しやすい
- Python 初心者でも楽しい

### 実習 1: Canvas で円を描く

```python
import tkinter as tk

root = tk.Tk()
root.tk.eval('''
    canvas .c -width 400 -height 300 -bg white
    pack .c

    .c create oval 50 50 100 100 -fill red -tags ball
''')
root.mainloop()
```

### 実習 2: Tcl 側でアニメーションループ

```python
import tkinter as tk

root = tk.Tk()
root.tk.eval('''
    canvas .c -width 400 -height 300 -bg white
    pack .c

    .c create oval 50 50 100 100 -fill red -tags ball

    set x 50
    set dx 5

    proc animate {} {
        global x dx
        .c move ball $dx 0
        incr x $dx
        if {$x > 300 || $x < 50} {
            set dx [expr {-$dx}]
        }
        after 16 animate
    }

    animate
''')
root.mainloop()
```

### 実習 3: マウスクリックで弾むボール

```python
import tkinter as tk

root = tk.Tk()
root.title("Bouncing Ball")
root.tk.eval('''
    canvas .c -width 400 -height 300 -bg white
    pack .c

    .c create oval 180 130 220 170 -fill blue -tags ball

    set vx 4
    set vy 3
    set x 200
    set y 150
    set r 20

    proc update {} {
        global x y vx vy r
        set width 400
        set height 300

        set x [expr {$x + $vx}]
        set y [expr {$y + $vy}]

        if {$x - $r < 0 || $x + $r > $width} {set vx [expr {-$vx}]}
        if {$y - $r < 0 || $y + $r > $height} {set vy [expr {-$vy}]}

        .c coords ball [expr {$x-$r}] [expr {$y-$r}] [expr {$x+$r}] [expr {$y+$r}]
        after 16 update
    }

    bind .c <Button-1> {
        set vx [expr {int(rand()*10) - 5}]
        set vy [expr {int(rand()*10) - 5}]
    }

    update
''')
root.mainloop()
```

### 実習 4: 複数ボール（list と proc の応用）

```python
import tkinter as tk

root = tk.Tk()
root.tk.eval('''
    canvas .c -width 400 -height 300 -bg white
    pack .c

    proc make_ball {cx cy r color} {
        set id [.c create oval [expr {$cx-$r}] [expr {$cy-$r}] \
                                  [expr {$cx+$r}] [expr {$cy+$r}] \
                                  -fill $color]
        return [list $id $cx $cy $r [expr {int(rand()*6)-3}] [expr {int(rand()*6)-3}]]
    }

    set balls {}
    foreach color {red green blue} {
        lappend balls [make_ball [expr {100+int(rand()*200)}] \
                                 [expr {100+int(rand()*100)}] \
                                 15 $color]
    }

    proc update_all {} {
        global balls
        set i 0
        foreach ball $balls {
            lassign $ball id x y r vx vy
            set x [expr {$x + $vx}]
            set y [expr {$y + $vy}]
            if {$x - $r < 0 || $x + $r > 400} {set vx [expr {-$vx}]}
            if {$y - $r < 0 || $y + $r > 300} {set vy [expr {-$vy}]}
            .c coords $id [expr {$x-$r}] [expr {$y-$r}] [expr {$x+$r}] [expr {$y+$r}]
            # 要素のコピー $ball ではなく元リスト $balls の該当インデックスを直接更新する
            lset balls $i 1 $x
            lset balls $i 2 $y
            lset balls $i 4 $vx
            lset balls $i 5 $vy
            incr i
        }
        after 16 update_all
    }

    update_all
''')
root.mainloop()
```

---

## Part 5: ootcl / list / dict / array と dict の使い分け（15分）

### ootcl とは

ootcl = Object Oriented Tcl。Tcl 8.6 以降の `oo::class` でオブジェクト指向を実現。

```tcl
oo::class create Person {
    variable name

    constructor {n} {
        set name $n
    }

    method greet {} {
        puts "hello, $name"
    }
}

set p [Person new takuya]
$p greet
```

GUI の部品をクラスとして抽象化する時に使える。

### list と dict

Tcl の本丸データ構造。

```tcl
# list
set colors {red green blue}
lappend colors yellow
puts [lindex $colors 0]
puts [llength $colors]

foreach c $colors {
    puts $c
}

# dict
set user [dict create name takuya age 42]
dict set user city tokyo
puts [dict get $user name]
```

list は Tcl の中核。dict は Tcl 8.5 から追加された。

### array と dict の使い分け

- 伝統的な Tcl array は連想配列だが、構文が特殊
- dict の方が第一級オブジェクトとして扱いやすい
- **array は公式に非推奨ではない**（現在も完全にサポートされ、性能面で優れる場面もある）
- ただし可読性の観点から、新規コードでは dict を推奨
- array はレガシーや既存コードで遭遇する程度

```tcl
# array（旧）
set user(name) takuya
set user(age) 42
puts $user(name)
parray user

# dict（新）
set user [dict create name takuya age 42]
puts [dict get $user name]
```

dict を使うメリット:

- 変数として値渡しできる
- `dict with` / `dict for` / `dict filter` が豊富
- JSON 的な構造に近い

---

## まとめと次の1手

Takeaway:

1. Tcl は Lisp に似たシンプルな言語仕様
2. tkinter から Tcl を使いこなせると爆速 GUI が作れる

次の1手:

- 自分で1つ Tcl スクリプトを書く
- `tkinter.Tcl()` で純粋な Tcl を動かしてみる
- canvas アニメを1つ改造してみる

---

## 関連ドキュメント・参考資料

- [Tcl/Tk ジオメトリマネージャー完全ガイド](docs/geometry-managers.md)
- [Flutter 開発者のための Tcl/Tk 完全ガイド](docs/flutter-guide.md)
- Tcl Developer Site: https://www.tcl.tk/
- Python tkinter docs: https://docs.python.org/3/library/tkinter.html
- Tcl 8.6 OO: https://www.tcl.tk/man/tcl8.6/TclCmd/define.htm

---

## 講師メモ

- Python 初心者には `puts` / `set` / `proc` の3つを最初に覚えさせる
- 中級者には `eval` / `uplevel` / `apply` の遅延評価を強調
- 実習ではコピペから始めて、最後に1行だけ書き換えさせる
- 2時間では深くなりすぎない。テイクアウェイ2つを繰り返す
- array は非推奨ではないが「レガシーで遭遇したら dict に置き換えられる」と伝える
