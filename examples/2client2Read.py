import asyncio

import pandas
import secret
import sqlalchemy

from binance import BinanceSocketManager
from binance.client import Client

client = Client(secret.api_key, secret.api_secret)

bsm = BinanceSocketManager(client)

pair = "PNTUSDT"
socket = bsm.trade_socket(pair)


async def read_sock():
    while 1:
        await socket.__aenter__()
        msg = await socket.recv()
        print("asdf")
        print(msg)  # prices live!


loop = asyncio.get_event_loop()
loop.run_until_complete(read_sock())
