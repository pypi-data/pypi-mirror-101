"""Main module."""

from functools import reduce
import itertools as it
import numpy as np
from math import isnan

# adapted from https://stackoverflow.com/a/45325587
def _float_gcd(a, b, rtol = 1e-05, atol = 1e-08):
    t = min( abs(a), abs(b) )
    while abs(b) > rtol * t + atol:
        a, b = b, a % b
    return a

# adapted from https://stackoverflow.com/a/50830937
def _float_series_gcd( floats ):
    x = reduce( _float_gcd, floats )
    return x

def _is_numeric( val ):
    try:
        float( val )
    except ValueError:
        return False
    return not isnan( float(val) )

# adapted from https://stackoverflow.com/a/43091576
def _to_ranges( floats ):

    floats = sorted(set( floats ))
    assert len(floats)

    by = _float_series_gcd( floats ) or 1

    for key, group in it.groupby(
        enumerate( floats ),
        lambda t: round( t[1] / by - t[0], 8 ),
    ):
        group = list( group )
        yield group[0][1], group[-1][1], by


def _summarize_ranges( floats ):
    fmt = lambda f: np.format_float_positional(
        f,
        trim='-',
        precision=6,
    )
    return '_'.join(
        f'{fmt(begin)}-{fmt(end)}{f"%{fmt(by)}" if by != 1 else ""}'
        if begin != end else
        f'{fmt(begin)}'
        for begin, end, by in _to_ranges(floats )
    )

def dub( values ):
    values = list( values )

    if not values:
        return 'none'
    elif values and all( _is_numeric( value ) for value in values ):
        return _summarize_ranges( float( value ) for value in values )
    elif len(set(values)) == 1:
        value, = set(values)
        return str(value)
    elif not all(
            len(str(value)) <= 32
            and '~' not in str(value)
            for value in values
        ):
        return f'...%{len(set(values))}'
    elif len(set(values)) < 3:
        return '~'.join( str(x) for x in sorted(set(values)) )
    else:
        num_more = len(set(values)) - 1
        assert num_more > 1
        return f'{min(values)}~...%{num_more}'
