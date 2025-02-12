# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピー
COPY requirements.txt requirements.txt

# 必要なライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ボットのコードをコピー
COPY . .

# ボットを実行
CMD ["python", "main.py"]
