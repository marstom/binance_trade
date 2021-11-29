import pandas

import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager

import secret
import asyncio

client = Client(secret.api_key, secret.api_secret)

bsm = BinanceSocketManager(client)

pair = "PNTUSDT"
socket = bsm.trade_socket(pair)


async def read_sock():
    while 1:
        await socket.__aenter__()
        msg = await socket.recv()
        print("asdf")
        print(msg) # prices live!


loop = asyncio.get_event_loop()
loop.run_until_complete(read_sock())

