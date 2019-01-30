__version__ = "0.1.0"

import click
import ccxt
import os
import sys

from .utils.exceptions import *

from .utils.functions import create_intervals, TIMEFRAMES
from .utils.downloader import make_downloader
from .utils.merge_results import ohlcv_to_pandas, merge_df, col_names
from .utils.iterlist import iterlist
from .utils.post_callbacks import *

KNOWN_EXCHANGES = [
    'bitfinex'
]

EXCHANGE_MAKERS = {
    'bitfinex': lambda: ccxt.bitfinex2({'enableRateLimit': True})
}

OUTPUT_DIR = 'data/'

TIME_FORMAT_STRING = "%FT%H-%M-%S%Z"

@click.command()
@click.option('--exchange', default='bitfinex')
@click.option('-t','--timeframe', default='1m', type=click.Choice(TIMEFRAMES))
@click.option('--symbol',default='XRP/USDT')
# NOTE: it is not clear how to get the correct accepted symbol
@click.option('-s','--start',required=True)
@click.option('-e','--end',default=None)
@click.option('-o','--output',default=OUTPUT_DIR)
@click.option('--save/--no-save',default=True)
@click.option('--echo',is_flag=True,default=False,help="If true prints to stdout")
@click.option('-v','--verbose',is_flag=True,default=False)
def main(exchange,timeframe,symbol,start,end,output,save,echo,verbose):
    if not exchange in KNOWN_EXCHANGES:
        raise UnknownExchangeError

    ex = EXCHANGE_MAKERS[exchange]()
    get_ohlcv = make_downloader(ex)

    # Check that the symbol is understandable
    ex.loadMarkets()
    if not symbol in ex.symbols:
        raise UnknownSymbolError

    partition = create_intervals(start,end,timeframe)

    res = None

    for a,b in iterlist(partition,2):
        part = ohlcv_to_pandas(get_ohlcv(symbol,a,b,timeframe))
        if res is not None:
            res = merge_df(res,part)
            res = res.sort_index()
        else:
            res = part.sort_index()

    res = ensure_unique_index(ensure_sorted(res))

    symbol_id = ex.markets[symbol]['id']
    string_params = {
        'exchange': exchange,
        'symbol': symbol_id,
        'timeframe': timeframe,
        'start_time': partition[0].strftime(TIME_FORMAT_STRING),
        'end_time': partition[-1].strftime(TIME_FORMAT_STRING)
    }
    out_bufs = []
    if save:
        filepath = os.path.join(output,"{exchange}_{symbol}_{timeframe}_{start_time}_{end_time}.csv".format(**string_params))
        out_bufs.append(filepath)
    if echo:
        out_bufs.append(sys.stdout)

    for buf in out_bufs:
        if verbose and buf is not sys.stdout:
            click.echo("Saving to {}".format(buf))
        res[col_names].to_csv(buf)

if __name__ == '__main__':
    main()
