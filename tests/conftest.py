import pytest


@pytest.fixture
def mocky_trade_socket_data():
    return {
        "e": "trade",
        "E": 1638088187687,
        "s": "PNTUSDT",
        "t": 13903253,
        "p": "1.53560000",
        "q": "195.00000000",
        "b": 184634835,
        "a": 184634902,
        "T": 1638088187686,
        "m": True,
        "M": True,
    }
