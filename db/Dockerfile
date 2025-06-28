FROM postgres:16-alpine

# 日本語ロケールの設定
ENV LANG ja_JP.utf8

# タイムゾーンの設定
ENV TZ=Asia/Tokyo

# 初期化スクリプトディレクトリ
COPY ./init.sql /docker-entrypoint-initdb.d/

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD pg_isready -U postgres || exit 1