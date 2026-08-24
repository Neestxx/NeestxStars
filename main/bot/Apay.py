from http.client import responses

import requests, hashlib


class Apay:
    @staticmethod
    def get_link(amount: int, id_order: str) -> str:
        order_id = id_order
        secret = "Apay secret"
        sign = hashlib.md5(f"{order_id}:{amount}:{secret}".encode()).hexdigest()

        params = {
        "client_id": id клиента,
        "order_id": order_id,
        "amount": amount,
        "sign": sign
        }

        response = requests.get("https://apays.io/backend/create_order", params=params)
        return response.json()

    @staticmethod
    def check_payment(id_order: str) -> str:
        order_id = id_order
        secret = "Apay secret"
        sign = hashlib.md5(f"{order_id}:{secret}".encode()).hexdigest()

        params = {
            "client_id": id клиента,
            "order_id": order_id,
            "sign": sign
        }
        response = requests.get("https://apays.io/backend/get_order", params=params)
        return response.json()["order_status"]
