from .exceptions import *

def iterlist(data_l,stride):
    if stride < 0:
        raise StrideNotPositiveError
    if len(data_l) < stride:
        raise StrideTooBigError
    else:
        for i in range(len(data_l) - stride + 1):
            yield data_l[i:i+stride]
