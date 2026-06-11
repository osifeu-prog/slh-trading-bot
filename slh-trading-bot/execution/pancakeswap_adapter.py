import json, os
from web3 import Web3

class PancakeSwapAdapter:
    def __init__(self, rpc_url="https://bsc-dataseed.binance.org"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        abi_path = os.path.join(os.path.dirname(__file__), "..", "data", "pancakeswap_router_abi.json")
        with open(abi_path) as f:
            self.router_abi = json.load(f)
        self.router_address = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
        self.contract = self.w3.eth.contract(address=self.router_address, abi=self.router_abi)

    def place_order(self, symbol, side, size):
        # placeholder for actual swap
        print(f"[PancakeSwap] {side} {size} of {symbol}")
        return None

    def get_positions(self):
        return []  # currently no tracking
