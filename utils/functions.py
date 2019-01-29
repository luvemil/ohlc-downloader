import datetime as dt
from dateutil import parser, tz
from dateutil.tz import tzlocal

from .exceptions import *

TIMEFRAMES = [
    '1m',
    '5m',
    '15m',
    '30m',
    '1h',
    '6h',
    '12h',
    '1d'
]

TF_SECONDS = {
    '1m': 60,
    '5m': 5*60,
    '15m': 15*60,
    '30m': 30*60,
    '1h': 60*60,
    '6h': 6*60*60,
    '12h': 12*60*60,
    '1d': 24*60*60
}

def ensure_tz(dt_time):
    if not dt_time.tzinfo:
        return dt_time.replace(tzinfo=tzlocal())
    else:
        return dt_time

ALLOWED_ROUNDINGS = [
    'CEIL',
    'FLOOR'
]

def round_timeframe(time_dt,timeframe,method='FLOOR'):
    if timeframe not in TIMEFRAMES:
        raise NotAValidTimeZoneError
    ts = int(time_dt.timestamp())
    frame_size = TF_SECONDS[timeframe]
    rem = ts % frame_size
    if method not in ALLOWED_ROUNDINGS:
        raise NotAValidRoundMethodError

    # Round the timestamp to the nearest timeframe
    if method == 'CEIL':
        return time_dt + dt.timedelta(seconds=frame_size - rem)
    elif method == 'FLOOR':
        return time_dt - dt.timedelta(seconds=rem)

LIMIT = 4500

def create_intervals(start_time,end_time=None,timeframe='1m',interval_max_size=LIMIT):
    """
        timeframe: one of '1m','5m','15m','30m', '1h', '6h', '12h', '1d'
        start_time: datetime parsable by dateutil.parser.parse
    """
    start_dt = round_timeframe(ensure_tz(parser.parse(start_time)),timeframe)
    if end_time is None:
        end_dt = dt.datetime.now(tzlocal())
    else:
        end_dt = ensure_tz(parser.parse(end_time))
    end_dt = round_timeframe(end_dt,timeframe,method='CEIL')

    inc = interval_max_size * TF_SECONDS[timeframe]

    q = int((end_dt - start_dt).total_seconds() / inc)

    partition = [ start_dt + dt.timedelta(seconds = x * inc) for x in range(q + 1) ]

    if len(partition) <= 0:
        raise EmptyPartitionError

    # The following logic is just to ensure that everything is fine. In theory we
    # should always be in case 2.
    last_dt = partition[-1]
    if last_dt < end_dt:
        if (end_dt - last_dt).total_seconds() > inc:
            # Case 1: more than inc seconds remaining
            partition += create_intervals("{}".format(last_dt),"{}".format(end_dt),timeframe,interval_max_size)
        else:
            # Case 2: Less than inc seconds remaining
            partition.append(end_dt)
    else:
        # Case 3: end_dt included
        pass

    return partition
