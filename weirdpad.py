from PIL import Image
from random import randint
import os

class WeirdPad(object):

    def __init__(self):
        """ inits an instance of WeirdPad """
        self._in_dir = ''
        self._out_dir = ''
        self._file_name = ''
        self._pic = None
        self._effects_applied = []

    def reset(self):
        """ resets current pic """
        self._pic = None
        self._effects_applied = []
        self._file_name = ''

    @property
    def in_dir(self):
        """ getter for _in_dir """
        return self._in_dir

    @in_dir.setter
    """ setter for _in_dir """
    def in_dir(self, in_dir):
        """
        sets default input directory
        """
        self._in_dir = in_dir

    @property
    def out_dir(self):
        """ getter for _out_dir """
        return self._out_dir

    @out_dir.setter
    def out_dir(self, out_dir):
        """
        sets default output directory
        """
        self._out_dir = out_dir

    def load_pic(self, file_name):
        """
        opens an image file and attaches it to this instance for processing
        """
        self._effects_applied = []
        self._file_name = file_name
        self._pic = Image.open(self._in_dir + self._file_name)

    def save_pic(self, reset = True):
        """
        saves a file of the current pic,
        resets self._pic unless reset = False
        """
        out_file_name = '_'.join(self._effects_applied) + '_' + self._file_name

        if not os.path.isdir(self._out_dir):
            os.makedirs(self._out_dir)
        self._pic.save(self._out_dir + out_file_name)

        if reset:
            self.reset()

    def get_lumosity(self, pixel):
        """
        gets lumosity for a pixel
        """
        return pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114

    def color_match(self, color, target_color, tolerance):
        """
        returns True if all channels in a color are
        equal to corresponding channel in target_color +/- tolerance
        """
        for channel in range(0, 3):
            if color[channel] not in range(target_color[channel] - tolerance, target_color[channel] + tolerance):
                return False
        return True

    def flatten_image(self, pic):
        """
        flattens image into list of ints
        """
        width = pic.size[0]
        height = pic.size[1]
        flattened_image = [None] * height * width * 3
        i = 0 # counter for flattened_image
        for h in range(0, height):
            for w in range(0, width):
                pixel = pic.getpixel((w,h))
                for channel in pixel:
                    flattened_image[i] = channel
                    i += 1
        return flattened_image

    def reconstruct_flattened_image(self, int_list, width, height):
        """
        constructs image of provided width and heigh from int list
        """
        image = Image.new('RGB', (width, height))
        reconstructed_output = []
        # each row of our output
        for h in range(0, height):
            current_row = []
            start = h * width * 3
            stop = start + width * 3
            for p in range(start, stop, 3):
                reconstructed_pixel = (int_list[p], int_list[p + 1], int_list[p + 2])
                w = p / 3 - h * width
                image.putpixel((w,h), reconstructed_pixel)
        return image

    def wordpad_flattened_input(self, flattened_input, glitch_target, interval):
        """
        iterates over flattend_image by provided interval
        and inserts glitch when glitch_target is encountered.
        throws away overhaning ints
        """
        output_length = len(flattened_input)
        # now copy flattened image to output flattened image but insert
        # glitches
        flattened_output = [None] * output_length

        fo = 0 # output counter

        for i in range(0, len(flattened_output), interval):
            if flattened_input[i] == glitch_target:
                flattened_output[fo] = 13
                fo += 1
                flattened_output[fo:fo+interval] = flattened_input[i:i+interval]
                fo += interval
            else:
                flattened_output[fo:fo+interval] = flattened_input[i:i+interval]
                fo += interval
            if fo >= output_length - interval:
                break

        for j in range(output_length - 1, -1, -1):
            if flattened_output[j] == None:
                flattened_output[j] = 255

        return flattened_output

    def wordpad_flattened_input_by_color(self, flattened_image, target_color, tolerance):
        """
        iterates over flattend_image by interval of 3
        and inserts glitch when three ints matchng color
        within tolerance is encountered.
        throws away overhaning ints.
        """
        output_length = len(flattened_image)
        flattened_output = [None] * output_length

        i = 0
        fo = 0
        glitch_count = 0

        while fo < output_length:
            pixel = (flattened_image[i], flattened_image[i + 1], flattened_image[i + 2])
            if self.color_match(pixel, target_color, tolerance):
                flattened_output[fo] = 255
                fo += 1
                glitch_count += 1

            if fo < output_length - 3:
                flattened_output[fo], flattened_output[fo + 1], flattened_output[fo + 2] = pixel
            elif fo < output_length - 2:
                flattened_output[fo], flattened_output[fo + 1] = (pixel[0], pixel[1])
            elif fo < output_length:
                flattened_output[fo] = pixel[0]
            i += 3
            fo += 3

        # in case we didn't land at the end
        if flattened_output[output_length - 1] == None:
            flattened_output[output_length - 1] = 255

        return flattened_output

    def wordpad(self, glitch_target, interval = 1):
        """
        flattens image, applies wordpad glitch, and reconstructs image
        """
        height = self._pic.size[1]
        width = self._pic.size[0]

        flat_image = self.flatten_image(self._pic)

        glitched_output = self.wordpad_flattened_input(flat_image, glitch_target, interval)

        self._pic = self.reconstruct_flattened_image(glitched_output, width, height)

        effect_name = 'wordpad-' + str(glitch_target) + '-' + str(interval)
        self._effects_applied.append(effect_name)

    def wordpad_rows(self, glitch_target, interval = 1):
        """
        effectively applies wordpad glitch to each
        row independanty (does not carry over to next row)
        """
        width = self._pic.size[0]
        height = self._pic.size[1]

        flattened_image = self.flatten_image(self._pic)
        glitched_output = [None] * len(flattened_image)

        # now loop through flattened_image one row's length at a time
        flat_row_length = width * 3
        for h in range(0, height):
            start = h * flat_row_length
            stop = start + flat_row_length
            flat_row = flattened_image[start:stop]
            glitched_row = self.wordpad_flattened_input(flat_row, glitch_target, interval)
            glitched_output[start:stop] = glitched_row

        self._pic = self.reconstruct_flattened_image(glitched_output, width, height)

        effect_name = 'wordpad-rows-' + str(glitch_target) + '-' + str(interval)
        self._effects_applied.append(effect_name)


    def wordpad_by_color(self, target_color = (255, 255, 255), tolerance = 0):
        """
        applies wordpad effect to pixels that match target_color within tolerance
        """
        width = self._pic.size[0]
        height = self._pic.size[1]
        flattened_image = self.flatten_image(self._pic)

        glitched_output = self.wordpad_flattened_input_by_color(flattened_image, target_color, tolerance)

        self._pic = self.reconstruct_flattened_image(glitched_output, width, height)

        effect_name = 'wordpad-by-color-' + str(target_color) + '-' + str(tolerance)
        self._effects_applied.append(effect_name)

    def wordpad_rows_by_color(self, target_color = (255, 255, 255), tolerance = 0):
        """
        applies wordpad_by_color effect to each row independantly
        """
        width = self._pic.size[0]
        height = self._pic.size[1]

        flattened_image = self.flatten_image(self._pic)
        output_length = len(flattened_image)
        flattened_output = [None] * output_length
        fo = 0 # output counter

        # loop through rows (row * width * 3)
        for row in range(0, height):
            start_of_row = row * width * 3
            pixel_counter = 0
            for i in range(start_of_row, start_of_row + width * 3, 3):
                if fo - start_of_row >= (width) * 3 - 3:
                    break
                pixel = (flattened_image[i], flattened_image[i + 1], flattened_image[i + 2])
                if self.color_match(pixel, target_color, tolerance):
                    flattened_output[fo] = randint(0,255)
                    fo += 1
                flattened_output[fo], flattened_output[fo + 1], flattened_output[fo + 2] = pixel
                fo += 3
                pixel_counter += 1
        # fill in any blanks in last row
        for channel in range(output_length - 1, 0, -1):
            if flattened_output[channel] == None:
                flattened_output[channel] = randint(0,255)
            else:
                break

        self._pic = self.reconstruct_flattened_image(flattened_output, width, height)

        effect_name = 'wordpad-rows-by-color-' + str(target_color) + '-' + str(tolerance)
        self._effects_applied.append(effect_name)
