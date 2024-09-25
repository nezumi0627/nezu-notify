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

    def revoke(self, token: str) -> str:
        url = "https://notify-bot.line.me/api/revoke"
        payload = f"token={token}"

        try:
            response = requests.post(url, headers=self.headers, data=payload)
            response.raise_for_status()
            return "Token revoked successfully."
        except requests.exceptions.RequestException as e:
            return f"Error occurred while revoking token: {str(e)}"
