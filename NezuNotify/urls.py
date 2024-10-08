class APIUrls:
    BASE_URL = "https://notify-api.line.me"
    UNOFFICIAL_BASE_URL = "https://notify-bot.line.me"
    NOTIFY_URL = f"{BASE_URL}/api/notify"
    GROUP_LIST_URL = f"{UNOFFICIAL_BASE_URL}/api/groupList?page=1"
    PERSONAL_ACCESS_TOKEN_URL = f"{UNOFFICIAL_BASE_URL}/my/personalAccessToken"
    STATUS_URL = f"{BASE_URL}/api/status"
    REVOKE_URL = f"{BASE_URL}/api/revoke"
