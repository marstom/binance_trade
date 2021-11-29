from typing import Dict
import pandas

import sqlalchemy
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance import BinanceSocketManager

import secret
import asyncio
import config


class TradeSocketColumns:
    SYMBOL = 's'
    TIMESTAMP = 'E'
    PRICE = 'p'

def create_frame(msg: Dict):
    df = pandas.DataFrame([msg])
    df = df.loc[:,[TradeSocketColumns.SYMBOL, TradeSocketColumns.TIMESTAMP, TradeSocketColumns.PRICE]]
    df.columns =['symbol', 'time', 'price']
    df.price = df.price.astype(float)
    df.time = pandas.to_datetime(df.time, unit='ms')
    return df


async def main():
    client = Client(secret.api_key, secret.api_secret)

    bsm = BinanceSocketManager(client)

    socket = bsm.trade_socket(config.pair)
    engine = sqlalchemy.create_engine(f"sqlite:///{config.pair}-stream.sqlite")

    while True:
        await socket.__aenter__()
        try:
            msg = await socket.recv()
            frame = create_frame(msg)
            #sql
            frame.to_sql(config.pair, engine, if_exists='append', index=False)
            print(frame)
        except BinanceAPIException as e:
            print(f"Failed to read data from API{e}.")
        except Exception as e:
            print("Other exception occurs")
        finally:
            await socket.__aexit__(None, None, None)

if __name__ == "__main__":
    print("----------------Exec main-------------")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




