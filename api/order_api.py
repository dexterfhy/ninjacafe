from requests import request
from constants import MENU_CODES_TO_OPTIONS, INTERNAL_ACCESS_TOKEN
from beans.user import User
from utils import default_if_blank


# Calls an API to list orders for a user given his Telegram user id
def list_orders(user: User):
    # !!! Commented out first since API is not done, also returns dummy data
    # return json.loads(__send_request('GET', get_orders_url(user), ()).text)
    return list(map(__parse_order, [
        {
            "items": [
                {
                    "code": "MENU_ITEM_COOKIE",
                    "count": 2
                },
                {
                    "code": "MENU_ITEM_STEAK",
                    "count": 3
                },
                {
                    "code": "MENU_ITEM_BURGER",
                    "count": 1
                }
            ],
            "timestamp": "29th December 2020, 12 PM"
        },
        {
            "items": [
                {
                    "code": "MENU_ITEM_MACARONI",
                    "count": 5
                }
            ],
            "timestamp": "29th December 2020, 6 PM"
        }
    ]))


# Calls an API to create a new order (with one or many menu items) for a user given his Telegram user id
def create_order(user: User, order_items):
    # !!! Commented out first since API is not done
    # return __send_request('POST', get_orders_url(user), order_items)
    return {}


# Parses the response from list orders endpoint into a list of order descriptions and timestamps
def __parse_order(order):
    return {
        "order_description": ", ".join(
            map(lambda item: "{}x {}".format(item['count'], MENU_CODES_TO_OPTIONS[item['code']]),
                filter(lambda item: item['code'] in MENU_CODES_TO_OPTIONS, order['items']))),
        "timestamp": order['timestamp']
    }


def get_orders_url(user: User):
    return "https://api.com/sg/ninjacafe/%s/orders".format(default_if_blank(user.id, ''))


def __send_request(method, url, body):
    headers = {
        "Connection": "keep-alive",
        "Authorization": "Bearer " + INTERNAL_ACCESS_TOKEN
    }

    response = request(method, headers=headers, url=url, data=body)
    return response
