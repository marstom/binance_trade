import sqlalchemy
import pandas

import matplotlib.pyplot

pair = "PNTUSDT" # pNetwork
engine = sqlalchemy.create_engine(f"sqlite:///{pair}-stream.sqlite")

df = pandas.read_sql(pair, engine)
df.price.plot()
matplotlib.pyplot.show()