from typing import List, Optional, Union

from .group_manager import GroupManager
from .line_notify import LineNotify
from .token_manager import TokenManager


class NezuNotify:
    def __init__(
        self,
        csrf: Optional[str] = None,
        cookie: Optional[str] = None,
        target_mid: Optional[str] = None,
        token: Optional[str] = None,
        message_type: Optional[str] = None,
        message_content: Optional[str] = None,
        sticker_id: Optional[str] = None,
        sticker_package_id: Optional[str] = None,
    ):
        self.csrf = csrf
        self.cookie = cookie
        self.target_mid = target_mid
        self.token = token
        self.message_type = message_type
        self.message_content = message_content
        self.sticker_id = sticker_id
        self.sticker_package_id = sticker_package_id

        if csrf and cookie:
            self.group_manager = GroupManager(csrf, cookie)
            self.token_manager = TokenManager(csrf, cookie)
        if token:
            self.line_notify = LineNotify(token)

    def process(
        self, action: str, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, List[str], dict]:
        actions = {
            "create": self._create,
            "revoke": self._revoke,
            "check": self._check,
            "send": self._send,
        }
        if action not in actions:
            raise ValueError(
                "無効なアクションです。'create'、'revoke'、'check'、または'send'である必要があります。"
            )
        return actions[action](data)

    def _create(self, data: Optional[str] = None) -> str:
        if not self.csrf or not self.cookie or not self.target_mid:
            raise ValueError("トークン作成にはcsrf、cookie、target_midが必要です。")
        description = data or "NezuNotify"
        return self.token_manager.create_token(self.target_mid, description)

    def _revoke(
        self, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, List[str]]:
        if not data:
            raise ValueError("トークンの取り消しにはトークンが必要です。")
        if isinstance(data, str):
            return self.token_manager.revoke_token(data)
        elif isinstance(data, list):
            self.token_manager.revoke_all_tokens(data)
            return "すべてのトークンが取り消されました。"
        else:
            raise ValueError("データは文字列またはリストである必要があります。")

    def _check(self, data: Optional[Union[str, List[str]]] = None) -> Union[str, dict]:
        if not data:
            raise ValueError("ステータスの確認にはトークンが必要です。")
        return self.token_manager.check_token_status(data)

    def _send(self, data: Optional[str] = None) -> str:
        if not self.token:
            raise ValueError("メッセージの送信にはトークンが必要です。")
        if not self.message_type or not self.message_content:
            raise ValueError(
                "メッセージの送信にはメッセージタイプとコンテンツが必要です。"
            )

        if self.message_type == "text":
            self.line_notify.send_message(self.message_content)
        elif self.message_type == "image_url":
            self.line_notify.send_image_with_url("", self.message_content)
        elif self.message_type == "image_path":
            self.line_notify.send_image_with_local_path("", self.message_content)
        elif self.message_type == "sticker":
            if not self.sticker_id or not self.sticker_package_id:
                raise ValueError(
                    "スティッカーの送信にはsticker_idとsticker_package_idが必要です。"
                )
            self.line_notify.send_sticker(
                self.message_content, self.sticker_id, self.sticker_package_id
            )
        else:
            raise ValueError("無効なメッセージタイプです。")

        return "メッセージが送信されました。"
