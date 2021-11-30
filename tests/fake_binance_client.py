from typing import Literal

from enums import SideEnum


class FakeClient:
    def create_order(symbol: str, side: SideEnum, type: Literal["MARKET"], quantity: float):
        if side == SideEnum.BUY:
            return {
                "symbol": "BTCUSDT",
                "orderId": 8445965999,
                "orderListId": -1,
                "clientOrderId": "gfbT4sjFjR8RpKQoEMzovz",
                "transactTime": 1638213340747,
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
        elif side == SideEnum.SELL:
            return {
                "symbol": "BTCUSDT",
                "orderId": 8445965999,
                "orderListId": -1,
                "clientOrderId": "gfbT4sjFjR8RpKQoEMzovz",
                "transactTime": 1638213340747,
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
