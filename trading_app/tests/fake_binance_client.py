from datetime import datetime
from typing import Literal

from trading_app.enums import SideEnum


class FakeClient:
    def __init__(self) -> None:
        self.buy_time = lambda: int(datetime.timestamp(datetime.now()) * 1000)
        self.sell_time = lambda: int(datetime.timestamp(datetime.now()) * 1000)

    def create_order(self, symbol: str, side: Literal["BUY", "SELL"], type: Literal["MARKET"], quantity: float):
        if side == SideEnum.BUY.name:
            return {
                "symbol": "fake_BTCUSDT",
                "orderId": 0,
                "orderListId": -1,
                "clientOrderId": "fake_gfbT4sjFjR8RpKQoEMzovz",
                "transactTime": self.buy_time(),
                "price": "0.00000000",
                "origQty": "0.00100000 ",
                "executedQty": "0.00100000",
                "cummulativeQuoteQty": "58.27886000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "BUY",
                "fills": [
                    {
                        "price": "58278.86000000",
                        "qty": "0.0 0100000",
                        "commission": "0.00000100",
                        "commissionAsset": "BTC",
                        "tradeId": 1167816780,
                    }
                ],
            }
        elif side == SideEnum.SELL.name:
            return {
                "symbol": "fake_BTCUSDT",
                "orderId": 0,
                "orderListId": -1,
                "clientOrderId": "fake_gfbT4sjFjR8RpKQoEMzovz",
                "transactTime": self.sell_time(),
                "price": "0.00000000",
                "origQty": "0.0010000 0",
                "executedQty": "0.00100000",
                "cummulativeQuoteQty": "58.27886000",
                "status": "FILLED",
                "timeInForce": "GTC",
                "type": "MARKET",
                "side": "BUY",
                "fills": [
                    {
                        "price": "58278.86000000",
                        "qty": "0.  00100000",
                        "commission": "0.00000100",
                        "commissionAsset": "BTC",
                        "tradeId": 1167816780,
                    }
                ],
            }
        else:
            raise Exception("No such side")
