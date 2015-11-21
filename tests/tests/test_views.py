import os
from cStringIO import StringIO
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import override_settings
from dju_image.tools import get_relative_path_from_img_id, clear_profile_configs_cache, ERROR_MESSAGES as TOOLS_ERRORS
from dju_image.views import ERROR_MESSAGES as VIEWS_ERRORS
from tests.tests.tools import (get_img_file, create_test_image, clean_media_dir, safe_change_dju_settings,
                               ViewTestCase)
from dju_image import settings as dju_settings


class TestViews(ViewTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        cls.upload_url = reverse('dju_image_upload')

    def setUp(self):
        super(TestViews, self).setUp()
        clean_media_dir()

    def tearDown(self):
        super(TestViews, self).tearDown()
        clean_media_dir()

    def test_upload_image_wrong_request_method(self):
        self.assertEqual(self.client.get(self.upload_url).status_code, 405)
        self.assertEqual(self.client.head(self.upload_url).status_code, 405)
        self.assertEqual(self.client.options(self.upload_url).status_code, 405)
        self.assertEqual(self.client.put(self.upload_url).status_code, 405)
        self.assertEqual(self.client.trace(self.upload_url).status_code, 405)
        self.assertEqual(self.client.patch(self.upload_url).status_code, 405)
        self.assertEqual(self.client.delete(self.upload_url).status_code, 405)

    def test_upload_image_empty_data_and_files(self):
        r = self.client.post(self.upload_url)
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), 0)
        self.assertEqual(len(d['errors']), 1)
        self.assertEqual(d['errors'][0], unicode(VIEWS_ERRORS['no_uploaded_files']))

    def test_upload_image_without_profile(self):
        f = get_img_file(create_test_image(1000, 1000))
        r = self.client.post(self.upload_url, {'images[]': [f]})
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), 1)
        self.assertEqual(len(d['errors']), 0)
        item = d['uploaded'][0]
        self.assertIn('url', item)
        self.assertIn('rel_url', item)
        self.assertIn('img_id', item)
        self.assertIn('variants', item)
        self.assertIn('variants_by_label', item)
        self.assertIsInstance(item['url'], basestring)
        self.assertIsInstance(item['rel_url'], basestring)
        self.assertIsInstance(item['img_id'], basestring)
        self.assertIsInstance(item['variants'], list)
        self.assertIsInstance(item['variants_by_label'], dict)
        self.assertEqual(len(item['variants']), 0)
        self.assertEqual(len(item['variants_by_label']), 0)
        self.assertTrue(item['img_id'].startswith('default:' + dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX))
        self.assertTrue(item['img_id'].endswith('.jpeg'))
        self.assertEqual(get_relative_path_from_img_id(item['img_id']), item['rel_url'])
        self.assertEqual(settings.MEDIA_URL + item['rel_url'], item['url'])
        self.assertUploadedFilesExist(d)
        f.seek(0)
        r = self.client.post(self.upload_url, {'images[]': [f], 'label': 'lab'})
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        item = d['uploaded'][0]
        self.assertTrue(item['img_id'].endswith('_lab.jpeg'))
        self.assertUploadedFilesExist(d)

    def test_upload_image_wrong_file(self):
        f = StringIO('0' * 1024 * 1024)
        r = self.client.post(self.upload_url, {'images[]': [f]})
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), 0)
        self.assertEqual(len(d['errors']), 1)
        self.assertEqual(
            d['errors'][0],
            unicode(VIEWS_ERRORS['wrong_file_format']) % {
                'name': 'images[]',
                'formats': ', '.join(map(lambda t: t.upper(), dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT['TYPES']))
            }
        )

    @override_settings()
    def test_upload_image_wrong_image_format(self):
        with safe_change_dju_settings():
            dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT['TYPES'] = ('PNG',)
            clear_profile_configs_cache()
            f = get_img_file(create_test_image(1000, 1000))
            r = self.client.post(self.upload_url, {'images[]': [f]})
            self.assertEqual(r.status_code, 200)
            d = self.get_json(r)
            self.assertEqual(len(d['uploaded']), 0)
            self.assertEqual(len(d['errors']), 1)
            self.assertEqual(
                d['errors'][0],
                unicode(VIEWS_ERRORS['wrong_file_format']) % {
                    'name': 'images[]',
                    'formats': ', '.join(map(lambda t: t.upper(), dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT['TYPES']))
                }
            )

    def test_upload_image_wrong_profile(self):
        f = get_img_file(create_test_image(1000, 1000))
        r = self.client.post(self.upload_url, {'images[]': [f], 'profile': 'wrong'})
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), 0)
        self.assertEqual(len(d['errors']), 1)
        self.assertEqual(d['errors'][0], unicode(TOOLS_ERRORS['unknown_profile']) % {'profile': 'wrong'})

    def test_upload_image_variants(self):
        f1 = get_img_file(create_test_image(1000, 1000))
        f2 = get_img_file(create_test_image(1000, 1000))
        for r in (self.client.post(self.upload_url, {'images[]': [f1], 'profile': 'simple1'}),
                  self.client.post(self.upload_url, {'images[]': [f2], 'profile': 'simple1', 'label': 'lab'})):
            self.assertEqual(r.status_code, 200)
            d = self.get_json(r)
            variants = d['uploaded'][0]['variants']
            self.assertEqual(len(variants), 4)
            name = os.path.splitext(d['uploaded'][0]['img_id'])[0].split(':', 1)[1]
            for item in variants:
                self.assertIsInstance(item['url'], basestring)
                self.assertIsInstance(item['rel_url'], basestring)
                self.assertIn(name, item['url'])
                self.assertIn(name, item['rel_url'])
            self.assertTrue(variants[0]['url'].endswith('_20x30.jpeg'))
            self.assertTrue(variants[1]['url'].endswith('_w20.jpeg'))
            self.assertTrue(variants[2]['url'].endswith('_h30.jpeg'))
            self.assertTrue(variants[3]['url'].endswith('_lab1.jpeg'))
            variants_by_label = d['uploaded'][0]['variants_by_label']
            self.assertEqual(len(variants_by_label), 4)
            self.assertEqual(variants_by_label['20x30'], 0)
            self.assertEqual(variants_by_label['w20'], 1)
            self.assertEqual(variants_by_label['h30'], 2)
            self.assertEqual(variants_by_label['lab1'], 3)
            self.assertUploadedFilesExist(d)

    def test_upload_image_multiple_files(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple1'
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
