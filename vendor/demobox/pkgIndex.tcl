# pkgIndex.tcl — Tcl パッケージ demobox の検索インデックス。
#
# Tcl は auto_path に置かれた各ディレクトリの pkgIndex.tcl を読み、
# "package require demobox" に応じてパッケージを提供するファイルを探す。
# ここでは .tm 形式（Tcl モジュール）の demobox-*.tm を登録する。
#
# package ifneeded: 要求されたバージョンに対して、そのパッケージを
# ロードするコマンドを返す。Tcl の標準的な配布機構。
package ifneeded demobox 1.0 [list source [file join $dir demobox-1.0.tm]]
