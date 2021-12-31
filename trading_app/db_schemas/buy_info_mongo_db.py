"""
Mongo version
"""
import json

from trading_app.types_internal import DatabaseClient


class WriteOrder:
    def __init__(self, engine: DatabaseClient, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name

    def write(self, data):
        # json_data = json.dumps(data)
        # print(json_data)
        # import ipdb;ipdb.set_trace()
        self.engine[self.table_name].insert_one(data)


class WriteDf:
    """
    {'symbol': 'BTCUSDT', 'time': Timestamp('2021-11-29 13:46:41.482000'), 'price': 57365.28}
    """

    def __init__(self, engine: DatabaseClient, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name

    def write(self, data):
        dict_data = data.to_dict()
        self.engine[self.table_name].insert_one(dict_data)
