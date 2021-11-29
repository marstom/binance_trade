

import secret
from binance.client import Client
import config


client = Client(secret.api_key, secret.api_secret)

qty=0.001

order = client.create_order(
        symbol=config.pair,
        side='BUY',
        type='MARKET',
        quantity=qty
)
print(order)