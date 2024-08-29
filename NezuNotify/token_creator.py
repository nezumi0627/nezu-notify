import logging
import secrets
from typing import List, Optional

import requests

from .urls import APIUrls


class TokenCreator:
    def __init__(self, csrf: str, cookie: str):
        self.csrf = csrf
        self.cookie = cookie

    def create_token(self, target_mid: str, description: str) -> str:
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
        }
        try:
            response = requests.post(
                APIUrls.PERSONAL_ACCESS_TOKEN_URL, headers=headers, data=data
            )
            response.raise_for_status()
            token = response.json().get("token", "")
            if not token:
                logging.warning(
                    f"Token generation response does not contain a token: {response.json()}"
                )
            return token
        except requests.RequestException as e:
            logging.error(f"Error occurred while generating LINE Notify token: {e}")
            return ""

    def create_multiple_tokens(
        self, target_mid: str, num_tokens: int = 1, custom_string: Optional[str] = None
    ) -> List[str]:
        num_tokens = min(num_tokens, 100)
        tokens = [
            self.create_token(target_mid, custom_string or "NezuNotify")
            for _ in range(num_tokens)
        ]
        valid_tokens = [token for token in tokens if token]

        if valid_tokens:
            logging.info(f"{len(valid_tokens)} tokens have been generated.")
            return valid_tokens
        else:
            logging.warning("Failed to generate tokens.")
            return []

    def generate_token(self, length: int = 16) -> str:
        return secrets.token_hex(length)
