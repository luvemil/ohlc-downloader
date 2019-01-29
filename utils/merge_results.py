import pandas as pd

col_names = [
    'mts', # UTC timestamp in milliseconds, integer
    'open', # (O)pen price, float
    'high', # (H)ighest price, float
    'low', # (L)owest price, float
    'close', # (C)losing price, float
    'volume' # (V)olume (in terms of the base currency), float
]

def ohlcv_to_pandas(res_l):
    """
        Put ccxt ohlcv results in a Pandas.DataFrame. See (https://github.com/ccxt/ccxt/wiki/Manual#ohlcv-structure)
    """

    verbatim_df = pd.DataFrame(res_l,columns=col_names)
    verbatim_df['datetime'] = verbatim_df['mts'].apply(pd.to_datetime,unit='ms',utc=True)
    slice_df = verbatim_df.set_index(verbatim_df['datetime'])

    return slice_df.sort_index()

def merge_df(a_df,b_df):
    return pd.concat(a_df,b_df)
