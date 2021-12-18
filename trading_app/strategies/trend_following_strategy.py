"""

https://www.youtube.com/watch?v=rc_Y6rdBqXM&list=PL9ATnizYJ7f8_opOpLnekEZNsNVUVbCZN&index=2
"""

import logging
from typing import Callable, NewType, Union

import pandas
from pandas import DataFrame
from typing_extensions import Protocol

from binance.client import Client
from trading_app.db_schemas.writeable import Writeable

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

Order = NewType("Order", dict)


class TradingStrategy(Protocol):
    def run(self):
        ...

    def buy_strategy(self, data_frame: DataFrame) -> Union[Order, None]:
        ...

    def sell_strategy(self, data_frame: DataFrame, order: Order) -> Union[Order, None]:
        ...


"""
Trend following strategy
"""


class Strategy:
    def __init__(
        self,
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
        self.entry = entry
        self.loopback = loopback
        self.qty = qty
        self.currency_symbol = currency_symbol
        self.read_from_sql = read_from_sql
        self.write_order = write_order
        self.write_df_to_sql = write_df_to_sql
        self.open_position = open_position
        self.client = client

    def run(self):
        while 1:
            data_frame = self.read_from_sql()
            buy_order = self.buy_strategy(data_frame)
            if buy_order:
                break
        while 1:
            data_frame = self.read_from_sql()
            sell_order = self.sell_strategy(data_frame, buy_order)
            if sell_order:
                break

    def buy_strategy(self, data_frame: DataFrame) -> Union[Order, None]:
        loopback_period = data_frame.iloc[-self.loopback :]
        cummulative_return = (loopback_period.price.pct_change() + 1).cumprod() - 1
        if not self.open_position:
            if cummulative_return[cummulative_return.last_valid_index()] > self.entry:
                order = self.client.create_order(
                    symbol=self.currency_symbol, side="BUY", type="MARKET", quantity=self.qty
                )
                self.write_order.write(order)
                self.open_position = True
                last_row = data_frame.iloc[-1].copy(deep=True)
                last_row["side"] = "BUY"
                logging.info("--------symobl--------------")
                logging.info(self.currency_symbol)
                logging.info(f"Buy crypto {order}")
                logging.info(f"Last row buy: \n{last_row}")
                self.write_df_to_sql.write(last_row)
                return order
        return None

    def sell_strategy(self, data_frame: DataFrame, order: Order) -> Union[Order, None]:
        # TODO transactTime in fake mode is fixed, therefore it will be false result
        since_buy = data_frame.loc[data_frame.time > pandas.to_datetime(order["transactTime"], unit="ms")]
        if len(since_buy) > 1:
            since_buy_ret = (since_buy.price.pct_change() + 1).cumprod() - 1
            last_entry = since_buy_ret[since_buy_ret.last_valid_index()]
            if last_entry > 0.0015 or last_entry < -0.0015:
                order = self.client.create_order(
                    symbol=self.currency_symbol, side="SELL", type="MARKET", quantity=self.qty
                )
                self.write_order.write(order)
                last_row = data_frame.iloc[-1].copy(deep=True)
                last_row["side"] = "SELL"
                logging.info(f"Sell crypto {order}")
                logging.info(f"Last row sell: \n{last_row}")
                self.write_df_to_sql.write(last_row)
                return order
            return None
