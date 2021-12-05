"""

https://www.youtube.com/watch?v=rc_Y6rdBqXM&list=PL9ATnizYJ7f8_opOpLnekEZNsNVUVbCZN&index=2
"""

from typing import Callable, Type, Dict
from typing_extensions import Protocol
import sqlalchemy
import pandas
import secret
from binance.client import Client
import config
import time as tt
import json

"""
Trend following strategy
"""


class Writeable(Protocol):
    def write(self, data):
        ...


class WriteOrder:

    def __init__(self, engine: sqlalchemy.engine.Engine, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name
    
    def write(self, data):
        json_data = json.dumps(data)
        self.engine.execute(f"""
        create table if not exists {self.table_name}(
            id int primary key asc,
            data text);
        """)

        self.engine.execute(f"""
        INSERT INTO {self.table_name} (data)
        VALUES
        ('{json_data}')
        """)


class WriteDf:
    """
    {120: {'symbol': 'BTCUSDT', 'time': Timestamp('2021-11-29 13:46:41.482000'), 'price': 57365.28}}
    """
    def __init__(self, engine: sqlalchemy.engine.Engine, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name
    
    def write(self, data):
        print('--------------------------------------------***')
        print(data)
        dict_data = data.to_dict() # TODO sometimes nested dict sometimes not :( 
        print(dict_data)
        self.engine.execute(f"""
        create table if not exists {self.table_name}(
            id int primary key asc,
            frame_number int,
            symbol TEXT,
            time TIMESTAMP,
            price REAL
            );
        """)
        for frame_number, value in dict_data.items():
            print(f"frame number {frame_number}")
            self.engine.execute(f"""
            INSERT INTO {self.table_name} (frame_number, symbol, time, price)
            VALUES
            (
                {frame_number},
                "{value["symbol"]}",
                "{value["time"]}",
                {value["price"]}
            );
            """)

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
                write_order.write(order)
                open_position = True
                last_row = df.iloc[-1]
                print(f"Last row buy: \n{last_row}")
                write_df_to_sql.write(pandas.DataFrame(last_row))
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
                    order = client.create_order(symbol=currency_symbol, side="SELL", type="MARKET", quantity=qty)
                    print(f"Sell crypto {order}")
                    write_order.write(order)
                    last_row = df.iloc[-1]
                    print(f"Last row sell: \n{last_row}")
                    write_df_to_sql.write(last_row)
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
