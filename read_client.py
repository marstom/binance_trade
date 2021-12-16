"""
Script for readin live data and saving to db
"""
from typing import Dict
import pandas
import asyncio
from sys import argv
import sqlalchemy
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance import BinanceSocketManager

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

    while True:
        await socket.__aenter__()
        try:
            msg = await socket.recv()
            frame = create_frame(msg)
            # sql
            frame.to_sql(currency_symbol, engine, if_exists="append", index=False)
            print(frame)
        except BinanceAPIException as e:
            print(f"Failed to read data from API{e}.")
        except Exception as e:
            print("Other exception occurs")
        finally:
            await socket.__aexit__(None, None, None)


if __name__ == "__main__":
    if len(argv) != 2:
        raise Exception("Must be 1 argument: currency symbol <name>")

    _, currency_symbol = argv
    print("----------------Exec main-------------")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(currency_symbol))
