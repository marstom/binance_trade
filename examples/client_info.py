from typing import Type

import config
import secret

from binance.client import Client

client = Client(secret.api_key, secret.api_secret)


print(client.get_account())
