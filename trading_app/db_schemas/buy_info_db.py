import json

import sqlalchemy


class WriteOrder:
    def __init__(self, engine: sqlalchemy.engine.Engine, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name

    def write(self, data):
        json_data = json.dumps(data)
        self.engine.execute(
            f"""
        create table if not exists {self.table_name}(
            id int primary key asc,
            data text);
        """
        )

        self.engine.execute(
            f"""
        INSERT INTO {self.table_name} (data)
        VALUES
        ('{json_data}')
        """
        )


class WriteDf:
    """
    {'symbol': 'BTCUSDT', 'time': Timestamp('2021-11-29 13:46:41.482000'), 'price': 57365.28}
    """

    def __init__(self, engine: sqlalchemy.engine.Engine, table_name: str) -> None:
        self.engine = engine
        self.table_name = table_name

    def write(self, data):
        dict_data = data.to_dict()
        self.engine.execute(
            f"""
        create table if not exists {self.table_name}(
            id integer primary key autoincrement,
            side TEXT,
            symbol TEXT,
            time TIMESTAMP,
            price REAL
            );
        """
        )

        self.engine.execute(
            f"""
        INSERT INTO {self.table_name} (side, symbol, time, price)
        VALUES
        (
            "{dict_data["side"]}",
            "{dict_data["symbol"]}",
            "{dict_data["time"]}",
            {dict_data["price"]}
        );
        """
        )
