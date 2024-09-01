from . import __version__


class NezuNotifyError(Exception):
    """NezuNotify の基本例外クラス"""

    def __init__(self, message: str):
        self.message = message
        self.version = __version__
        super().__init__(f"[NezuNotify v{self.version}] {self.message}")


class NezuNotifyValueError(NezuNotifyError):
    """無効な値が提供された場合に発生する例外"""

    def __init__(self, message: str):
        super().__init__(f"無効な値: {message}")


class NezuNotifyAuthError(NezuNotifyError):
    """認証に失敗した場合に発生する例外"""

    def __init__(self, message: str):
        super().__init__(f"認証エラー: {message}")


class NezuNotifyAPIError(NezuNotifyError):
    """API呼び出しに失敗した場合に発生する例外"""

    def __init__(self, message: str, status_code: int = None):
        error_message = f"APIエラー: {message}"
        if status_code:
            error_message += f" (ステータスコード: {status_code})"
        super().__init__(error_message)
        self.status_code = status_code


class NezuNotifyRateLimitError(NezuNotifyError):
    """APIのレート制限に達した場合に発生する例外"""

    def __init__(self, limit: int, reset_time: int):
        super().__init__(
            f"レート制限に達しました。制限: {limit}, リセット時間: {reset_time}"
        )
        self.limit = limit
        self.reset_time = reset_time


class NezuNotifyNetworkError(NezuNotifyError):
    """ネットワーク関連のエラーが発生した場合の例外"""

    def __init__(self, message: str):
        super().__init__(f"ネットワークエラー: {message}")
