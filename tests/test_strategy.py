import sqlalchemy
from unittest import mock
from buy_strategy import strategy, WriteOrder, WriteDf
import buy_strategy
from .fake_binance_client import FakeClient

import pandas

"""
42002 rows x 3 columns]
....df         symbol                    time     price
0      BTCUSDT 2021-11-29 13:43:52.611  57474.41
1      BTCUSDT 2021-11-29 13:43:53.904  57486.81
2      BTCUSDT 2021-11-29 13:43:55.247  57486.82
3      BTCUSDT 2021-11-29 13:43:56.596  57482.85
4      BTCUSDT 2021-11-29 13:43:57.928  57465.45
...        ...                     ...       ...

"""


def df_generator():
    engine = sqlalchemy.create_engine(f"sqlite:///tests/data/buy_historical_data.sqlite")
    df = pandas.read_sql("BTCUSDT", engine)
    for i in range(10, df.size):
        yield df.iloc[:i]


def test_df_generator():
    print()
    df_generator()


# TODO strategy not testable
def test_strategy():
    client = FakeClient()
    engine = sqlalchemy.create_engine(f"sqlite:///tests/data/buy_historical_data.sqlite") # read only
    engine_memory = sqlalchemy.create_engine(f"sqlite:///:memory:")
    engine_test_output = sqlalchemy.create_engine(f"sqlite:///tests/_temp.sqlite")
    df_gen = df_generator()
    read_from_sql = lambda: next(df_gen)

    strategy(
        entry=0.001,
        loopback=60,
        qty=0.001,
        currency_symbol="BTCUSDT",
        write_order=WriteOrder(engine_test_output, "MY_ORDER"),
        write_df_to_sql=WriteDf(engine_test_output, "BUY_SELL"),
        open_position=False,
        client=client,
        read_from_sql=read_from_sql,
    )
