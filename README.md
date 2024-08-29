# NezuNotify の使い方

English: [README-en.md](README-en.md)

## 概要

NezuNotify は、LINE Notify を簡単に利用するための Python ライブラリです。主な機能は以下の通りです：

- LINE グループへのメッセージ送信
- 画像の送信（URL またはローカルファイル）
- スティッカーの送信
- トークンの生成と管理
- トークンの失効処理
- グループ情報の取得

## インストール

`git clone https://github.com/nezumi0627/NezuNotify.git`

## 使用方法

1. 環境変数の設定

```python
# 環境変数を設定します
import os

# CSRF トークンを設定
os.environ["LINE_CSRF_TOKEN"] = "YOUR_CSRF_TOKEN"

# Cookie を設定
os.environ["LINE_COOKIE"] = "YOUR_COOKIE"

# 対象 MID を設定
os.environ["LINE_TARGET_MID"] = "YOUR_TARGET_MID"

# 既存トークンを設定
os.environ["LINE_EXISTING_TOKEN"] = "YOUR_EXISTING_TOKEN"
```

2. 初期設定

```python
from NezuPuls.nezu_notify import NezuNotify

# 環境変数から認証情報を取得
csrf = os.environ.get("LINE_CSRF_TOKEN")
cookie = os.environ.get("LINE_COOKIE")
target_mid = os.environ.get("LINE_TARGET_MID")
existing_token = os.environ.get("LINE_EXISTING_TOKEN")
```

3. トークン管理

```python
# トークンの作成
nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_mid)
new_token = nezu_create.process("create", "新しいトークン")

# トークンのステータス確認
nezu_check = NezuNotify(token=new_token)
status = nezu_check.process("check", new_token)

# トークンの無効化
nezu_revoke = NezuNotify(token=new_token)
revoke_result = nezu_revoke.process("revoke", new_token)

# グループ一覧の取得
groups = nezu_create.get_groups()
```

4. メッセージの送信

```python
nezu_text = NezuNotify(
    token=existing_token,
    message_type="text",
    message_content="これはテストメッセージです。"
)
send_result = nezu_text.process("send")
```

5. 画像の送信

```python
# URL を使用して画像を送信
image_url = "https://example.com/image.jpg"
nezu_url_image = NezuNotify(
    token=existing_token,
    message_type="image",
    message_content=image_url
)
send_result = nezu_url_image.process("send")

# ローカルファイルから画像を送信
local_image_path = "/path/to/local/image.jpg"
nezu_local_image = NezuNotify(
    token=existing_token,
    message_type="image",
    message_content=local_image_path
)
send_result = nezu_local_image.process("send")
```

6. スタンプの送信

```python
nezu_sticker = NezuNotify(
    token=existing_token,
    message_type="sticker",
    message_content="ステッカー メッセージ!!",
    sticker_id="171",
    sticker_package_id="2"
)
send_result = nezu_sticker.process("send")
```

## 注意事項

- LINE Notify のトークンは安全に管理してください。
- API の利用制限に注意してください。
- 画像送信時は、LINE の仕様に合わせたサイズと形式を使用してください。
- 詳細な使用方法や高度な機能については、公式ドキュメントを参照してください。
