from typing import List, Optional

import requests

from .urls import APIUrls


class TokenCreator:
    def __init__(self, csrf: str, cookie: str):
        self.csrf = csrf
        self.cookie = cookie

    def create_token(self, target_mid: str, description: str) -> Optional[str]:
        url = APIUrls.PERSONAL_ACCESS_TOKEN_URL
        data = {
            "action": "issuePersonalAccessToken",
            "description": description,
            "targetType": "GROUP",
            "targetMid": target_mid,
            "_csrf": self.csrf,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": self.cookie,
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.36"
            ),
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json().get("token")
            else:
                return (
                    f"Failed to generate token. Status code: "
                    f"{response.status_code}, Response: {response.text}"
                )
        except requests.RequestException as e:
            return (
                f"Error occurred while generating LINE Notify token: "
                f"{str(e)}"
            )

    def create_multiple_tokens(
        self,
        target_mid: str,
        num_tokens: int = 1,
        custom_string: Optional[str] = None,
    ) -> List[str]:
        num_tokens = min(num_tokens, 100)
        tokens = [
            self.create_token(target_mid, custom_string or "NezuNotify")
            for _ in range(num_tokens)
        ]
        valid_tokens = [
            token
            for token in tokens
            if isinstance(token, str) and token.startswith("token_")
        ]

        if valid_tokens:
            return valid_tokens
        else:
            return ["Failed to generate tokens."]
