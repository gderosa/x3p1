# https://www.youtube.com/watch?v=094y1Z2wpJg

import sys
from os.path import exists
import json

import matplotlib.pyplot as plt

def odd(n):
    return n % 2

def next(y):
    if odd(y):
        return y*3 + 1
    else:
        return y // 2


MAX_Y_INIT          = int(float(sys.argv[1]))  # Allow  e.g. 1e6

max_x               = 0
max_y               = 0

widest_y_init       = 0
tallest_y_init      = 0

widest_X            = []
widest_Y            = []
tallest_X           = []
tallest_Y           = []

min_y_init          = 1
max_y_init          = MAX_Y_INIT
set_y_init          = range(min_y_init, max_y_init)

use_cached_exact    = False
cache               = {}
if exists('.cache.json'):
    with open('.cache.json') as f:
        cache = json.load(f)

for k, v in cache.items():
    k = int(k)
    # print(repr(v))
    if v['max_y_init'] >= MAX_Y_INIT:
        if v['widest_y_init'] < MAX_Y_INIT and v['tallest_y_init'] < MAX_Y_INIT:
            widest_y_init       = v['widest_y_init']
            tallest_y_init      = v['tallest_y_init']
            use_cached_exact    = True
            break
    else:
        if v['widest_y_init']   >  widest_y_init:
            widest_y_init   = v[  'widest_y_init']
        if v['tallest_y_init']  > tallest_y_init:
            tallest_y_init  = v[ 'tallest_y_init']

if use_cached_exact:
    set_y_init          = sorted([widest_y_init, tallest_y_init])
else:
    set_y_init          = range(min(widest_y_init, tallest_y_init), MAX_Y_INIT)


for y_init in set_y_init:
    print(("%.1f %%" % (100*y_init/MAX_Y_INIT)), end="\r")

    is_widest   = False
    is_tallest  = False

    x = 0
    y = y_init

    X = []
    Y = []

    while y > 1:
        X.append(x)
        Y.append(y)
        x = x + 1
        y = next(y)

        if y >  max_y:
            max_y = y
            is_tallest = True

    if x > max_x:
        max_x = x
        is_widest = True

    X.append(x)
    Y.append(y)

    if is_widest:
        widest_y_init   = y_init
        widest_X        = X
        widest_Y        = Y
    if is_tallest:
        tallest_y_init  = y_init
        tallest_X       = X
        tallest_Y       = Y


cache[MAX_Y_INIT] = {'max_y_init': MAX_Y_INIT, 'widest_y_init': widest_y_init, 'tallest_y_init': tallest_y_init}

with open('.cache.json', 'w') as f:
    json.dump(cache, f)


plt.plot(tallest_X, tallest_Y, label=f"\"Tallest\" y_init={tallest_y_init}")
plt.plot( widest_X,  widest_Y, label=f"\"Widest\" y_init={ widest_y_init}")
plt.legend()
plt.show()
