from weirdpad import WeirdPad

pad = WeirdPad()
pad.in_dir = 'in/'
pad.out_dir = 'out/'

pad.load_pic('pic.jpg')
"""
insert glitch everytime we find the color specified
(I was aiming for a blue here), within the tolerance provided,
resetting at each row
target_color = (20, 20, 200)
tolerance = 35
"""
pad.wordpad_rows_by_color((20, 20, 200), 60)
pad.save_pic()
