-- 初期化スクリプト
-- 必要に応じて初期データやテーブルを作成

-- 拡張機能の有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- データベースの文字エンコーディング確認
SELECT current_database(), 
       pg_encoding_to_char(encoding) AS encoding
FROM pg_database
WHERE datname = current_database();