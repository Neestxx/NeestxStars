import requests
from typing import Any

class Fragment:
    @staticmethod
    def auth(api_key: str, phone_number: str, mnemonics: list) -> str:
        url = "https://api.fragment-api.com/v1/auth/authenticate/"

        payload = {
            "api_key": api_key,
            "phone_number": phone_number,
            "mnemonics": mnemonics
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        return response.json()["token"]

    @staticmethod
    def buy_stars(username: str, quantity: int, tkn: str, show_sender: bool = False) -> str|tuple[str, Any]:
        url = "https://api.fragment-api.com/v1/order/stars/"

        payload = {
            "username": username,
            "quantity": quantity,
            "show_sender": show_sender
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f'JWT {tkn}'
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.json()["success"] is True:
            return True
        return False


