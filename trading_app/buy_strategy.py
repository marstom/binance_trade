"""

https://www.youtube.com/watch?v=rc_Y6rdBqXM&list=PL9ATnizYJ7f8_opOpLnekEZNsNVUVbCZN&index=2
"""

from typing import Callable
import pandas
from binance.client import Client
import logging
from trading_app.db_schemas.writeable import Writeable

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


"""
Trend following strategy
"""


def strategy(
    entry: float,
    loopback: int,
    qty: float,
    currency_symbol: str,
    read_from_sql: Callable,
    write_order: Writeable,
    write_df_to_sql: Writeable,
    open_position: bool = False,
    client: Client = None,
):
    while 1:
        df = read_from_sql()
        loopback_period = df.iloc[-loopback:]
        cummulative_return = (loopback_period.price.pct_change() + 1).cumprod() - 1
        if not open_position:
            if cummulative_return[cummulative_return.last_valid_index()] > entry:
                order = client.create_order(symbol=currency_symbol, side="BUY", type="MARKET", quantity=qty)
                write_order.write(order)
                open_position = True
                last_row = df.iloc[-1]
                last_row["side"] = "BUY"
                logging.info("--------symobl--------------")
                logging.info(currency_symbol)
                logging.info(f"Buy crypto {order}")
                logging.info(f"Last row buy: \n{last_row}")
                write_df_to_sql.write(last_row)
                break
    if open_position:
        while 1:
            df = read_from_sql()
            since_buy = df.loc[df.time > pandas.to_datetime(order["transactTime"], unit="ms")]
            if len(since_buy) > 1:
                since_buy_ret = (since_buy.price.pct_change() + 1).cumprod() - 1
                last_entry = since_buy_ret[since_buy_ret.last_valid_index()]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    order = client.create_order(symbol=currency_symbol, side="SELL", type="MARKET", quantity=qty)
                    write_order.write(order)
                    last_row = df.iloc[-1]
                    last_row["side"] = "SELL"
                    logging.info(f"Sell crypto {order}")
                    logging.info(f"Last row sell: \n{last_row}")
                    write_df_to_sql.write(last_row)
                    break


