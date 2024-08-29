import logging
from typing import List

import requests

from .urls import APIUrls


class TokenRevoker:
    def revoke_token(self, token: str) -> str:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            response = requests.post(APIUrls.REVOKE_URL, headers=headers)
            response.raise_for_status()
            status = {200: "Revoked successfully", 401: "Token is already revoked"}.get(
                response.status_code, "Unexpected response"
            )
            return f"Token {token}: {status}"
        except requests.RequestException as e:
            logging.error(f"Error occurred while revoking token {token}: {e}")
            return f"Error occurred while revoking token {token}: {e}"

    def revoke_all_tokens(self, tokens: List[str]) -> None:
        if not tokens:
            logging.info("No tokens to revoke.")
            return
        for token in tokens:
            self.revoke_token(token)
        logging.info("All tokens have been revoked.")
