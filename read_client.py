"""
Script for readin live data and saving to db
"""
import asyncio
from sys import argv
from typing import Dict

import pandas
import sqlalchemy
from pymongo import MongoClient

from binance import BinanceSocketManager
from binance.client import Client
from binance.exceptions import BinanceAPIException
from trading_app.types_internal import CurrencySymbol

try:
    from trading_app import secret
except ImportError:
    raise ModuleNotFoundError("Please create module secrety.py which contains 2 variables: api_key, api_secret")


class TradeSocketColumns:
    SYMBOL = "s"
    TIMESTAMP = "E"
    PRICE = "p"


def create_frame(msg: Dict):
    df = pandas.DataFrame([msg])
    df = df.loc[:, [TradeSocketColumns.SYMBOL, TradeSocketColumns.TIMESTAMP, TradeSocketColumns.PRICE]]
    df.columns = ["symbol", "time", "price"]
    df.price = df.price.astype(float)
    df.time = pandas.to_datetime(df.time, unit="ms")
    return df


async def main(currency_symbol: CurrencySymbol):
    client = Client(secret.api_key, secret.api_secret)

    bsm = BinanceSocketManager(client)

    socket = bsm.trade_socket(currency_symbol)
    engine = sqlalchemy.create_engine(f"sqlite:///db_sqlite/{currency_symbol}-stream.sqlite")
    # client = MongoClient("mongodb://root:example@localhost:27017/")
    # db = client["live-prices"]

    while True:
        await socket.__aenter__()
        try:
            msg = await socket.recv()
            frame = create_frame(msg)
            # sql
            print(msg)
            # print(frame.to_dict('list'))
            # data_for_db = {"symbol": frame.symbol[0], "time": frame.time[0], "price": frame.price[0]}
            # print(data_for_db)
            # db[currency_symbol].insert_one(data_for_db)
            frame.to_sql(currency_symbol, engine, if_exists="append", index=False)
        except BinanceAPIException as e:
            print(f"Failed to read data from API{e}.")
        except Exception as e:
            print("Other exception occurs", e)
        finally:
            await socket.__aexit__(None, None, None)


if __name__ == "__main__":
    if len(argv) != 2:
        raise Exception("Must be 1 argument: currency symbol <name>")

    _, currency_symbol = argv
    print("----------------Exec main-------------")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(currency_symbol))
