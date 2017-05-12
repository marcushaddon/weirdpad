# weirdpad
Python class meant to emulate "[wordpad effect](http://datamoshing.com/tag/wordpad-effect/)" on images.

## Installation
1. Clone this repo
2. `pip install requirments.txt`
```python
from WeirdPad import WeirdPad
pad = WeirdPad()
pad.in_dir = 'in/'
pad.out_dir = 'out/'
pad.load_pic('pic.jpg')
pad.wordpad(200)
pad.save(False)
pad.wordpad_by_color((100,50,25), 20)
pad.save()
```

Insert glitch everytime we find find channel value of 100
```python
pad.wordpad(100)
```
![A glitched image](http://pasteboard.co/5xzFvPVyT.jpg)

Insert glitch everytime we find find channel value of 100, checking every 5 spots.
```python
pad.wordpad(100, 5)
```
![A glitched image](http://pasteboard.co/5xALThJlp.jpg)

Insert glitch everytime we find find channel value of 100, resetting at each row (also accepts interval argument).
```python
pad.wordpad_rows(100)
```
[Imgur](http://i.imgur.com/iWfQb4B.jpg)

Insert glitch everytime we find the color specified (I was aiming for a blue here), within the tolerance provided.
target_color = (20, 20, 200)
tolerance = 35
```python
pad.wordpad_by_color((20, 20, 200), 35)
```
![A glitched image](http://pasteboard.co/5xCqEddf9.jpg)


Insert glitch everytime we find the color specified (I was aiming for a blue here), within the tolerance provided, resetting at each row.
target_color = (20, 20, 200)
tolerance = 35
```python
pad.wordpad_rows_by_color((20, 20, 200), 35)
```
![A glitched image](http://pasteboard.co/5xD5DbrQD.jpg)

And again with a higher tolerance, because the effect is less dramatic when reset at each row.
```python
pad.wordpad_rows_by_color((20, 20, 200), 60)
```
![A glitched image](http://pasteboard.co/ymyK5iOO.jpg)

Result of batch processing jpg sequence (using wordpad_by_color, targeting green, in this instance)
tree gif
![A gif of a glitched video](https://media.giphy.com/media/l0IygFSQeFVm9Hgas/giphy.gif)
