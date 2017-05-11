# weirdpad
Python script meant to emulate "[wordpad effect](http://datamoshing.com/tag/wordpad-effect/)" on images.

## Installation
1. Clone this repo
2. `python setup.py develop`
`from WeirdPad import WeirdPad`
`pad = WeirdPad()`
`pad.in_dir = 'in/'`
`pad.out_dir = 'out/'`
`pad.load_pic('pic.jpg')`
`pad.wordpad(200)`
`pad.save(False) # saves image in current state without resetting`
`pad.wordpad_by_color((100,50,25), 20)`
`pad.save()`
