import logging
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

        self.group_manager = None
        self.token_manager = None
        self.line_notify = None

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
        if action in ["create", "revoke", "check"] and not self.token_manager:
            raise ValueError("トークン管理アクションには csrf と cookie が必要です。")
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
        notify = LineNotify(self.token)

        if self.message_type == "text":
            notify.send_message(self.message_content)
        elif self.message_type == "image":
            if self.message_content.startswith(("http://", "https://")):
                notify.send_image_with_url("画像を送信します", self.message_content)
            else:
                notify.send_image_with_local_path(
                    "画像を送信します", self.message_content
                )
        else:
            raise ValueError("無効なメッセージタイプです。")

        return "メッセージが送信されました。"

    def get_groups(self) -> List[dict]:
        if not hasattr(self, "group_manager"):
            raise ValueError("グループ管理には csrf と cookie が必要です。")
        try:
            return self.group_manager.get_groups()
        except Exception as e:
            logging.error(f"グループの取得に失敗しました: {str(e)}")
            raise
