import logging
from typing import Dict, List, Optional

import requests

from .urls import APIUrls


class GroupManager:
    def __init__(self, csrf: str, cookie: str):
        self.csrf = csrf
        self.cookie = cookie
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": self.cookie,
        }

    def get_groups(self) -> List[Dict[str, str]]:
        try:
            response = self._make_request(APIUrls.GROUP_LIST_URL, method="GET")
            groups = response.json().get("groups", [])
            return [
                {
                    "mid": group.get("mid", "N/A"),
                    "name": group.get("name", "N/A"),
                    "pictureUrl": group.get("pictureUrl", "N/A"),
                }
                for group in groups
            ]
        except requests.RequestException as e:
            logging.error(f"Error occurred while retrieving group list: {e}")
            return []

    def get_group_by_mid(self, mid: str) -> Optional[Dict[str, str]]:
        groups = self.get_groups()
        for group in groups:
            if group["mid"] == mid:
                return group
        logging.warning(f"Group with MID: {mid} not found.")
        return None

    def _make_request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> requests.Response:
        method = method.upper()
        if method not in {"GET", "POST"}:
            raise ValueError(f"Invalid HTTP method specified: {method}")

        try:
            response = requests.request(
                method, endpoint, headers=self.headers, data=data
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(
                f"HTTP request error - URL: {endpoint}, Method: {method}, Error: {e}"
            )
            raise
