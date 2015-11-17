import os
from PIL import Image
from PIL.ImageDraw import ImageDraw
from StringIO import StringIO
from django.conf import settings


def create_test_image(w, h, c='RGB'):
    colors = {
        'RGB': {1: '#DDEEFF', 2: '#667788', 3: '#887766'},
        'CMYK': {1: (120, 130, 140, 25), 2: (80, 100, 120, 50), 3: (120, 100, 80, 75)},
    }
    color = colors[c]
    img = Image.new(c, (w, h), color=color[1])
    d = ImageDraw(img)
    d.line((-1, -1) + img.size, fill=color[2], width=2)
    d.line((-1, img.size[1], img.size[0], -1), fill=color[3], width=2)
    return img


def get_img_file(img, img_format='JPEG', jpeg_quality=100):
    f = StringIO()
    img.save(f, img_format, quality=jpeg_quality)
    return f


def save_img_file(fn, img, img_format='JPEG', jpeg_quality=100):
    full_path = os.path.join(settings.TMP_DIR, fn)
    if os.path.exists(full_path):
        os.remove(full_path)
    with open(full_path, 'wb') as f:
        img.save(f, img_format, quality=jpeg_quality)
    return full_path
