# デプロイ手順書

## 1. VPS の初期設定

### 1.1 サーバーへの SSH 接続

```bash
ssh root@your-vps-ip
```

### 1.2 システムの更新

```bash
apt update && apt upgrade -y
```

### 1.3 新規ユーザーの作成

```bash
# ユーザー作成
adduser deploy

# sudo権限付与
usermod -aG sudo deploy

# SSH設定をコピー
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

### 1.4 ファイアウォール設定

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## 2. 必要なソフトウェアのインストール

### 2.1 Docker & Docker Compose のインストール

```bash
# Dockerインストール
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Docker Composeインストール
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# deployユーザーをdockerグループに追加
usermod -aG docker deploy
```

### 2.2 Git のインストール

```bash
apt install git -y
```

## 3. アプリケーションのデプロイ

### 3.1 deploy ユーザーに切り替え

```bash
su - deploy
```

### 3.2 プロジェクトのクローン

```bash
cd ~
git clone https://github.com/your-username/WagtailHeadlessAPI.git
cd WagtailHeadlessAPI
```

### 3.3 環境変数ファイルの作成

```bash
# .env.exampleをコピー
cp .env.example .env.prod

# .env.prodを編集
nano .env.prod
```

以下の内容を設定:

```env
# Database
DB_NAME=wagtailheadlessapi
DB_USER=postgres
DB_PASSWORD=your_secure_password_here
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-vps-ip
DJANGO_SETTINGS_MODULE=config.settings.production

# API URLs
WAGTAILAPI_BASE_URL=https://your-domain.com
WAGTAILADMIN_BASE_URL=https://your-domain.com

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### 3.4 Nginx の設定更新

```bash
# Nginx設定を編集
nano nginx/conf.d/default.conf
```

`server_name`を更新:

```nginx
server_name your-domain.com;
```

## 4. アプリケーションの起動

### 4.1 Docker コンテナの起動

```bash
docker-compose -f docker-compose-prod.yml up -d
```

### 4.2 初期設定の実行

```bash
chmod +x production_setup.sh
./production_setup.sh
```

### 4.3 動作確認

```bash
# コンテナの状態確認
docker-compose -f docker-compose-prod.yml ps

# ログ確認
docker-compose -f docker-compose-prod.yml logs -f
```

## 5. SSL 証明書の設定（Let's Encrypt）

### 5.1 Certbot のインストール

```bash
# rootユーザーで実行
sudo apt install certbot python3-certbot-nginx -y
```

### 5.2 一時的に Nginx を停止

```bash
docker-compose -f docker-compose-prod.yml stop nginx
```

### 5.3 証明書の取得

```bash
sudo certbot certonly --standalone -d your-domain.com
```

### 5.4 Nginx 設定の更新

`nginx/conf.d/default.conf`の HTTPS 設定部分のコメントを解除し、証明書パスを更新:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 既存のlocationブロックをここに移動
    ...
}
```

### 5.5 証明書をコンテナにマウント

`docker-compose-prod.yml`の nginx サービスに追加:

```yaml
nginx:
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro
    # 既存のvolumes設定...
```

### 5.6 Nginx を再起動

```bash
docker-compose -f docker-compose-prod.yml up -d nginx
```

## 6. メンテナンス

### 6.1 バックアップ

```bash
# データベースバックアップ
docker-compose -f docker-compose-prod.yml exec db pg_dump -U postgres wagtailheadlessapi > backup_$(date +%Y%m%d).sql

# メディアファイルバックアップ
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

### 6.2 アップデート手順

```bash
# 最新コードを取得
git pull origin main

# コンテナ再ビルド・再起動
docker-compose -f docker-compose-prod.yml down
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d

# マイグレーション実行
docker-compose -f docker-compose-prod.yml exec backend python manage.py migrate

# 静的ファイル収集
docker-compose -f docker-compose-prod.yml exec backend python manage.py collectstatic --noinput
```

### 6.3 ログ確認

```bash
# すべてのログ
docker-compose -f docker-compose-prod.yml logs

# 特定のサービスのログ
docker-compose -f docker-compose-prod.yml logs backend
docker-compose -f docker-compose-prod.yml logs nginx
```

### 6.4 証明書の自動更新設定

```bash
# Cronジョブの設定
sudo crontab -e

# 以下を追加
0 2 * * * certbot renew --pre-hook "docker-compose -f /home/deploy/WagtailHeadlessAPI/docker-compose-prod.yml stop nginx" --post-hook "docker-compose -f /home/deploy/WagtailHeadlessAPI/docker-compose-prod.yml start nginx"
```

## トラブルシューティング

### ポート競合エラー

```bash
# 使用中のポートを確認
sudo lsof -i :80
sudo lsof -i :443
```

### コンテナが起動しない

```bash
# 詳細なログを確認
docker-compose -f docker-compose-prod.yml logs --tail=100
```

### 権限エラー

```bash
# ファイル権限の修正
sudo chown -R deploy:deploy ~/WagtailHeadlessAPI
```
