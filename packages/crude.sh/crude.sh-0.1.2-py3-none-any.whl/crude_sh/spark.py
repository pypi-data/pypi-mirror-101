#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adapted from
    https://gist.githubusercontent.com/rogerallen/1368454/raw/b17e96b56ae881621a9f3b1508ca2e7fde3ec93e/spark.py
"""

BARS = u'▁▂▃▅▆▇'

import sys

def sparkline(data):
    data = [float(x) for x in data if x]
    incr = min(data)
    width = (max(data) - min(data)) / (len(BARS) - 1)
    bins = [i*width+incr for i in range(len(BARS))]
    indexes = [i for n in data
            for i, thres in enumerate(bins)
            if thres <= n < thres+width]
    return ''.join(BARS[i] for i in indexes)
