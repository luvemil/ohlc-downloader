# get_ohlc

This software uses `ccxt` to download OHLCV candles in csv format.
It supports only bitfinex for now, but more can be easily added.


## Install

```
git clone git@github.com:luvemil/ohlc-downloader.git
cd ohlc-downloader
python setup.py install
```

## Run

Ensure that the output dir exists
```
mkdir -p data
```

Download with
```
get_ohlc -t 5m -s "2019-01-01 00:00 Z"
```

## Options

```
Required:
  -s, --start: datetime string parsable by dateutil.parser.parse
Optional:
      --echo: if set, prints output to stdout
  -e, --end: datetime string parsable by dateutil.parser.parse, default: now()
      --exchange: 'bitfinex' is the only one supported for now, default: 'bitfinex'
  -o, --output: output directory, default: data/
      --save/--no-save: boolean flag, determines whether to save on disk
      --symbol: symbols as expected by ccxt, e.g. 'BTC/USDT', default: 'XRP/USDT'
  -t, --timeframe: one of ['1m','5m','15m','30m','1h','6h','12h','1d'], default: '1m'
  -v, --verbose: adds some verbosity
```
