class TonAdapter:
    def __init__(self, rpc_url="https://toncenter.com/api/v2/jsonRPC"):
        self.rpc_url = rpc_url

    def place_order(self, symbol, side, size):
        print(f"[TON] {side} {size} of {symbol} (not implemented)")
        return None

    def get_positions(self):
        return []
