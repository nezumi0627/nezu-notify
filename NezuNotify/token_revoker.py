import logging

import requests


class TokenRevoker:
    def __init__(self, csrf: str, cookie: str):
        self.csrf = csrf
        self.cookie = cookie
        self.headers = {
            "X-CSRF-Token": self.csrf,
            "Cookie": self.cookie,
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def revoke(self, token: str) -> bool:
        url = "https://notify-bot.line.me/api/revoke"
        payload = f"token={token}"

        try:
            response = requests.post(url, headers=self.headers, data=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"トークンの取り消し中にエラーが発生しました: {str(e)}")
            return False
