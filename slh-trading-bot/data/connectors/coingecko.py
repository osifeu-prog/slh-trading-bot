from pycoingecko import CoinGeckoAPI

class CoinGeckoConnector:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_btc_data(self):
        data = self.cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days='1')
        return data  # prices, market_caps, total_volumes

    def get_trending(self):
        trending = self.cg.get_search_trending()
        return trending
