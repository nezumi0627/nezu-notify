from urllib.parse import urljoin


class LINEAccessURL:
    HOST = "https://access.line.me"
    QR_LOGIN_SESSION = urljoin(HOST, "qrlogin/v1/session")
    QR_LOGIN_WAIT = urljoin(HOST, "qrlogin/v1/qr/wait")
    QR_LOGIN_PIN_WAIT = urljoin(HOST, "qrlogin/v1/pin/wait")
