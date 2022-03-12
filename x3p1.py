# https://www.youtube.com/watch?v=094y1Z2wpJg

import sys
from os.path import exists
import itertools
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
    set_y_init  = itertools.chain(set_y_init, range(min_y_init, MAX_Y_INIT))

for y_init in set_y_init:
    print(("Computing %.1f %%" % (100*y_init/MAX_Y_INIT)), end="\r")

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

        if y >= max_y:
            max_y = y
            is_tallest = True

    if x >= max_x:
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
print()
# print(tallest_X)  # DEBUG
# print(tallest_Y)  # DEBUG

cache[str(MAX_Y_INIT)] = {  # prevent duplicate keys, and json only support string keys...
    'max_y_init': MAX_Y_INIT,
    'widest_y_init': widest_y_init,     'max_x': max_x,
    'tallest_y_init': tallest_y_init,   'max_y': max_y,
}

with open('.cache.json', 'w') as f:
    json.dump(cache, f, indent=2)


plt.title(f'"3y+1" problem: tallest and widest. Max y_init={MAX_Y_INIT}')
plt.plot(tallest_X, tallest_Y, label=f"max_y={max_y} @ y_init={tallest_y_init}")
plt.plot( widest_X,  widest_Y, label=f"max_x={max_x} @ y_init={ widest_y_init}")
plt.legend()
plt.tight_layout(rect=(-0.015, 0, 1, 1))
manager = plt.get_current_fig_manager()
if hasattr(manager, 'window'):
    manager.window.showMaximized()
plt.show()

# Optional: If you have an ATI Radeon: https://www.amd.com/en/support/kb/release-notes/rn-amdgpu-unified-linux-21-10
