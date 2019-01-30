from .exceptions import *


def to_mts(time_dt):
    return int(time_dt.timestamp()*1000)

class Downloader:
    def __init__(self,exchange):
        """
            exchange: ccxt.Exchange
        """
        if not exchange.has['fetchOHLCV']:
            raise NotCompatibleExchange
        self.ex = exchange


    def get_ohlcv(self,symbol,start_dt,end_dt,timeframe='1m'):
        # TODO: add a check for symbol
        start_ts = to_mts(start_dt)
        end_ts = to_mts(end_dt)
        res = self.ex.fetch_ohlcv(
            symbol=symbol,
            since=start_ts,
            timeframe=timeframe,
            limit=5000,
            params={
                'sort':-1,
                'end': end_ts
            }
        )

        return res

def make_downloader(exchange):
    """
    Return a single function to download ohlcv candles with signature:
    (symbol, start_dt, end_dt, timeframe)
    """
    d = Downloader(exchange)
    return d.get_ohlcv
