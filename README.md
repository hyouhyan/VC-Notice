# VC Notice
VC Noticeは指定されたDiscordのVCを監視し、ユーザーの入退室を通知するbotです。


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
![NewApp](./img/スクリーンショット%202023-01-12%2018.43.43.png)
3. 設定したいbotの名前を入力後、チェックを入れて「Create」  
![SetName](./img/スクリーンショット%202023-01-12%2020.03.35.png)
4. Bot欄から「Add Bot」をクリック  
![AddBot](./img/スクリーンショット%202023-01-12%2020.06.44.png)
5. 「Yes, do it!」をクリック  
![YesDoIt](./img/スクリーンショット%202023-01-12%2020.08.38.png)
6. 画面上に表示されるトークンをメモしてください  
![GetToken](./img/スクリーンショット%202023-01-12%2020.11.13.png)


## Pythonのダウンロードとインストール

### Linux(Ubuntu, Debian)の場合
1. ターミナルを起動
2. `$ sudo apt -y install python3.10` を実行
3. `$ python3 -V`を実行してエラーが出なければ成功です

### Windowsの場合

1. [Python公式ページ](https://www.python.org/downloads/)からインストーラをダウンロード  
![DLPython](./img/Install0.png)
2. インストーラーを開く  
![OpenPython](./img/OpenInstaller.png)
3. Install Nowをクリック  
![Install1](./img/Install1.png)
4. 待ちます
![Install2](./img/Install2.png)
5. 終わりです。Closeをクリック  
![Install3](./img/Install3.png)

MacもWindowsと同様でインストーラー開いてポチポチしてればできます。

## VC Noticeのダウンロードと実行
1. [こちら](https://github.com/ogLa-Production/VC-Notice/releases/latest)からzipファイルをダウンロード
2. zipファイルを解凍し、settings.json内の`WriteYourBotToken`に自分のトークンを入れて保存  
![settings.json](img/スクリーンショット%202023-01-12%2020.48.35.png)
3. ターミナルにて`python main.py`を実行するとbotを起動できます

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