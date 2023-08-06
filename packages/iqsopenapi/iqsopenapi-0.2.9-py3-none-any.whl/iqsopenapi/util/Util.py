# -*- coding: utf-8 -*-
import time
import sys
import os
import json
import datetime

def ExecutedTime(func):
    start = time.time()
    result = func()
    end = time.time()
    escape = end - start
    return escape, result

def Minimum(values, func):
    value = None
    last = None
    for x in values:
        result = func(x)
        if not last or last > result:
            value = x
            last = result
    return value

def get_change_percentage(actual, prev):
    if actual is None or prev is None or prev == 0:
        raise Exception("Invalid values")

    diff = actual-prev
    ret = diff / float(abs(prev))
    return ret


def safe_min(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return min(left, right)


def safe_max(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return max(left, right)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)