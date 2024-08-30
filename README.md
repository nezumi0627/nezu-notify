# NezuNotify の使い方

English: [README-en.md](README-en.md)

## 概要

NezuNotify は、LINE Notify を簡単に利用するための Python ライブラリです。主な機能は以下の通りです：

- メッセージ送信
- 画像の送信（URL またはローカルファイル）
- ステッカーの送信
- トークンの生成と管理
- トークンの失効処理
- グループ情報の取得

## インストール

`git clone https://github.com/nezumi0627/NezuNotify.git`

## 使用方法

1. プロジェクトのルートディレクトリに`.env`ファイルを作成します。
2. `.env`ファイルに以下の内容を追加し、実際の値を置き換えてください：

```plaintext
LINE_CSRF_TOKEN=""
LINE_COOKIE=""
```

3. トークン管理

```python
# トークンの作成
nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_id)
new_token = nezu_create.process("create", "NezuNotify")

# トークンのステータス確認
nezu_check = NezuNotify(token=token, csrf=csrf, cookie=cookie)
status = nezu_check.process("check", token)

# トークンの無効化
nezu = NezuNotify(token=token, csrf=csrf, cookie=cookie)
revoke_result = nezu.process("revoke")

# グループ一覧の取得
group_manager = GroupManager(csrf=csrf, cookie=cookie)
groups = group_manager.get_groups()

for i, group in enumerate(groups, 1):
    logging.info(f"{i}. 名前: {group['name']}, ID: {group['mid']}, 画像URL: {group['pictureUrl']}")

```

4. メッセージの送信

```python
nezu_text = NezuNotify(
    token=token,
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
    token=token,
    message_type="image",
    message_content=image_url
)
send_result = nezu_url_image.process("send")

# ローカルファイルから画像を送信
local_image_path = "/path/to/local/image.jpg"
nezu_local_image = NezuNotify(
    token=token,
    message_type="image",
    message_content=local_image_path
)
send_result = nezu_local_image.process("send")
```

6. スタンプの送信

```python
nezu_sticker = NezuNotify(
    token=token,
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
