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



def mocky_order():
    return  {'symbol': 'BTCUSDT-mocky', 'orderId': 8441603048, 'orderListId': -1, 'clientOrderId': 'G7713dats1tu9rMaLKgiAV', 'transactTime': 1638181577656, 'price': '0.00000000', 'origQty': '0.00100000', 'executedQty': '0.00100000', 'cummulativeQuoteQty': '57.08876000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'fills': [{'price': '57088.76000000', 'qty': '0.00100000', 'commission': '0.00000100', 'commissionAsset': 'BTC', 'tradeId': 1167287138}]}
