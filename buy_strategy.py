"""

https://www.youtube.com/watch?v=rc_Y6rdBqXM&list=PL9ATnizYJ7f8_opOpLnekEZNsNVUVbCZN&index=2
"""

from typing import Callable, Type
import sqlalchemy
import pandas
import secret
from binance.client import Client
import config
import time as tt


"""
Trend following strategy
"""


def strategy(
    entry: float,
    loopback: int,
    qty: float,
    currency_symbol: str,
    read_from_sql: Callable,
    open_position: bool = False,
    client: Client = None,
):
    while 1:
        # tt.sleep(1)
        # df = pandas.read_sql(currency_symbol, sql_engine)
        df = read_from_sql()
        # print(f"....df {df}")
        loopback_period = df.iloc[-loopback:]
        cummulative_return = (loopback_period.price.pct_change() + 1).cumprod() - 1
        if not open_position:
            if cummulative_return[cummulative_return.last_valid_index()] > entry:
                print("--------symobl--------------")
                print(currency_symbol)
                order = client.create_order(symbol=currency_symbol, side="BUY", type="MARKET", quantity=qty)
                print(f"Buy crypto {order}")
                open_position = True
                last_row = df.iloc[-1]
                print(f"Last row buy: \n{last_row}")
                break
    if open_position:
        while 1:
            # tt.sleep(1)
            # print(f"....SELL DF {df}")
            df = read_from_sql()
            since_buy = df.loc[df.time > pandas.to_datetime(order["transactTime"], unit="ms")]
            if len(since_buy) > 1:
                since_buy_ret = (since_buy.price.pct_change() + 1).cumprod() - 1
                last_entry = since_buy_ret[since_buy_ret.last_valid_index()]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    client.create_order(symbol=currency_symbol, side="SELL", type="MARKET", quantity=qty)
                    print(f"Sell crypto {order}")
                    last_row = df.iloc[-1]
                    print(f"Last row sell: \n{last_row}")
                    break


if __name__ == "__main__":
    engine = sqlalchemy.create_engine(f"sqlite:///{config.pair}-stream.sqlite")
    client = Client(secret.api_key, secret.api_secret)
    strategy(
        entry=0.001,
        loopback=60,
        qty=0.001,
        currency_symbol=config.pair,
        open_position=False,
        sql_engine=engine,
        client=client,
    )
