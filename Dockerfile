# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 日本語対応
RUN apt-get update
RUN apt-get -y install locales-all

ENV LANG=ja_JP.UTF-8
ENV TZ=Asia/Tokyo

# 依存関係をコピー
COPY requirements.txt requirements.txt

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ボットのコードをコピー
COPY . .

# ボットを実行
CMD ["python", "main.py"]
