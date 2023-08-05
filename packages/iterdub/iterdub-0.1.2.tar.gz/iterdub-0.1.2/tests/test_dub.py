#!/usr/bin/env python

'''
`dub` tests for `iterdub` package.
'''

import pytest

from iterdub import iterdub as ib

def test_empty_dub():
    assert ib.dub([]) == 'none'

def test_str_dub():
    assert ib.dub(['foo']) == 'foo'
    assert ib.dub(['foo', 'bar', 'bar']) == 'bar~foo'
    assert ib.dub(['foo', 'barrrrrrrrrrrrrrrrrrrrrrrrr', 'foo']) == '...%2'
    assert ib.dub(['foo', 'bar', 'bizz', 'foo']) == 'bar~...%2'
    assert ib.dub(['foooooooooooooooooo', 'bar', 'bizz', 'bar']) == '...%3'
    assert ib.dub(['foo~', 'bar', 'bizz', 'bar']) == '...%3'

def test_int_dub():
    assert ib.dub([1]) == '1'
    assert ib.dub([20433930, 20433930]) == '20433930'
    assert ib.dub([1, 2]) == '1-2'
    assert ib.dub([1, 3, 2]) == '1-3'
    assert ib.dub([0, 4, 2]) == '0-4%2'
    assert ib.dub([0, 4, 2, 8]) == '0-4%2_8'
    assert ib.dub([0, 4, 2, 8, 10]) == '0-4%2_8-10%2'

def test_float_dub():
    assert ib.dub([0.25]) == '0.25'
    assert ib.dub([0.1, 0.2, 0.2, 0.3]) == '0.1-0.3%0.1'
