import logging
import os
from typing import Dict, Optional

import requests

from .urls import APIUrls


class LineNotify:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def send_message(self, message: str) -> None:
        data = {"message": message}
        self._make_request(APIUrls.NOTIFY_URL, method="POST", data=data)

    def send_image_with_url(self, text: str, url: str) -> None:
        data = {
            "message": text,
            "imageThumbnail": url,
            "imageFullsize": url,
        }
        self._make_request(APIUrls.NOTIFY_URL, method="POST", data=data)

    def send_image_with_local_path(self, text: str, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Image file not found at the specified path: {path}"
            )

        try:
            with open(path, "rb") as image_file:
                files = {"imageFile": image_file}
                data = {"message": text}
                response = requests.post(
                    APIUrls.NOTIFY_URL, headers=self.headers, data=data, files=files
                )
                response.raise_for_status()
        except IOError as e:
            logging.error(f"Failed to read image file: {e}")
            raise
        except requests.RequestException as e:
            logging.error(f"Error occurred while sending image: {e}")
            raise

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
