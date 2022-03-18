# https://www.youtube.com/watch?v=094y1Z2wpJg

import sys
from os.path import exists
import itertools
import json

import matplotlib.pyplot as plt


def odd(n):
    return n % 2

def range_odd(from_, to_):
    if odd(from_):
        return range(from_, to_, 2)
    else:
        return range(from_ + 1, to_, 2)

def next(y):
    if odd(y):
        return y*3 + 1
    else:
        return y // 2

def sequence(y_init):
    x = 0
    y = y_init

    X = []
    Y = []

    while y > 1:
        X.append(x)
        Y.append(y)
        x = x + 1
        y = next(y)

    X.append(x)
    Y.append(y)

    return X, Y


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
set_y_init          = range_odd(min_y_init, max_y_init)


use_cached_exact    = False
cache               = {}
if exists('.cache.json'):
    with open('.cache.json') as f:
        cache = json.load(f)


print('Loading from cache', end='')
for k, v in cache.items():
    print('.', end='')
    if v['max_y_init'] >= MAX_Y_INIT:
        if v['widest_y_init'] < MAX_Y_INIT and v['tallest_y_init'] < MAX_Y_INIT:
            widest_y_init       = v['widest_y_init']
            tallest_y_init      = v['tallest_y_init']
            use_cached_exact    = True
            break
    else:
        if v['max_x'] > max_x:
            widest_y_init   = v['widest_y_init']
            max_x           = v['max_x']
        if v['max_y'] > max_y:
            tallest_y_init  = v['tallest_y_init']
            max_y           = v['max_y']
        if v['max_y_init'] > min_y_init:
            min_y_init = v['max_y_init']
print()

set_y_init = [widest_y_init, tallest_y_init]
if not use_cached_exact:
    set_y_init  = itertools.chain(set_y_init, range_odd(min_y_init, MAX_Y_INIT))


for y_init in set_y_init:
    print(("Computing %.2f %%" % (100*y_init/MAX_Y_INIT)), end="\r")

    X, Y = sequence(y_init)
    _max_X = X[-1]
    if _max_X >= max_x:
        max_x           = _max_X
        widest_y_init   = y_init
        widest_X        = X
        widest_Y        = Y
    _max_Y = max(Y)
    if _max_Y >= max_y:
        max_y           = _max_Y
        tallest_y_init  = y_init
        tallest_X       = X
        tallest_Y       = Y
print()


cache[str(MAX_Y_INIT)] = {  # prevent duplicate keys, and json only support string keys...
    'max_y_init': MAX_Y_INIT,
    'widest_y_init': widest_y_init,     'max_x': max_x,
    'tallest_y_init': tallest_y_init,   'max_y': max_y,
}
# "Sort" cache dict by 'max_y_init' key of each value; see .cache.sample.json for an idea of the structure
cache = dict(sorted(cache.items(), key=lambda kv: kv[1]['max_y_init']))
with open('.cache.json', 'w') as f:
    json.dump(cache, f, indent=2)


# What we call `y_init`` throughout the code is labeled as `y_0` in the plot. Sorry :)

max_y_widest = max(widest_Y)
max_x_tallest = max(tallest_X)

if max_y_widest / max_y > 0.1:
    yscale = 'linear'
else:
    yscale = 'log'

plt.rcParams['font.family'] = 'monospace'
fig, ax = plt.subplots()
fig.set_tight_layout(True)
ax.set_title(f'"3y+1" problem. Max y_0 = {MAX_Y_INIT}')
ax.set_yscale(yscale)
ax.plot(
    tallest_X, tallest_Y, linewidth=0.85,
    label=f'"Tallest":\ny_0    = {tallest_y_init}\ny_max  = {max_y       }\nx_max  = {max_x_tallest}'
)
ax.plot(
    widest_X,  widest_Y, linewidth=0.85,
    label=f'"Widest": \ny_0    = { widest_y_init}\ny_max  = {max_y_widest}\nx_max  = {max_x        }'
)
ax.set_xlabel('n')
ax.set_ylabel('y_n')
ax.legend()
plt.show()

# Optional: If you have an ATI Radeon: https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-21-10
