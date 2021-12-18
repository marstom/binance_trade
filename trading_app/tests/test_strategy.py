import pandas
import sqlalchemy

from trading_app.db_schemas.buy_info_db import WriteDf, WriteOrder
from trading_app.strategies.trend_following_strategy import Strategy

from .fake_binance_client import FakeClient

"""
42002 rows x 3 columns]
df      symbol         time              price
0      BTCUSDT 2021-11-29 13:43:52.611  57474.41
1      BTCUSDT 2021-11-29 13:43:53.904  57486.81
2      BTCUSDT 2021-11-29 13:43:55.247  57486.82
3      BTCUSDT 2021-11-29 13:43:56.596  57482.85
4      BTCUSDT 2021-11-29 13:43:57.928  57465.45
...        ...                     ...       ...

"""


def df_generator():
    engine = sqlalchemy.create_engine(f"sqlite:///trading_app/tests/data/buy_historical_data.sqlite")
    df = pandas.read_sql("BTCUSDT", engine)
    for i in range(10, df.size):
        yield df.iloc[:i]


def test_df_generator():
    df_generator()


def test_strategy():
    client = FakeClient()
    client.buy_time = lambda: 1638213340747
    client.sell_time = lambda: 1638213340747
    engine_test_output = sqlalchemy.create_engine(f"sqlite:///db_sqlite/_temp.sqlite")
    df_gen = df_generator()
    read_from_sql = lambda: next(df_gen)

    strategy = Strategy(
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
    strategy.run()


# TODO detailed tests buy sell
def test_buy_when_above_entry():
    ...


def test_sell_after_period_of_time_when_is_profitable():
    ...
