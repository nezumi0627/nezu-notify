from urllib.parse import urljoin


class NotifyURL:
    HOST = "https://notify-bot.line.me"
    WEB_LOGIN = urljoin(HOST, "login")
    WEB_MYPAGE = urljoin(HOST, "my")
    ISSUE_TOKEN = urljoin(HOST, "my/personalAccessToken")
    API_GROUP_LIST = urljoin(HOST, "api/groupList")
