import logging

from .status_manager import StatusManager
from .token_creator import TokenCreator
from .token_revoker import TokenRevoker


class TokenManager:
    def __init__(self, csrf: str, cookie: str):
        self.csrf = csrf
        self.cookie = cookie
        logging.info(f"CSRF Token: {self.csrf}")
        logging.info(f"Cookie: {self.cookie}")
        self.token_creator = TokenCreator(csrf, cookie)
        self.token_revoker = TokenRevoker(csrf, cookie)
        self.status_manager = StatusManager(csrf, cookie)

    def create_token(self, target_mid: str, description: str) -> str:
        return self.token_creator.create_token(target_mid, description)

    def revoke_token(self, token: str) -> str:
        return self.token_revoker.revoke(token)

    def revoke_all_tokens(self, tokens: list[str]) -> str:
        results = [self.revoke_token(token) for token in tokens]
        return (
            "All tokens have been revoked."
            if all(results)
            else "Failed to revoke some tokens."
        )

    def check_token_status(self, token: str) -> dict:
        return self.status_manager._check_single_token_status(token)
