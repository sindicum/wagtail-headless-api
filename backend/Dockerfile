FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# # 必要なシステムパッケージをインストール
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# システムパッケージの更新とNode.jsのインストール
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @anthropic-ai/claude-code \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# 静的ファイルディレクトリとログディレクトリを作成
RUN mkdir -p staticfiles media logs

# ポート8000を公開
EXPOSE 8000

# デフォルトコマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]