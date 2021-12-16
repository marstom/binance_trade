from .fake_binance_client import FakeClient


def test_fake_client():
    client = FakeClient()
    order = client.create_order(symbol="BCTUSDT", side="BUY", type="MARKET", quantity=0.0001)

    ...
