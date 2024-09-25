import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get_cookie(url):
        headers = {
            "authority": "notify-bot.line.me",
            "method": "GET",
            "path": "/login",
            "scheme": "https",
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://notify-bot.line.me/ja/",
            "sec-ch-ua": (
                '"Google Chrome";v="129", "Not=A?Brand";v="8", '
                '"Chromium";v="129"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            ),
        }
        response = requests.get(url, headers=headers)
        return response.cookies.get_dict()

    @staticmethod
    def create_xrsf():
        return Login.get_cookie("https://notify-bot.line.me/ja/")["XSRF-TOKEN"]

    @staticmethod
    def create_session(xrsf: str):
        headers = {
            "authority": "notify-bot.line.me",
            "method": "GET",
            "path": "/login",
            "scheme": "https",
            "accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": (
                "no-cache, no-store, max-age=0, must-revalidate"
            ),
            "content-language": "ja",
            "content-length": "0",
            "dnt": "1",
            "cookie": f"XSRF-TOKEN={xrsf}",
            "date": "Wed, 25 Sep 2024 03:56:15 GMT",
            "expires": "0",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://notify-bot.line.me/ja/",
            "sec-ch-ua": (
                '"Google Chrome";v="129", "Not=A?Brand";v="8", '
                '"Chromium";v="129"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/129.0.0.0 Safari/537.36"
            ),
        }
        try:
            response = requests.get(
                "https://notify-bot.line.me/login", headers=headers
            )
            return response.headers.get("Location")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None

    def login(self):
        xrsf = Login.create_xrsf()
        login_selenium = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        login_selenium.delete_all_cookies()
        login_selenium.get("https://notify-bot.line.me/login")
        time.sleep(3)
        login_selenium.add_cookie(
            {
                "name": "XSRF-TOKEN",
                "value": xrsf,
                "url": "https://notify-bot.line.me/",
                "domain": ".line.me",
            }
        )
        login_selenium.find_element(By.NAME, "tid").send_keys(self.username)
        login_selenium.find_element(By.NAME, "tpasswd").send_keys(
            self.password
        )
        login_button = login_selenium.find_element(By.CLASS_NAME, "MdBtn01")
        if not login_button.get_attribute("disabled"):
            login_button.click()
        else:
            print("mailとpassが未指定")
            return None
        time.sleep(3)
        try:
            verification_code = login_selenium.find_element(
                By.CLASS_NAME, "mdMN06Number"
            ).text
            print(f"Enter Pincode: {verification_code}")
        except Exception:
            print("認証コードの要素が見つかりません。")
            return None
        try:
            WebDriverWait(login_selenium, 10).until(
                EC.url_changes(login_selenium.current_url)
            )
        except TimeoutException:
            print("URLの変更に失敗しました。")
            return None
        login_selenium.get("https://notify-bot.line.me/my/")
        final_cookies = login_selenium.get_cookies()
        cookie_string = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in final_cookies]
        )
        return [xrsf, cookie_string]
