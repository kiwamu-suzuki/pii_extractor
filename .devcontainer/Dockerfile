# ベースイメージ
FROM python:3.11-slim

# 必要なパッケージをインストール（Rustも含める）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && rm -rf /var/lib/apt/lists/*

# Rustのパスを追加
ENV PATH="/root/.cargo/bin:${PATH}"

# 作業ディレクトリ作成
WORKDIR /app

# Python依存ライブラリをインストール（Spacyモデル含む）
COPY ../requirements.txt .

# --root-user-action=ignore を加えてワーニング抑制
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# ソースコードをコピー
COPY ../src ./src

# 作業ディレクトリへ
WORKDIR /app/src

EXPOSE 8000

# 起動
CMD ["python", "main.py"]
