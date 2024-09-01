from typing import Dict, List, Optional, Union

from .exceptions import NezuNotifyError, NezuNotifyValueError
from .group_manager import GroupManager
from .line_notify import LineNotify
from .token_manager import TokenManager


class NezuNotify:
    """NezuNotify クラスは、LINE Notify の操作を簡略化します。"""

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
        """
        NezuNotify オブジェクトを初期化します。

        Args:
            csrf (Optional[str]): CSRF トークン
            cookie (Optional[str]): セッションクッキー
            target_mid (Optional[str]): ターゲットの MID
            token (Optional[str]): LINE Notify トークン
            message_type (Optional[str]): メッセージタイプ
            message_content (Optional[str]): メッセージ内容
            sticker_id (Optional[str]): スタッカーID
            sticker_package_id (Optional[str]): スタッカーパッケージID
        """
        self.csrf = csrf
        self.cookie = cookie
        self.target_mid = target_mid
        self.token = token
        self.message_type = message_type
        self.message_content = message_content
        self.sticker_id = sticker_id
        self.sticker_package_id = sticker_package_id

        self.group_manager: Optional[GroupManager] = None
        self.token_manager: Optional[TokenManager] = None
        self.line_notify: Optional[LineNotify] = None

        if csrf and cookie:
            self.group_manager = GroupManager(csrf, cookie)
            self.token_manager = TokenManager(csrf, cookie)
        if token:
            self.line_notify = LineNotify(token)

    def process(
        self, action: str, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, List[str], Dict[str, str]]:
        """
        指定されたアクションを実行します。

        Args:
            action (str): 実行するアクション ('create', 'revoke', 'check', 'send')
            data (Optional[Union[str, List[str]]]): アクションに必要なデータ

        Returns:
            Union[str, List[str], Dict[str, str]]: アクションの結果

        Raises:
            NezuNotifyValueError: 無効なアクションや不足しているデータがある場合
        """
        actions = {
            "create": self._create,
            "revoke": self._revoke,
            "check": self._check,
            "send": self._send,
        }
        if action not in actions:
            raise NezuNotifyValueError(
                "無効なアクションです。'create'、'revoke'、'check'、または'send'である必要があります。"
            )
        if action in ["create", "revoke", "check"] and not self.token_manager:
            raise NezuNotifyValueError(
                "トークン管理アクションには csrf と cookie が必要です。"
            )
        return actions[action](data)

    def _create(self, data: Optional[str] = None) -> str:
        """トークンを作成します。"""
        if not self.csrf or not self.cookie or not self.target_mid:
            raise NezuNotifyValueError(
                "トークン作成にはcsrf、cookie、target_midが必要です。"
            )
        description = data or "NezuNotify"
        return self.token_manager.create_token(self.target_mid, description)

    def _revoke(
        self, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, List[str]]:
        """トークンを取り消します。"""
        if not data:
            raise NezuNotifyValueError("トークンの取り消しにはトークンが必要です。")
        if isinstance(data, str):
            return self.token_manager.revoke_token(data)
        elif isinstance(data, list):
            return self.token_manager.revoke_all_tokens(data)
        else:
            raise NezuNotifyValueError(
                "データは文字列またはリストである必要があります。"
            )

    def _check(
        self, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, Dict[str, str]]:
        """トークンのステータスを確認します。"""
        if not data:
            raise NezuNotifyValueError("ステータスの確認にはトークンが必要です。")
        return self.token_manager.check_token_status(data)

    def _send(self, data: Optional[str] = None) -> str:
        """メッセージを送信します。"""
        if not self.line_notify:
            raise NezuNotifyValueError("メッセージの送信にはトークンが必要です。")

        try:
            if self.message_type == "text":
                self.line_notify.send_message(self.message_content)
            elif self.message_type == "image":
                if self.message_content.startswith(("http://", "https://")):
                    self.line_notify.send_image_with_url(
                        "画像を送信します", self.message_content
                    )
                else:
                    self.line_notify.send_image_with_local_path(
                        "画像を送信します", self.message_content
                    )
            elif self.message_type == "sticker":
                if not self.sticker_id or not self.sticker_package_id:
                    raise NezuNotifyValueError(
                        "ステッカー送信にはsticker_idとsticker_package_idが必要です。"
                    )
                self.line_notify.send_sticker(
                    self.message_content, self.sticker_package_id, self.sticker_id
                )
            else:
                raise NezuNotifyValueError("無効なメッセージタイプです。")
        except Exception as e:
            raise NezuNotifyError(f"メッセージの送信に失敗しました: {str(e)}") from e

        return "メッセージが送信されました。"

    def get_groups(self) -> List[Dict[str, str]]:
        """グループのリストを取得します。"""
        if not self.group_manager:
            raise NezuNotifyValueError("グループ管理には csrf と cookie が必要です。")
        try:
            return self.group_manager.get_groups()
        except Exception as e:
            raise NezuNotifyError(f"グループの取得に失敗しました: {str(e)}") from e
