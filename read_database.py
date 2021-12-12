"""
Script for plotting database
"""
import sqlalchemy
import pandas

import matplotlib.pyplot
import config

engine = sqlalchemy.create_engine(f"sqlite:///db_sqlite/{config.pair}-stream.sqlite")

df = pandas.read_sql(config.pair, engine)
df.price.plot()
matplotlib.pyplot.show()
