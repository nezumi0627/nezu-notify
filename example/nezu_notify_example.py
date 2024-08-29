import os

from NezuNotify.nezu_notify import NezuNotify

# 環境変数から認証情報を取得
csrf = os.environ.get("LINE_CSRF_TOKEN")
cookie = os.environ.get("LINE_COOKIE")
target_mid = os.environ.get("LINE_TARGET_MID")
existing_token = os.environ.get("LINE_EXISTING_TOKEN")


def token_management_example():
    print("=== トークン管理の例 ===")
    nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_mid)

    # トークンの作成
    new_token = nezu_create.process("create", "新しいトークン")
    print(f"新しいトークン: {new_token}")

    # トークンのステータス確認
    nezu_check = NezuNotify(token=new_token)
    status = nezu_check.process("check", new_token)
    print(f"トークンのステータス: {status}")

    # トークンの無効化
    nezu_revoke = NezuNotify(token=new_token)
    revoke_result = nezu_revoke.process("revoke", new_token)
    print(f"トークン無効化結果: {revoke_result}")

    # グループ一覧の取得
    groups = nezu_create.get_groups()
    print("グループ一覧:")
    for group in groups:
        print(f"名前: {group['name']}, MID: {group['mid']}")


def sending_example():
    print("\n=== 送信の例 ===")

    # テキストメッセージの送信
    nezu_text = NezuNotify(
        token=existing_token,
        message_type="text",
        message_content="これはテストメッセージです。",
    )
    send_result = nezu_text.process("send")
    print(f"テキストメッセージ送信結果: {send_result}")

    # URLを使用した画像の送信
    image_url = "https://example.com/image.jpg"
    nezu_url_image = NezuNotify(
        token=existing_token, message_type="image", message_content=image_url
    )
    send_result = nezu_url_image.process("send")
    print(f"URL画像送信結果: {send_result}")

    # ローカルファイルからの画像送信
    local_image_path = "/path/to/local/image.jpg"
    nezu_local_image = NezuNotify(
        token=existing_token, message_type="image", message_content=local_image_path
    )
    send_result = nezu_local_image.process("send")
    print(f"ローカル画像送信結果: {send_result}")


def main():
    token_management_example()
    sending_example()


if __name__ == "__main__":
    main()
