# x3p1

See https://www.youtube.com/watch?v=094y1Z2wpJg.

This is about sequences having just these rules:
* if value `y` is even, then divide it by 2
* if it's odd, then turn it into `3*y + 1
* extra rule: if y is equal to 1, interrupt the sequence (it would otherwise get into a 4-2-1 endless loop),

and keeping track of the "tallest" and "widest" sequence obtained so far (progressively increasing the initial value).

Plot images of such sequences go into `plots/*/`. For example:

![000000156159](https://user-images.githubusercontent.com/55979/159082829-8136668d-bf05-4b0d-87b5-ab5a302413c1.svg)


## Requirements

* A recent Python 3.
* [Matplotlib](https://matplotlib.org/).

## Usage

```
python x3p1.py
```

### Stopping and resuming (caching)

You can stop execution with CTRL+C. You can resume later, and computation will start from where you left. If you want to start everything over, delete the file `.cache.json`.

## A video was made out of plot pictures

See https://www.youtube.com/watch?v=TzE3z4Burdk.

Video was made with
```
ffmpeg -framerate 2 -pattern_type glob -i 'plots/jpg/*.jpg' out.mp4
```
