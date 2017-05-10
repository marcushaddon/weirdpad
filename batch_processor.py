from pixels import WeirdPad
from PIL import Image
import os
import csv

class Effect(object):
    def __init__(self, name, params = []):
        self.name = name
        self.params = params


class BatchProcessor(object):

    def __init__(self):
        self._weird_pad = WeirdPad()

    def process_file(self, file_name, in_dir, out_dir, effects):
        pic = Image.open(in_dir + file_name)
        print "processing " + file_name
        for effect in effects:
            if effect["name"] == 'wordpad_pic_interval':
                pic = self._weird_pad.wordpad_pic_interval(pic, effect["args"]["glitch_target"], effect["args"]["interval"])
            elif effect["name"] == 'wordpad_by_color':
                pic = self._weird_pad.wordpad_by_color(pic, effect["args"]["target_color"], effect["args"]["tolerance"])
            elif effect["name"] == 'wordpad_rows_by_color':
                pic = self._weird_pad.wordpad_rows_by_color(pic, effect["args"]["target_color"], effect["args"]["tolerance"])


        pic.save(out_dir + 'processed_' + file_name)

    def process_folder(self, folder_name, effects):

        for pic in contents:
            self.process_file(pic, folder_name + '/', folder_name + '/', effects)


batcher = BatchProcessor()

todo = [
{
"name": "wordpad_pic_interval",
"args": {
"glitch_target": 150,
"interval": 5
}
}
# {
# "name": "wordpad_pic",
# "args": {
# "glitch_target": 100,
# "glitch_limit": 0
# }
# }
]

batcher.process_folder('in/tree', todo)
# batcher.process_file('tree_00166.jpg', 'in/tree/', 'in/', todo)
