import unittest
import django
from django.conf import settings
from django.template import Template, Context
from django.test import TestCase
from dju_image import settings as dju_settings


class TestTemplatetagsDjUtils(TestCase):
    def get_tpl_f(self, tpl, context=None):
        return lambda: Template('{% load dju_image %}' + tpl).render(Context(context))

    def test_dju_img_url_with_as(self):
        # main image without label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='.jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='.jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))

        # main image with label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' label='lab1' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='.jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='.jpeg' as v %}{{ v }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))

    @unittest.skipIf(django.VERSION >= (1, 9), 'Skip django >= 1.9')
    def test_dju_img_url_django_1_8(self):
        # main image without label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))

        # main image with label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' label='lab1' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))


    @unittest.skipIf(django.VERSION < (1, 9), 'Skip django < 1.9')
    def test_dju_img_url_django_1_9_up(self):
        # main image without label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' ext='.jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' ext='.jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}94c41774a6.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX,
        ))

        # main image with label
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.jpeg' label='lab1' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7' label='lab1' ext='.jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))
        t = self.get_tpl_f("{% dju_img_url 'simple1:ihrtfelu_c5e7.png' label='lab1' ext='.jpeg' %}")
        self.assertEqual(t(), '{}upload-img/s1/lu/ihrtfelu_c5e7{}38728b6f68_lab1.jpeg'.format(
            settings.MEDIA_URL,
            dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX,
        ))

    @unittest.skipIf(django.VERSION >= (1, 9), 'Skip django >= 1.9')
    def test_dju_img_url_wrong_imgid_django_1_8(self):
        t = self.get_tpl_f("{% dju_img_url 'simple1ihrtfelu_c5e7.jpeg' as t %}{{ t }}")
        self.assertEqual(t(), '')

        t = self.get_tpl_f("{% dju_img_url '' as t %}{{ t }}")
        self.assertEqual(t(), '')

    @unittest.skipIf(django.VERSION < (1, 9), 'Skip django < 1.9')
    def test_dju_img_url_wrong_imgid_django_1_9_up(self):
        t = self.get_tpl_f("{% dju_img_url 'simple1ihrtfelu_c5e7.jpeg' %}")
        self.assertEqual(t(), '')

        t = self.get_tpl_f("{% dju_img_url '' %}")
        self.assertEqual(t(), '')
