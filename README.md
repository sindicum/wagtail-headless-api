# Wagtail Headless API

Wagtail CMS ベースのヘッドレス CMS バックエンドシステム

## 概要

このプロジェクトは、Wagtail CMS を使用したヘッドレス CMS のバックエンド API です。フロントエンドアプリケーション（React、Next.js など）にコンテンツを提供するための RESTful API を提供します。

## 主な機能

- 📝 ブログ記事管理（Markdown 対応）
- 🖼️ 画像・メディア管理
- 📄 ドキュメント管理
- 🔖 タグシステム
- 🔐 管理画面（Wagtail Admin）
- 🚀 RESTful API（Wagtail API v2）
- 🐳 Docker 完全対応

## 技術スタック

- **フレームワーク**: Django 4.2 + Wagtail 5.2
- **データベース**: PostgreSQL
- **Web サーバー**: Nginx + Gunicorn
- **コンテナ**: Docker & Docker Compose
- **言語**: Python 3.11

## API エンドポイント

- `/wagtail-api/pages/` - ページ一覧・詳細
- `/wagtail-api/images/` - 画像一覧・詳細
- `/wagtail-api/documents/` - ドキュメント一覧・詳細
- `/wagtail-api/tags/` - タグ一覧
- `/wagtail-admin/` - 管理画面

## クイックスタート

### 前提条件

- Docker & Docker Compose
- Git

### セットアップ

1. リポジトリのクローン

```bash
git clone https://github.com/your-username/WagtailHeadlessAPI.git
cd WagtailHeadlessAPI
```

2. 環境変数の設定

```bash
cp .env.example .env.dev
# .env.devを編集して必要な値を設定
```

3. 開発環境の起動

```bash
docker-compose -f docker-compose-dev.yml up -d
```

4. 初期設定

```bash
# マイグレーション
docker-compose -f docker-compose-dev.yml exec backend python manage.py migrate

# スーパーユーザー作成
docker-compose -f docker-compose-dev.yml exec backend python manage.py createsuperuser

# 静的ファイル収集
docker-compose -f docker-compose-dev.yml exec backend python manage.py collectstatic --noinput
```

5. アクセス

- 管理画面: http://localhost/wagtail-admin/
- API: http://localhost/wagtail-api/pages/

## 開発

### ローカル開発

```bash
# コンテナの起動
docker-compose -f docker-compose-dev.yml up

# ログの確認
docker-compose -f docker-compose-dev.yml logs -f

# コンテナに入る
docker-compose -f docker-compose-dev.yml exec backend bash
```

### コード構成

```
backend/
├── config/          # Django設定
│   ├── settings/    # 環境別設定
│   └── urls.py      # URLルーティング
├── home/            # メインアプリ
│   ├── models.py    # Wagtailページモデル
│   ├── api.py       # API設定
│   └── serializers.py # APIシリアライザー
└── requirements.txt # Python依存関係
```

## 本番環境へのデプロイ

詳細なデプロイ手順は[DEPLOY.md](DEPLOY.md)を参照してください。

### 簡易手順

1. 環境変数の準備

```bash
cp .env.example .env.prod
# .env.prodを本番環境用に編集
```

2. 本番環境の起動

```bash
docker-compose -f docker-compose-prod.yml up -d
```

## API 使用例

### ページ一覧の取得

```bash
curl http://localhost/wagtail-api/pages/
```

### 特定ページの取得

```bash
curl http://localhost/wagtail-api/pages/3/
```

### フィールド指定

```bash
curl "http://localhost/wagtail-api/pages/?fields=title,body,tags"
```
