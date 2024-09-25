from typing import Dict, List, Optional, Union

from .exceptions import NezuNotifyError, NezuNotifyValueError
from .group_manager import GroupManager
from .line_notify import LineNotify
from .token_manager import TokenManager


class NezuNotify:
    """NezuNotify class simplifies the operations of LINE Notify."""

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
        Initialize a NezuNotify object.

        Args:
            csrf (Optional[str]): CSRF token
            cookie (Optional[str]): Session cookie
            target_mid (Optional[str]): Target MID
            token (Optional[str]): LINE Notify token
            message_type (Optional[str]): Message type
            message_content (Optional[str]): Message content
            sticker_id (Optional[str]): Sticker ID
            sticker_package_id (Optional[str]): Sticker package ID
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
        Execute the specified action.

        Args:
            action (str): The action to perform ('create', 'revoke', 'check',
                'send')
            data (Optional[Union[str, List[str]]]): Data required for the \
                action.

        Returns:
            Union[str, List[str], Dict[str, str]]: The result of the action

        Raises:
            NezuNotifyValueError: If the action is invalid or required data
                is missing
        """
        actions = {
            "create": self._create,
            "revoke": self._revoke,
            "check": self._check,
            "send": self._send,
        }
        if action not in actions:
            raise NezuNotifyValueError(
                "Invalid action. It must be 'create', 'revoke', 'check', or "
                "'send'."
            )
        if action in ["create", "revoke", "check"] and not self.token_manager:
            raise NezuNotifyValueError(
                "CSRF and cookie are required for token management actions."
            )
        return actions[action](data)

    def _create(self, data: Optional[str] = None) -> str:
        """Create a token."""
        if not self.csrf or not self.cookie or not self.target_mid:
            raise NezuNotifyValueError(
                "CSRF, cookie, and target_mid are required to create a token."
            )
        description = data or "NezuNotify"
        return self.token_manager.create_token(self.target_mid, description)

    def _revoke(
        self, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, List[str]]:
        """Revoke a token."""
        if not data:
            raise NezuNotifyValueError("A token is required for revocation.")
        if isinstance(data, str):
            return self.token_manager.revoke_token(data)
        elif isinstance(data, list):
            return self.token_manager.revoke_all_tokens(data)
        else:
            raise NezuNotifyValueError("Data must be a string or a list.")

    def _check(
        self, data: Optional[Union[str, List[str]]] = None
    ) -> Union[str, Dict[str, str]]:
        """Check the status of a token."""
        if not data:
            raise NezuNotifyValueError(
                "A token is required to check the status."
            )
        return self.token_manager.check_token_status(data)

    def _send(self, data: Optional[str] = None) -> str:
        """Send a message."""
        if not self.line_notify:
            raise NezuNotifyValueError(
                "A token is required to send a message."
            )

        try:
            if self.message_type == "text":
                self.line_notify.send_message(self.message_content)
            elif self.message_type == "image":
                if self.message_content.startswith(("http://", "https://")):
                    self.line_notify.send_image_with_url(
                        "Sending image", self.message_content
                    )
                else:
                    self.line_notify.send_image_with_local_path(
                        "Sending image", self.message_content
                    )
            elif self.message_type == "sticker":
                if not self.sticker_id or not self.sticker_package_id:
                    raise NezuNotifyValueError(
                        "sticker_id and sticker_package_id are required to "
                        "send a sticker."
                    )
                self.line_notify.send_sticker(
                    self.message_content,
                    self.sticker_package_id,
                    self.sticker_id,
                )
            else:
                raise NezuNotifyValueError("Invalid message type.")
        except Exception as e:
            raise NezuNotifyError(
                f"Failed to send the message: {str(e)}"
            ) from e

        return "Message has been sent."

    def get_groups(self) -> List[Dict[str, str]]:
        """Retrieve the list of groups."""
        if not self.group_manager:
            raise NezuNotifyValueError(
                "CSRF and cookie are required for group management."
            )
        try:
            return self.group_manager.get_groups()
        except Exception as e:
            raise NezuNotifyError(
                f"Failed to retrieve groups: {str(e)}"
            ) from e
