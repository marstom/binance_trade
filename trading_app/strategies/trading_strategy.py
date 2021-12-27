from typing import NewType, Union

from pandas import DataFrame
from typing_extensions import Protocol

Order = NewType("Order", dict)


class TradingStrategy(Protocol):
    def run(self):
        ...

    def buy_strategy(self, data_frame: DataFrame) -> Union[Order, None]:
        ...

    def sell_strategy(self, data_frame: DataFrame, order: Order) -> Union[Order, None]:
        ...
