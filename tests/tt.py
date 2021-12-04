import sqlalchemy

# from buy_strategy import strategy
# from .fake_binance_client import FakeClient


# client = FakeClient()
engine = sqlalchemy.create_engine(f"sqlite:///tests/buy_historical_data.sqlite")
engine.execute("select * from BTCUSDT;")
print("finin")
