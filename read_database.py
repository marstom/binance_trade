"""
Script for plotting database
"""
import sqlalchemy
import pandas

import matplotlib.pyplot
from sys import argv

if __name__ == "__main__":
    if len(argv) != 2:
        raise Exception("Must be 1 argument: currency symbol <name>")

    _, currency_symbol = argv

    engine = sqlalchemy.create_engine(f"sqlite:///db_sqlite/{currency_symbol}-stream.sqlite")

    df = pandas.read_sql(currency_symbol, engine)
    df.price.plot()
    matplotlib.pyplot.show()
