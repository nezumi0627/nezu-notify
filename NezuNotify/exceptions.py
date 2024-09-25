class NezuNotifyError(Exception):
    """Base exception class for NezuNotify"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"[NezuNotify] {self.message}")


class NezuNotifyValueError(NezuNotifyError):
    """Exception raised when an invalid value is provided"""

    def __init__(self, message: str):
        super().__init__(f"Invalid value: {message}")


class NezuNotifyAuthError(NezuNotifyError):
    """Exception raised when authentication fails"""

    def __init__(self, message: str):
        super().__init__(f"Authentication error: {message}")


class NezuNotifyAPIError(NezuNotifyError):
    """Exception raised when an API call fails"""

    def __init__(self, message: str, status_code: int = None):
        error_message = f"API error: {message}"
        if status_code:
            error_message += f" (Status code: {status_code})"
        super().__init__(error_message)
        self.status_code = status_code


class NezuNotifyRateLimitError(NezuNotifyError):
    """Exception raised when the API rate limit is reached"""

    def __init__(self, limit: int, reset_time: int):
        super().__init__(
            f"Rate limit reached. Limit: {limit}, Reset time: {reset_time}"
        )
        self.limit = limit
        self.reset_time = reset_time


class NezuNotifyNetworkError(NezuNotifyError):
    """Exception raised when a network-related error occurs"""

    def __init__(self, message: str):
        super().__init__(f"Network error: {message}")
