import logging
from typing import Dict, List

import requests

from .urls import APIUrls


class StatusManager:
    def __init__(self, csrf: str, cookie: str):
        self.status: Dict[str, str] = {}
        self.csrf = csrf
        self.cookie = cookie

    def check_token_statuses(self, tokens: List[str]) -> Dict[str, str]:
        """
        Check the status of multiple tokens.

        Args:
            tokens (List[str]): A list of tokens to check.

        Returns:
            Dict[str, str]: A dictionary mapping each token to its status.
        """
        if not tokens:
            logging.warning("No tokens provided.")
            return {}

        return {token: self._check_single_token_status(token) for token in tokens}

    def _check_single_token_status(self, token: str) -> str:
        """
        Check the status of a single token.

        Args:
            token (str): The token to check.

        Returns:
            str: The status of the token.
        """
        headers = {
            "Authorization": f"Bearer {token}",
            "X-CSRF-TOKEN": self.csrf,
            "Cookie": self.cookie,
        }
        try:
            response = requests.get(APIUrls.STATUS_URL, headers=headers)
            response.raise_for_status()
            return self._determine_status(response)
        except requests.RequestException as error:
            logging.error(
                f"Error occurred while checking status for token {token}: {error}"
            )
            return "Error"

    def _determine_status(self, response: requests.Response) -> str:
        """
        Determine the status based on the API response.

        Args:
            response (requests.Response): The API response.

        Returns:
            str: The determined status.
        """
        if response.status_code == 200:
            return "OK"
        elif response.status_code == 401:
            return "Blocked token"
        else:
            logging.error(f"Unexpected response status code: {response.status_code}")
            return "Waiting"
