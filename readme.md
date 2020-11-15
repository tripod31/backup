backup
=====
linuxの設定ファイルをバックアップするスクリプト
# 設定
## backup.conf
.config/backup.conf.sampleを.config/backup.confにコピーして、変数の値を編集

### dist_dir
tarファイルの出力先ディレクトリを指定する。デフォルトはカレントディレクトリ。

### prefix:
tarファイル名の先頭文字列を指定する。  
例

	prefix=debian

作成されるtarファイル

	debian_YYMMDD.tar.gz

### keyword:
正規表現。実行時に'--update'オプションがあるとき、この正規表現が下記のsearch_dirのディレクトリ下のファイルの１行にマッチすれば、下記のfiles.txtに追加される。

	例
	keyword=^#yoshi
	
### search_dir:
KEYWORDを含むファイルを探すディレクトリをカンマ区切りで指定する。
例

	search_dir=/etc,/home/yoshi

## files.txt
このファイルにバックアップするファイルのパスを書いておく。改行区切り  
例  

	#commment
	/etc/default/grub
	/etc/sysconfig/network


## 引数
### --update/-u:
search_dirで指定したディレクトリを上記keywordで検索し、keywordを含むファイルをfiles.txtに追加する

### --keep_old/-k:
古い日付のtar.gzファイルを消さない
