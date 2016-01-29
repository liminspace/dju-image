import glob
import os
import shutil
import copy
import simplejson
from contextlib import contextmanager
from PIL import Image
from PIL.ImageDraw import ImageDraw
from cStringIO import StringIO
from django.conf import settings
from django.test import TestCase
from dju_image import settings as dju_settings
from dju_image.tools import clear_profile_configs_cache, media_path


def create_test_image(w, h, c='RGB'):
    colors = {
        'RGB': {1: '#DDEEFF', 2: '#667788', 3: '#887766'},
        'CMYK': {1: (120, 130, 140, 25), 2: (80, 100, 120, 50), 3: (120, 100, 80, 75)},
        'P': {1: '#DDEEFF', 2: '#667788', 3: '#887766'},
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
    f.seek(0)
    return f


def save_img_file(fn, img, img_format='JPEG', jpeg_quality=100):
    full_path = os.path.join(settings.TMP_DIR, fn)
    if os.path.exists(full_path):
        os.remove(full_path)
    with open(full_path, 'wb') as f:
        img.save(f, img_format, quality=jpeg_quality)
    return full_path


def clean_media_dir():
    for fn in glob.glob(media_path('*')):
        if os.path.isdir(fn):
            shutil.rmtree(fn)
        else:
            os.remove(fn)


@contextmanager
def safe_change_dju_settings():
    """
    with safe_change_dju_settings():
        dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT['TYPES'] = ('PNG',)
        ...
    # dju settings will be restored
    ...
    """
    settings_bak = {}
    for k, v in dju_settings.__dict__.iteritems():
        if k[:4] == 'DJU_':
            settings_bak[k] = copy.deepcopy(v)
    try:
        yield
    finally:
        for k, v in settings_bak.iteritems():
            setattr(dju_settings, k, v)
        clear_profile_configs_cache()


class ViewTestCase(TestCase):
    def get_json(self, response):
        self.assertEqual(response['Content-Type'], 'application/json')
        try:
            data = simplejson.loads(response.content)
        except (TypeError, simplejson.JSONDecodeError):
            raise self.failureException('Response is not JSON')
        self.assertIsInstance(data, dict)
        self.assertIsInstance(data['uploaded'], list)
        self.assertIsInstance(data['errors'], list)
        return data

    def assertUploadedFilesExist(self, response_data):
        for item in response_data['uploaded']:
            path = media_path(item['rel_url'])
            self.assertTrue(os.path.isfile(path))
            for var_data in item['variants'].values():
                var_path = media_path(var_data['rel_url'])
                self.assertTrue(os.path.isfile(var_path))

    def assertUploadedFilesNotExist(self, response_data):
        for item in response_data['uploaded']:
            path = media_path(item['rel_url'])
            self.assertFalse(os.path.isfile(path))
            for var_data in item['variants'].values():
                var_path = media_path(var_data['rel_url'])
                self.assertFalse(os.path.isfile(var_path))


class CleanTmpDirMixin(object):
    @classmethod
    def _clean_tmp_dir(cls):
        for fn in glob.glob(os.path.join(settings.TMP_DIR, '*')):
            if os.path.isdir(fn):
                shutil.rmtree(fn)
            else:
                os.remove(fn)
