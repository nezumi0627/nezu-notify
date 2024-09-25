import os
from typing import Dict, Optional

import requests

from .urls import APIUrls


class LineNotify:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def send_message(self, message: str) -> str:
        data = {"message": message}
        return self._make_request(APIUrls.NOTIFY_URL, method="POST", data=data)

    def send_image_with_url(self, text: str, url: str) -> str:
        data = {
            "message": text,
            "imageThumbnail": url,
            "imageFullsize": url,
        }
        return self._make_request(APIUrls.NOTIFY_URL, method="POST", data=data)

    def send_image_with_local_path(self, text: str, path: str) -> str:
        if not os.path.exists(path):
            return f"Image file not found at the specified path: {path}"

        try:
            with open(path, "rb") as image_file:
                files = {"imageFile": image_file}
                data = {"message": text}
                response = requests.post(
                    APIUrls.NOTIFY_URL, headers=self.headers, data=data, files=files
                )
                response.raise_for_status()
                return "Image sent successfully."
        except IOError as e:
            return f"Failed to read image file: {e}"
        except requests.RequestException as e:
            return f"Error occurred while sending image: {e}"

    def send_sticker(
        self, message: str, sticker_id: str, sticker_package_id: str
    ) -> str:
        data = {
            "message": message,
            "stickerId": sticker_id,
            "stickerPackageId": sticker_package_id,
        }
        return self._make_request(APIUrls.NOTIFY_URL, method="POST", data=data)

    def _make_request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict] = None
    ) -> str:
        method = method.upper()
        if method not in {"GET", "POST"}:
            return f"Invalid HTTP method specified: {method}"

        try:
            response = requests.request(
                method, endpoint, headers=self.headers, data=data
            )
            response.raise_for_status()
            return "Request successful."
        except requests.RequestException as e:
            return f"HTTP request error - URL: {endpoint}, Method: {method}, Error: {e}"
