""" Copy image with PIL/tobytes """
import PIL
from PIL import Image
import base64

im_in = Image.open('im.png')
im_in_b = im_in.tobytes()
im_in_size = (im_in.width, im_in.height)
im_in_mode = im_in.mode

im_out = PIL.Image.frombytes(im_in_mode, im_in_size, im_in_b)
im_out.save('immm.png', 'PNG')
