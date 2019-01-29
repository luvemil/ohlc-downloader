import click
import ccxt
import os

from utils.exceptions import *

from utils.functions import create_intervals, TIMEFRAMES
from utils.downloader import make_downloader
from utils.merge_results import ohlcv_to_pandas, merge_df, col_names
from utils.iterlist import iterlist

KNOWN_EXCHANGES = [
    'bitfinex'
]

EXCHANGE_MAKERS = {
    'bitfinex': lambda: ccxt.bitfinex2({'enableRateLimit': True})
}

OUTPUT_DIR = 'data/'


@click.command()
@click.option('-e','--exchange', default='bitfinex')
@click.option('-t','--timeframe', default='1m', type=click.Choice(TIMEFRAMES))
@click.option('--symbol',default='XRP/USDT')
# NOTE: it is not clear how to get the correct accepted symbol
@click.option('-s','--start',required=True)
@click.option('-e','--end',default=None)
@click.option('-o','--output',default=OUTPUT_DIR)
def download(exchange,timeframe,symbol,start,end,output):
    if not exchange in KNOWN_EXCHANGES:
        raise

    ex = EXCHANGE_MAKERS[exchange]()
    get_ohlcv = make_downloader(ex)

    partition = create_intervals(start,end,timeframe)

    res = None

    for a,b in iterlist(partition,2):
        part = ohlcv_to_pandas(get_ohlcv(symbol,a,b,timeframe))
        if res is not None:
            res = merge_df(res,part)
            res = res.sort_index()
        else:
            res = part.sort_index()

    # TODO: fix "symbol" in next line
    res[col_names].to_csv(os.path.join(output,"{}_{}_{}.csv".format(exchange,"symbol",timeframe)))
if __name__ == '__main__':
    download()
