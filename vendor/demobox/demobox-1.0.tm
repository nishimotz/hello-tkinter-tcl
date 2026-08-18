# demobox-1.0.tm — Tcl モジュール demobox。
#
# tkinter の Canvas に複数の弾むボールのアニメーションを追加する、
# 純 Tcl のパッケージ。Python 側は "package require demobox" して
# Tcl コマンドを呼ぶだけで、アニメーションループは全て Tcl の
# after で回す（Python のイベントループをブロックしない）。
#
# このパッケージは「Tcl エコシステムの拡張を vendoring して
# tkinter から使う」仕組みの最小デモ。pkgIndex.tcl が指す .tm 形式。
#
# コマンド:
#   demobox::start path ?n? ?fps?
#       指定した canvas パスにボールを n 個（デフォルト 30）作り、
#       アニメーションを開始する。
#   demobox::stop  path
#       path のアニメーションを停止し、canvas を破棄する。
#   demobox::speed path fps
#       アニメーションの FPS を変更する。
#   demobox::add  path ?n?
#       既存の canvas にボールを n 個追加する。
#
# 各ボールは canvas アイテムのタグ "ball<i>" で識別し、状態は
# demobox::ball(path,id) の連想配列（Tcl array）に保持する。
# 大量のボールでも Tcl の after ループ1本で全ボールを更新するので、
# 滑らかさと速度の体感を同時に示せる。

package require Tk

namespace eval demobox {
    variable after_id {}    ;# after ハンドラのID（グローバル管理）
    variable fps 60
    # ball(path,id) -> "x y r vx vy" 形式の文字列（list）。
    variable ball

    proc start {path {n 30} {fps 60}} {
        variable after_id
        variable ball

        # canvas が無ければ新規作成。既に存在する canvas（tkinter の
        # Canvas など）があれば再利用して、ボールを描画する。
        # 既存 canvas の場合、pack はしない（レイアウトは呼び出し側が持つ）。
        if {![winfo exists $path]} {
            canvas $path -width 640 -height 400 -bg white
            pack $path -fill both -expand true
        }

        # 前回のアニメーションとボールをクリア（再開を安全に）。
        after cancel $after_id
        set after_id {}
        foreach key [array names ball "$path,*"] {
            set id [lindex [split $key ","] end]
            $path delete ball$id
        }
        array unset ball "$path,*"

        set ::demobox::fps $fps
        set w [winfo width  $path]
        set h [winfo height $path]
        if {$w <= 1} {set w 640}
        if {$h <= 1} {set h 400}
        _spawn $path $n $w $h

        after cancel $after_id
        set after_id [after [expr {1000 / $fps}] \
                          [list ::demobox::tick $path]]
        return $path
    }

    proc stop {path} {
        variable after_id
        variable ball
        after cancel $after_id
        set after_id {}
        if {[winfo exists $path]} {
            # ボールのアイテムと状態を消す。canvas 自体は破壊しない
            # （tkinter が所有する stage canvas を再利用しているため）。
            foreach key [array names ball "$path,*"] {
                set id [lindex [split $key ","] end]
                $path delete ball$id
            }
            array unset ball "$path,*"
        }
        return
    }

    proc speed {path fps} {
        variable after_id
        set ::demobox::fps $fps
        # 次の tick から新しい間隔で回るように after を張り直す。
        after cancel $after_id
        set after_id [after [expr {1000 / $fps}] \
                          [list ::demobox::tick $path]]
        return $fps
    }

    proc add {path {n 10}} {
        variable ball
        if {![winfo exists $path]} {
            return -code error "canvas $path does not exist"
        }
        set w [winfo width  $path]
        set h [winfo height $path]
        _spawn $path $n $w $h
        return $n
    }

    # _spawn path n w h — ボールを n 個生成して状態を記録する。
    proc _spawn {path n w h} {
        variable ball
        for {set i 0} {$i < $n} {incr i} {
            set r   [expr {8 + int(rand() * 14)}]
            set x   [expr {double($r) + rand() * ($w - 2 * $r)}]
            set y   [expr {double($r) + rand() * ($h - 2 * $r)}]
            set vx  [expr {int(rand() * 6) - 3}]
            set vy  [expr {int(rand() * 6) - 3}]
            if {$vx == 0} {set vx 2}
            if {$vy == 0} {set vy 2}
            set id [expr {[llength [array names ball "$path,*"]]}]
            # canvas アイテムを作る。タグ "ball$id" で coords を参照する。
            $path create oval \
                [expr {$x - $r}] [expr {$y - $r}] \
                [expr {$x + $r}] [expr {$y + $r}] \
                -fill [lindex {red blue green orange purple teal} \
                           [expr {$id % 6}]] \
                -tags "ball$id"
            set ball($path,$id) "$x $y $r $vx $vy"
        }
        return
    }

    proc tick {path} {
        variable after_id
        variable ball

        if {![winfo exists $path]} {
            # canvas が消えていたら停止。
            return
        }

        set width  [winfo width  $path]
        set height [winfo height $path]

        # 全ボールの状態を一括更新。
        foreach key [array names ball "$path,*"] {
            # key は "path,id" 形式。id をタグ名に使う。
            set id [lindex [split $key ","] end]
            lassign $ball($key) x y r vx vy

            set x [expr {$x + $vx}]
            set y [expr {$y + $vy}]

            if {$x - $r < 0 || $x + $r > $width}  {set vx [expr {-$vx}]}
            if {$y - $r < 0 || $y + $r > $height} {set vy [expr {-$vy}]}

            set ball($key) "$x $y $r $vx $vy"
            $path coords ball$id \
                [expr {$x - $r}] [expr {$y - $r}] \
                [expr {$x + $r}] [expr {$y + $r}]
        }

        # 次フレームをスケジュール。
        set after_id [after [expr {1000 / $::demobox::fps}] \
                          [list ::demobox::tick $path]]
    }
}

package provide demobox 1.0
