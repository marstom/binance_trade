from typing import Dict

import pandas
import sqlalchemy

from binance.client import Client
from trading_app.db_schemas.buy_info_db import WriteDf, WriteOrder
from trading_app.strategies.trading_strategy import TradingStrategy
from trading_app.strategies.trend_following_strategy import \
    Strategy as TrendFollowingStrategy
from trading_app.types_internal import CurrencySymbol, StrategyType


class InvalidCurrencySymbol(Exception):
    message = "Invalid currency symbol"


def strategy_factory(
    strategy_type: StrategyType, currency_symbol: str, client: Client, engine: sqlalchemy.engine.Engine
) -> TradingStrategy:
    if strategy_type == "TrendFollowing":
        return TrendFollowingStrategy(**currency_config_factory(currency_symbol, strategy_type, client, engine)).run()


def currency_config_factory(
    currency_symbol: CurrencySymbol, strategy_type: StrategyType, client: Client, engine: sqlalchemy.engine.Engine
) -> Dict:
    if currency_symbol == "BTCUSDT" and strategy_type == "TrendFollowing":
        return {
            "entry": 0.001,
            "loopback": 60,
            "qty": 0.001,
            "currency_symbol": "BTCUSDT",
            "write_order": WriteOrder(engine, "MY_ORDER"),
            "write_df_to_sql": WriteDf(engine, "BUY_SELL"),
            "open_position": False,
            "client": client,
            "read_from_sql": lambda: pandas.read_sql(currency_symbol, engine),
        }
    else:
        raise InvalidCurrencySymbol()
