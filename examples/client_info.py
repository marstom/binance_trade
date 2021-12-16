from typing import Type

import secret
from binance.client import Client
import config

client = Client(secret.api_key, secret.api_secret)


print(client.get_account())
