import logging
from typing import Dict, List

import requests

from .urls import APIUrls


class StatusManager:
    def __init__(self):
        self.status = {}

    def check_token_statuses(self, tokens: List[str]) -> Dict[str, str]:
        if not tokens:
            logging.warning("No tokens provided.")
            return {}

        return {token: self._check_single_token_status(token) for token in tokens}

    def _check_single_token_status(self, token: str) -> str:
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(APIUrls.STATUS_URL, headers=headers)
            response.raise_for_status()
            return self._determine_status(response)
        except requests.RequestException as e:
            logging.error(
                f"Error occurred while checking status for token {token}: {e}"
            )
            return "Error"

    def _determine_status(self, response: requests.Response) -> str:
        if response.status_code == 200:
            return "OK"
        elif response.status_code == 401:
            return "Blocked token"
        else:
            logging.error(f"Unexpected response status code: {response.status_code}")
            return "Waiting"
