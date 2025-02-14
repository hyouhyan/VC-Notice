# VC Notice
VC Noticeは指定されたDiscordのVCを監視し、ユーザーの入退室を通知するbotです。  
[![Image from Gyazo](https://i.gyazo.com/1c9b3a536c4a0888b66ceeac6796ecba.png)](https://gyazo.com/1c9b3a536c4a0888b66ceeac6796ecba)


# セットアップ
VC Noticeを運用するためには以下の手順を踏む必要があります。  

1. Discord Developer PortalでBotを作成
2. Pythonのダウンロードとインストール
3. VC Noticeのダウンロードと実行

ざっとこんな感じです。  
これだけだと随分あいまいなので、細かく説明していきます。


## Discord Developer PortalでBotを作成

1. [Discord Developer Portal](https://discord.com/developers/applications)にアクセス
2. 右上の「New Application」をクリック  
[![Image from Gyazo](https://i.gyazo.com/7ce6d34de12a50bebbb4319db8e3ff5c.png)](https://gyazo.com/7ce6d34de12a50bebbb4319db8e3ff5c)
3. 設定したいbotの名前を入力後、チェックを入れて「Create」  
[![Image from Gyazo](https://i.gyazo.com/96697ad6183da211de986b4cd1161851.png)](https://gyazo.com/96697ad6183da211de986b4cd1161851)
4. Bot欄から「Add Bot」をクリック  
[![Image from Gyazo](https://i.gyazo.com/6265c5a51e406058322af857a9293191.png)](https://gyazo.com/6265c5a51e406058322af857a9293191)
5. 「Yes, do it!」をクリック  
[![Image from Gyazo](https://i.gyazo.com/9f8c7369237b3548a3d62f5baf618b5d.png)](https://gyazo.com/9f8c7369237b3548a3d62f5baf618b5d)
6. 画面上に表示されるトークンをメモしてください  
[![Image from Gyazo](https://i.gyazo.com/8bbacdae3b2173cf4ebbf0ac1f204fce.png)](https://gyazo.com/8bbacdae3b2173cf4ebbf0ac1f204fce)


## Pythonのダウンロードとインストール

### Linux(Ubuntu, Debian)の場合
1. ターミナルを起動
2. `$ sudo apt -y install python3.10` を実行
3. `$ python3 -V`を実行してエラーが出ないことを確認
4. `$ python3 -m pip install discord.py`を実行
5. エラーが発生しなければ成功

### Windowsの場合

1. [Python公式ページ](https://www.python.org/downloads/)からインストーラをダウンロード  
[![Image from Gyazo](https://i.gyazo.com/cb6f68a28cbcf45d5dbef4adcc1f5b1a.png)](https://gyazo.com/cb6f68a28cbcf45d5dbef4adcc1f5b1a)
2. インストーラーを開く  
[![Image from Gyazo](https://i.gyazo.com/beabc719a83b57f4b398de7fe3ec1ddd.png)](https://gyazo.com/beabc719a83b57f4b398de7fe3ec1ddd)
3. Install Nowをクリック  
[![Image from Gyazo](https://i.gyazo.com/6bfd2deaf0eb7034471f408234ba67e8.png)](https://gyazo.com/6bfd2deaf0eb7034471f408234ba67e8)
4. 待ちます  
[![Image from Gyazo](https://i.gyazo.com/124c30c99aee6dadace73c89e10a2b30.png)](https://gyazo.com/124c30c99aee6dadace73c89e10a2b30)
5. Closeをクリック  
[![Image from Gyazo](https://i.gyazo.com/c793924c1c18d2382a09a8b1211afe52.png)](https://gyazo.com/c793924c1c18d2382a09a8b1211afe52)
6. コマンドプロンプトを起動
7. `python3 -V`を実行してエラーが出ないことを確認
8. `python3 -m pip install discord.py`を実行
9. エラーが発生しなければ成功

MacもWindowsと同様でインストーラー開いてポチポチしてればできます。

## VC Noticeのダウンロードと実行
1. [こちら](https://github.com/hyouhyan/VC-Notice/releases/latest)からVC-Notice.zipファイルをダウンロード
2. zipファイルを解凍し、TOKEN.txt内の`WriteYourBotToken`を削除し、自分のトークンを記入して保存  
[![Image from Gyazo](https://i.gyazo.com/d1ba9edbbc3189f17c0ff5d7b54629f0.png)](https://gyazo.com/d1ba9edbbc3189f17c0ff5d7b54629f0)
1. ターミナルにて`python main.py`を実行するとbotを起動できます

Linuxの方は以下のようなserviceファイルを作成し、systemctlで管理することをお勧めします。
```
[Unit]
Description=VC Notice
After=network.target

[Service]
#自分の作業ディレクトリを指定
WorkingDirectory=/home/ogla/vcnotice

#実行ユーザーを指定
User=root
Group=root

Restart=always
RestartSec=10

ExecStart=/usr/bin/screen -DmS disc-vcnotice /usr/bin/python3 main.py

ExecStop=/bin/kill -s INT $MAINPID

[Install]
WantedBy=multi-user.target
```


## Dockerfile
```
docker build -t vc-notice .
docker run -d --restart always --name vc-notice vc-notice
```
