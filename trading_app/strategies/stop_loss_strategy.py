"""
https://www.youtube.com/watch?v=V6z1ME3-0_I&list=PL9ATnizYJ7f8_opOpLnekEZNsNVUVbCZN&index=3
"""

from typing import NewType, Union

from pandas import DataFrame

from trading_app.strategies.trading_strategy import Order


class Strategy:
    def run(self):
        ...

    def buy_strategy(self, data_frame: DataFrame) -> Union[Order, None]:
        ...

    def sell_strategy(self, data_frame: DataFrame, order: Order) -> Union[Order, None]:
        ...
