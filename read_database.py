"""
Script for plotting database
"""
from sys import argv

import matplotlib.pyplot
import pandas
import sqlalchemy
from pymongo import MongoClient

from trading_app.secret import mongo_password, mongo_username

if __name__ == "__main__":
    if len(argv) != 2:
        raise Exception("Must be 1 argument: currency symbol <name>")

    _, currency_symbol = argv

    # engine = sqlalchemy.create_engine(f"sqlite:///db_sqlite/{currency_symbol}-stream.sqlite")
    client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/")
    db = client["live-prices"]
    values = db[currency_symbol]
    df = pandas.DataFrame(values.find())

    # df = pandas.read_sql(currency_symbol, engine)
    df.price.plot()
    matplotlib.pyplot.show()
