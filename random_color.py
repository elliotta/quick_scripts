#!/usr/bin/env python

import random # to generate a color
from time import time
random.seed(time)
from PIL import Image, ImageFont, ImageDraw # make the image
# from tempfile import NamedTemporaryFile # to put the image on disk
import subprocess # to put the image into the clipboard
from os import remove # clean up file


# Generate a color in hex
color = random.randint(0, 0xFFFFFF)
color_string = '#{:0>6}'.format(hex(color)[2:])
print('Your color is ' + color_string)

# Make an image with the color
im = Image.new(mode='RGB', size=(200, 200), color=color_string)

# Add the text, black over transparent white
draw = ImageDraw.Draw(im)
font = ImageFont.truetype("KL Sweet Berries Plump.ttf", 30)
w, h = font.getsize(color_string)
draw.rectangle((100-w/2., 100-h/2., 100+w/2., 100+h/2. ), fill='white')
draw.text((100-w/2., 100-h/2.), color_string, fill='black', font=font)

# Write to a file
f_name = '/tmp/foo.jpg'
im.save(f_name, im.format)
# Put in the clipboard
print(subprocess.run(['osascript', '-e', 'set the clipboard to (read (POSIX file "{}") as JPEG picture)'.format(f_name)], check=True))
print(subprocess.run(['osascript', '-e', 'clipboard info'], check=True))
# Clean up
remove(f_name)

# Show me!
#im.show()


