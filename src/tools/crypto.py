import json
from phi.tools import Toolkit
from phi.utils.log import logger
import ccxt as ccxt

class CoinTracker(Toolkit):
    def __init__(self, 
                 api_key: str, api_secret: str, market='future'
                 ):

        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'options': {
                'defaultType': market,
            },
        })

        exchange.load_markets()
        self.exchange = exchange

        super().__init__(name="coin_tracker")

        self.register(self.get_coin_price)

    def get_coin_price(self, coin: str) -> str:
        """Use this function to get the current price of a cryptocurrency or coin. Send coin as its symbol like BTC for Bitcoin
        
        Args:
            coin (str): The name of the cryptocurrency.
                Eg: "bitcoin" or "ethereum"
        
        Returns:
            str: The current price of the cryptocurrency or error message.
        """
        try:
            ticker = self.exchange.fetch_ticker(f'{coin.upper()}/USDT')
            print(ticker)
            return json.dumps({'indicator': 'price','result':ticker['last']})
        except Exception as e:
            return str(e)
