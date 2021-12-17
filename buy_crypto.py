"""
Main entrypoint for buy/sell crypto
console application

python buy_crypto.py --fake TrendFollowing BTCUSDT
"""
import os
from sys import argv

import sqlalchemy

from binance.client import Client
from trading_app.strategy_factory import strategy_factory
from trading_app.tests.fake_binance_client import FakeClient
from trading_app.types_internal import StrategyType

try:
    from trading_app import secret
except ImportError:
    raise ModuleNotFoundError("Please create module secrety.py which contains 2 variables: api_key, api_secret")


def entrypoint(
    strategy_type: StrategyType,
    currency_symbol: str,
    client: Client,
):
    file_path = f"db_sqlite/{currency_symbol}-stream.sqlite"
    if not os.path.isfile(file_path):
        raise FileNotFoundError("No such database, you must run worker, read_client.py")
    engine = sqlalchemy.create_engine(f"sqlite:///{file_path}")
    strategy_factory(strategy_type, currency_symbol, client, engine)


if __name__ == "__main__":
    if len(argv) != 4:
        raise Exception("Must be 3 arguments (operation --real/--fale) (strategy <name>), currency symbol <name>")
    if argv[1] == "--real":
        client = Client(secret.api_key, secret.api_secret)
    elif argv[1] == "--fake":
        client = FakeClient()
    else:
        raise Exception("Wrong client type, must be: --real or --fake")

    _, _, strategy_name, currency_symbol = argv

    # entrypoint("TrendFollowing", "BTCUSDT", client)
    entrypoint(strategy_name, currency_symbol, client)
