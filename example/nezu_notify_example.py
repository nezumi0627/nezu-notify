import json
import logging
import os
from typing import Dict, Optional, Tuple

from dotenv import load_dotenv

from NezuNotify.group_manager import GroupManager
from NezuNotify.nezu_notify import NezuNotify

load_dotenv()

csrf = os.environ.get("LINE_CSRF_TOKEN")
cookie = os.environ.get("LINE_COOKIE")

TOKENS_FILE = "./tokens.json"

logging.basicConfig(level=logging.INFO)


class TokenManager:
    def __init__(self, tokens_file: str = "./tokens.json"):
        self.tokens_file = tokens_file

    def save_token(self, target_mid: str, token_name: str, token: str) -> None:
        tokens = self.load_tokens()
        if target_mid not in tokens:
            tokens[target_mid] = {}
        tokens[target_mid][token_name] = token
        try:
            with open(self.tokens_file, "w") as f:
                json.dump(tokens, f, indent=2)
            logging.info(f"トークンが {self.tokens_file} に保存されました。")
        except IOError as e:
            logging.error(f"トークンの保存中にエラーが発生しました: {e}")

    def load_tokens(self) -> Dict[str, Dict[str, str]]:
        try:
            with open(self.tokens_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"{self.tokens_file} が見つかりません。")
            return {}
        except json.JSONDecodeError:
            logging.error(f"{self.tokens_file} の解析に失敗しました。")
            return {}

    def load_token(self, target_mid: str, token_name: str) -> Optional[str]:
        tokens = self.load_tokens()
        token = tokens.get(target_mid, {}).get(token_name)
        if token is None:
            logging.warning(
                f"トークン '{token_name}' (MID: {target_mid}) が見つかりません"
            )
        return token


def create_new_token(
    token_manager: TokenManager,
) -> Tuple[Optional[str], Optional[str]]:
    logging.info("=== 新しいトークンの作成 ===")
    group_manager = GroupManager(csrf=csrf, cookie=cookie)

    groups = group_manager.get_groups()
    if not groups:
        logging.error(
            "グループが見つかりませんでした。CSRFトークンとCookieを確認してください。"
        )
        return None, None

    logging.info("グループ一覧:")
    for i, group in enumerate(groups, 1):
        logging.info(f"{i}. 名前: {group['name']}, ID: {group['mid']}")

    while True:
        try:
            choice = int(input("使用するグループの番号を入力してください: "))
            if 1 <= choice <= len(groups):
                target_id = groups[choice - 1]["mid"]
                break
            else:
                logging.error(
                    "無効な選択です。リストの番号を入力してください。"
                )
        except ValueError:
            logging.error("数字を入力してください。")

    token_name = input("新しいトークンの名前を入力してください: ")

    nezu_create = NezuNotify(csrf=csrf, cookie=cookie, target_mid=target_id)
    new_token = nezu_create.process("create", "新しいトークン")

    if new_token:
        logging.info(f"新しいトークン: {new_token}")
        token_manager.save_token(target_id, token_name, new_token)
        logging.info(
            f"トークンが {token_manager.tokens_file} に保存されました。"
        )

        nezu_check = NezuNotify(token=new_token, csrf=csrf, cookie=cookie)
        status = nezu_check.process("check", new_token)
        logging.info(f"トークンのステータス: {status}")
        return target_id, token_name
    else:
        logging.error("トークンの作成に失敗しました。")
        return None, None


def use_existing_token(
    token_manager: TokenManager,
) -> Tuple[Optional[str], Optional[str]]:
    logging.info("=== 既存のトークンの使用 ===")
    tokens = token_manager.load_tokens()
    if not tokens:
        logging.error("保存されているトークンがありません。")
        return None, None

    token_list = []
    logging.info("保存されているトークン:")
    for i, (target_id, token_dict) in enumerate(tokens.items(), 1):
        for token_name in token_dict.keys():
            logging.info(
                f"{i}. グループID: {target_id}, トークン名: {token_name}"
            )
            token_list.append((target_id, token_name))

    while True:
        try:
            choice = int(input("使用するトークンの番号を入力してください: "))
            if 1 <= choice <= len(token_list):
                target_id, token_name = token_list[choice - 1]
                return target_id, token_name
            else:
                logging.error(
                    "無効な選択です。リストの番号を入力してください。"
                )
        except ValueError:
            logging.error("数字を入力してください。")


def send_message(token_manager: TokenManager, target_id: str, token_name: str):
    token = token_manager.load_token(target_id, token_name)
    if not token:
        logging.error(f"トークン '{token_name}' が見つかりません。")
        return

    while True:
        print("\n送信するメッセージタイプを選択してください:")
        print("1. テキスト")
        print("2. 画像")
        print("3. ステッカー")
        print("4. メインメニューに戻る")

        try:
            choice = int(input("選択肢の番号を入力してください: "))
            if choice == 1:
                message_content = input("送信するテキストを入力してください: ")
                nezu = NezuNotify(
                    token=token,
                    message_type="text",
                    message_content=message_content,
                )
                send_result = nezu.process("send")
                logging.info(f"テキストメッセージ送信結果: {send_result}")
            elif choice == 2:
                image_content = input(
                    "画像のURLまたはローカルパスを入力してください: "
                )

                nezu = NezuNotify(
                    token=token,
                    message_type="image",
                    message_content=image_content,
                )
                send_result = nezu.process("send")
                logging.info(f"画像メッセージ送信結果: {send_result}")
            elif choice == 3:
                sticker_package_id = input(
                    "ステッカーパッケージIDを入力してください: "
                )
                sticker_id = input("ステッカーIDを入力してください: ")

                nezu = NezuNotify(
                    token=token,
                    message_type="sticker",
                    sticker_package_id=sticker_package_id,
                    sticker_id=sticker_id,
                )
                send_result = nezu.process("send")
                logging.info(f"ステッカー送信結果: {send_result}")
            elif choice == 4:
                break
            else:
                logging.error(
                    "無効な選択です。1、2、3、または4を入力してください。"
                )
        except ValueError:
            logging.error("数字を入力してください。")


def main():
    token_manager = TokenManager()

    while True:
        print("\n操作を選択してください:")
        print("1. 新しいトークンを作成")
        print("2. 既存のトークンを使用")
        print("3. プログラムを終了")

        try:
            choice = int(input("選択肢の番号を入力してください: "))
            if choice == 1:
                target_id, token_name = create_new_token(token_manager)
            elif choice == 2:
                target_id, token_name = use_existing_token(token_manager)
            elif choice == 3:
                logging.info("プログラムを終了します。")
                break
            else:
                logging.error(
                    "無効な選択です。1、2、または3を入力してください。"
                )
                continue

            if target_id and token_name:
                send_message(token_manager, target_id, token_name)
            else:
                logging.error("有効なトークンが選択されませんでした。")
        except ValueError:
            logging.error("数字を入力してください。")


if __name__ == "__main__":
    main()
