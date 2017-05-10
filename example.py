from WeirdPad import WeirdPad

pad = WeirdPad()
pad.in_dir = 'in/'
pad.out_dir = 'out/'

pad.load_pic('pic.jpg')
pad.wordpad_rows(200)

pad.save_pic()
