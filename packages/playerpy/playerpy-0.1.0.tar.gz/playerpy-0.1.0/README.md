# playerpy - Simple and extendable video player using python

A simple video player with quick key-bindings for play, reverse,
single frame step forward and backwards, goto frame number etc.
Class is easily extendible for other projects, e.g. data annotation
tools.

# How to install
```bash
git clone https://github.com/daniel-falk/playerpy.git
pip install -r playerpy/requirements.txt
pip install playerpy
```

# How to use

## To run from command line:
```bash
playerpy <VIDEO FILE PATH>
```

## To run from a script
```python
from playerpy import play
play(<VIDEO FILE PATH>)  # string or pathlib.Path
```

## Key bindinigs
* SPACE - pause/play
* ENTER - step single frame in paused mode
* g -> [0-9]+ -> ENTER - jump to frame number
* RIGHT ARROW - increase speed
* LEFT ARROW - decrease speed
* r - reverse playback speed
* s - save current frame to disk as JPG


## Example view

Frame number is seen in top of video. Cursor position and pixel intensities are seen in the window footer.
![example view](https://github.com/daniel-falk/playerpy/blob/images/images/playerpy.png "Example view of window: Surveillance view credits to https://viratdata.org/")

# How to subclass

todo

# Todo

- [ ] Add footer showing total number of frames
- [ ] Better readme
- [ ] Upload release to pypi to make "pip installable"
