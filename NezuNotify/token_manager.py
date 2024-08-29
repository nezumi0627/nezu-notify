from typing import List, Union

from .status_manager import StatusManager
from .token_creator import TokenCreator
from .token_revoker import TokenRevoker


class TokenManager:
    def __init__(self, csrf: str = None, cookie: str = None):
        if csrf and cookie:
            self.creator = TokenCreator(csrf, cookie)
        self.revoker = TokenRevoker()
        self.status_manager = StatusManager()

    def create_token(self, target_mid: str, description: str) -> str:
        if not hasattr(self, "creator"):
            raise AttributeError(
                "TokenCreator is not initialized. Provide csrf and cookie."
            )
        return self.creator.create_token(target_mid, description)

    def create_multiple_tokens(
        self, target_mid: str, num_tokens: int = 1, custom_string: str = None
    ) -> List[str]:
        if not hasattr(self, "creator"):
            raise AttributeError(
                "TokenCreator is not initialized. Provide csrf and cookie."
            )
        return self.creator.create_multiple_tokens(
            target_mid, num_tokens, custom_string
        )

    def revoke_token(self, token: str) -> str:
        return self.revoker.revoke_token(token)

    def revoke_all_tokens(self, tokens: List[str]) -> None:
        self.revoker.revoke_all_tokens(tokens)

    def check_token_status(self, token: Union[str, List[str]]) -> Union[str, dict]:
        if isinstance(token, str):
            return self.status_manager.check_single_token_status(token)
        if isinstance(token, list):
            return self.status_manager.check_token_statuses(token)
        raise ValueError("Token must be a string or a list of strings")

    def generate_token(self, length: int = 16) -> str:
        return self.creator.generate_token(length)
