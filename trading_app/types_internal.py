from typing import Literal, NewType

StrategyType = Literal["TrendFollowing"]
CurrencySymbol = Literal["BTCUSDT", "DUSKUSDT"]
DatabaseClient = NewType("DatabaseClient", object)
