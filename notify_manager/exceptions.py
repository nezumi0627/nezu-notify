class NotifyException(Exception):
    pass


class AuthorizeException(NotifyException):
    pass


class QRLoginSessionException(AuthorizeException):
    pass


class QRLoginWaitException(AuthorizeException):
    pass


class QRLoginPINWaitException(AuthorizeException):
    pass


class GetGroupListException(NotifyException):
    pass


class IssueTokenException(NotifyException):
    pass
