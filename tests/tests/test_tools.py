import hashlib
import os
import re
import shutil
from django.conf import settings
from django.core.urlresolvers import reverse
from dju_image.image import image_get_format
from dju_image.tools import (get_relative_path_from_img_id, generate_img_id, get_profile_configs,
                             get_variant_label, save_file, get_files_by_img_id, HASH_SIZE,
                             remove_tmp_prefix_from_filename, remove_tmp_prefix_from_file_path, make_permalink)
from dju_image import settings as dju_settings
from tests.tests.tools import get_img_file, create_test_image, clean_media_dir, ViewTestCase


class TestTools(ViewTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestTools, cls).setUpClass()
        cls.upload_url = reverse('dju_image_upload')

    def setUp(self):
        super(TestTools, self).setUp()
        clean_media_dir()

    def tearDown(self):
        super(TestTools, self).tearDown()
        clean_media_dir()

    def test_generate_img_id(self):
        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:[a-z0-9]{8,11}_[a-z0-9]{4}$',
                                          generate_img_id('simple1')))
        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:[a-z0-9]{8,11}_[a-z0-9]{4}\.png$',
                                          generate_img_id('simple1', ext='png')))
        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:[a-z0-9]{8,11}_[a-z0-9]{4}_tst$',
                                          generate_img_id('simple1', label='tst')))
        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:[a-z0-9]{8,11}_[a-z0-9]{4}_tst\.png$',
                                          generate_img_id('simple1', ext='png', label='tst')))

        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:__t_[a-z0-9]{8,11}_[a-z0-9]{4}$',
                                          generate_img_id('simple1', tmp=True)))

        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:__t_[a-z0-9]{8,11}_[a-z0-9]{4}\.png$',
                                          generate_img_id('simple1', tmp=True, ext='png')))

        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:__t_[a-z0-9]{8,11}_[a-z0-9]{4}_tst$',
                                          generate_img_id('simple1', tmp=True, label='tst')))

        for i in xrange(50):
            self.assertIsNotNone(re.match(r'^simple1:__t_[a-z0-9]{8,11}_[a-z0-9]{4}_tst\.png$',
                                          generate_img_id('simple1', tmp=True, label='tst', ext='png')))
        self.assertIsNotNone(re.match(
            r'^simple1:[a-z0-9]{8,11}_[a-z0-9]{4}_ts_ABC159\-q_qweyuoopzts_ABC159\-q_qweyuoopzts_ABC159\-q_qweyuo$',
            generate_img_id('simple1', label=('ts_/ABC159-q___q(w..e#y%uo&op*?z' * 5))
        ))

    def test_get_relative_path_from_img_id(self):
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg'),
            'upload-img/common/34/abcde1234_ab12__m_93c87b2a66.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12'),
            'upload-img/common/34/abcde1234_ab12__m_93c87b2a66'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', ext='png'),
            'upload-img/common/34/abcde1234_ab12__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12', ext='png'),
            'upload-img/common/34/abcde1234_ab12__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', variant_label='test'),
            'upload-img/common/34/abcde1234_ab12__v_b8a30d0227_test.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12', variant_label='test'),
            'upload-img/common/34/abcde1234_ab12__v_b8a30d0227_test'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', variant_label='test', ext='png'),
            'upload-img/common/34/abcde1234_ab12__v_b8a30d0227_test.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12', variant_label='test', ext='png'),
            'upload-img/common/34/abcde1234_ab12__v_b8a30d0227_test.png'
        )

        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12.jpeg'),
            'upload-img/common/34/__t_abcde1234_ab12__m_93c87b2a66.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12.jpeg', ext='png'),
            'upload-img/common/34/__t_abcde1234_ab12__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12.jpeg', variant_label='test'),
            'upload-img/common/34/__t_abcde1234_ab12__v_b8a30d0227_test.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12.jpeg', variant_label='test', ext='png'),
            'upload-img/common/34/__t_abcde1234_ab12__v_b8a30d0227_test.png'
        )

        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12_myname.jpeg'),
            'upload-img/common/34/abcde1234_ab12_myname__m_93c87b2a66.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12_myname'),
            'upload-img/common/34/abcde1234_ab12_myname__m_93c87b2a66'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12_myname.jpeg', ext='png'),
            'upload-img/common/34/abcde1234_ab12_myname__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12_myname.jpeg', variant_label='test'),
            'upload-img/common/34/abcde1234_ab12_myname__v_b8a30d0227_test.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12_myname.jpeg', variant_label='test', ext='png'),
            'upload-img/common/34/abcde1234_ab12_myname__v_b8a30d0227_test.png'
        )

        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12_myname.jpeg'),
            'upload-img/common/34/__t_abcde1234_ab12_myname__m_93c87b2a66.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12_myname.jpeg', ext='png'),
            'upload-img/common/34/__t_abcde1234_ab12_myname__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12_myname.jpeg', variant_label='test'),
            'upload-img/common/34/__t_abcde1234_ab12_myname__v_b8a30d0227_test.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12_myname.jpeg', variant_label='test', ext='png'),
            'upload-img/common/34/__t_abcde1234_ab12_myname__v_b8a30d0227_test.png'
        )

        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12.jpeg', variant_label='20x30'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_51c425ba08_20x30.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12', variant_label='20x30'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_51c425ba08_20x30.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12.jpeg', variant_label='w20'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_a4b31265b5_w20.gif'
        )
        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12.jpeg', variant_label='w20', ext='png'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_a4b31265b5_w20.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12.png', variant_label='lab0'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_4f495406be_lab0.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('simple0:__t_abcde1234_ab12.png', variant_label='lab0', ext='gif'),
            'upload-img/s0/34/__t_abcde1234_ab12__v_4f495406be_lab0.gif'
        )

    def test_get_relative_path_from_img_id_with_create_dirs(self):
        self.assertEqual(
            get_relative_path_from_img_id('default:__t_abcde1234_ab12_myname.jpeg', create_dirs=True),
            'upload-img/common/34/__t_abcde1234_ab12_myname__m_93c87b2a66.jpeg'
        )
        self.assertTrue(os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'upload-img/common/34')))

    def test_get_profile_configs(self):
        c = get_profile_configs('simple1')
        rc = dju_settings.DJU_IMG_UPLOAD_PROFILES['simple1']
        self.assertEqual(c['PATH'], rc['PATH'])
        self.assertEqual(c['MAX_SIZE'], rc['MAX_SIZE'])
        self.assertEqual(len(c['VARIANTS']), len(rc['VARIANTS']))
        for i in xrange(len(rc['VARIANTS'])):
            for k in rc['VARIANTS'][i]:
                self.assertEqual(rc['VARIANTS'][i][k], c['VARIANTS'][i][k])

        self.assertEqual(get_profile_configs('default'), dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT)

        with self.assertRaises(ValueError):
            get_profile_configs('none')

    def test_get_variant_label(self):
        self.assertEqual(get_variant_label({'MAX_SIZE': (10, 20)}), '10x20')
        self.assertEqual(get_variant_label({'MAX_SIZE': (10, None)}), 'w10')
        self.assertEqual(get_variant_label({'MAX_SIZE': (None, 20)}), 'h20')

    def test_save_file(self):
        f = get_img_file(create_test_image(1000, 1000))
        img_id = generate_img_id('simple1', ext=image_get_format(f), label='test-save-file')
        relative_path = get_relative_path_from_img_id(img_id)
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path).replace('\\', '/')
        save_file(f, full_path)
        file_exists = os.path.exists(full_path)
        self.assertTrue(file_exists)
        if file_exists:
            f.seek(0)
            h1 = hashlib.md5(f.read()).hexdigest()
            h2 = hashlib.md5(open(full_path, 'rb').read()).hexdigest()
            self.assertEqual(h1, h2)

    def test_get_files_by_img_id(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple1',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            r = get_files_by_img_id(item['img_id'])
            self.assertEqual(r['main'], item['rel_url'])
            self.assertEqual(len(item['variants']), len(r['variants']))
            for var_label, ix in item['variants_by_label'].iteritems():
                self.assertEqual(r['variants'][var_label], item['variants'][ix]['rel_url'])

        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple1',
            'label': 'world1',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            r = get_files_by_img_id(item['img_id'])
            self.assertEqual(r['main'], item['rel_url'])
            self.assertEqual(len(item['variants']), len(r['variants']))
            for var_label, ix in item['variants_by_label'].iteritems():
                self.assertEqual(r['variants'][var_label], item['variants'][ix]['rel_url'])

    def test_get_files_by_img_id_removed_variants_ext(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple0',
            'label': 'world0',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            for i in xrange(len(item['variants'])):
                # remove ext for all variants files
                rel_url = item['variants'][i]['rel_url']
                rel_url_new = os.path.splitext(rel_url)[0]
                os.rename(
                    os.path.join(settings.MEDIA_ROOT, rel_url).replace('\\', '/'),
                    os.path.join(settings.MEDIA_ROOT, rel_url_new).replace('\\', '/')
                )
                item['variants'][i]['rel_url'] = rel_url_new
            r = get_files_by_img_id(item['img_id'])
            self.assertEqual(r['main'], item['rel_url'])
            self.assertEqual(len(item['variants']), len(r['variants']))
            for var_label, ix in item['variants_by_label'].iteritems():
                self.assertEqual(r['variants'][var_label], item['variants'][ix]['rel_url'])

    def test_get_files_by_img_id_with_invalid_hash_and_filename_pattern(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple0',
            'label': 'world0',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            for var_item in item['variants']:
                # add file with invalid hash
                rel_url = var_item['rel_url']
                rel_url_new = re.sub(
                    r'({suf})[a-z0-9]{{hs}}(_.+)'.replace(
                        '{suf}', dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
                    ).replace(
                        '{hs}', str(HASH_SIZE)
                    ),
                    r'\1{h}\2'.replace('{h}', 'z' * HASH_SIZE),
                    rel_url
                )
                shutil.copy(
                    os.path.join(settings.MEDIA_ROOT, rel_url).replace('\\', '/'),
                    os.path.join(settings.MEDIA_ROOT, rel_url_new).replace('\\', '/')
                )
                # add file with invalid filename pattern
                rel_url = var_item['rel_url']
                rel_url_new = re.sub(
                    r'({suf})[a-z0-9]{{hs}}(_.+)'.replace(
                        '{suf}', dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
                    ).replace(
                        '{hs}', str(HASH_SIZE)
                    ),
                    r'\1{h}\2'.replace('{h}', 'z' * (HASH_SIZE + 1)),
                    rel_url
                )
                shutil.copy(
                    os.path.join(settings.MEDIA_ROOT, rel_url).replace('\\', '/'),
                    os.path.join(settings.MEDIA_ROOT, rel_url_new).replace('\\', '/')
                )
            r = get_files_by_img_id(item['img_id'])
            self.assertEqual(r['main'], item['rel_url'])
            self.assertEqual(len(item['variants']), len(r['variants']))
            for var_label, ix in item['variants_by_label'].iteritems():
                self.assertEqual(r['variants'][var_label], item['variants'][ix]['rel_url'])

    def test_get_files_by_img_id_with_invalid_hash_and_ignore_check_hash(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple0',
            'label': 'world0',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            for var_item in item['variants']:
                # add file with invalid hash
                rel_url = var_item['rel_url']
                rel_url_new = re.sub(
                    r'({suf})[a-z0-9]{{hs}}(_.+)'.replace(
                        '{suf}', dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
                    ).replace(
                        '{hs}', str(HASH_SIZE)
                    ),
                    r'\1{h}\2'.replace('{h}', 'z' * HASH_SIZE),
                    rel_url
                )
                os.rename(
                    os.path.join(settings.MEDIA_ROOT, rel_url).replace('\\', '/'),
                    os.path.join(settings.MEDIA_ROOT, rel_url_new).replace('\\', '/')
                )
                var_item['rel_url'] = rel_url_new
            r = get_files_by_img_id(item['img_id'], check_hash=False)
            self.assertEqual(r['main'], item['rel_url'])
            self.assertEqual(len(item['variants']), len(r['variants']))
            for var_label, ix in item['variants_by_label'].iteritems():
                self.assertEqual(r['variants'][var_label], item['variants'][ix]['rel_url'])

    def test_get_files_by_img_id_file_is_not_exists(self):
        r = get_files_by_img_id(generate_img_id('simple0'))
        self.assertIsNone(r)

    def test_remove_tmp_prefix_from_filename(self):
        fn = 'test_file_name.jpeg'
        fn_tmp = dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX + fn
        self.assertEqual(remove_tmp_prefix_from_filename(fn_tmp), fn)

        with self.assertRaises(RuntimeError):
            remove_tmp_prefix_from_filename(fn)

    def test_remove_tmp_prefix_from_file_path(self):
        fn = 'test_file_name.jpeg'
        fn_tmp = dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX + fn
        path = '/some/path/'
        file_path = path + fn
        file_path_tmp = path + fn_tmp
        self.assertEqual(remove_tmp_prefix_from_file_path(file_path_tmp), file_path)

        with self.assertRaises(RuntimeError):
            remove_tmp_prefix_from_file_path(file_path)

    def test_make_permalink(self):
        r = self.client.post(self.upload_url, {
            'images[]': [
                get_img_file(create_test_image(1000, 1000)),
                get_img_file(create_test_image(900, 900)),
                get_img_file(create_test_image(800, 800)),
                get_img_file(create_test_image(700, 700)),
            ],
            'profile': 'simple0',
            'label': 'world0',
        })
        self.assertEqual(r.status_code, 200)
        d = self.get_json(r)
        self.assertEqual(len(d['uploaded']), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)
        self.assertEqual(len(d['errors']), 0)
        self.assertUploadedFilesExist(d)
        for item in d['uploaded']:
            new_img_id = make_permalink(item['img_id'])
            files = get_files_by_img_id(new_img_id)
            self.assertEqual(files['main'], remove_tmp_prefix_from_file_path(item['rel_url']))
            new_item = {
                'rel_url': files['main'],
                'variants': [],
            }
            for var_label, var_ix in item['variants_by_label'].iteritems():
                self.assertEqual(
                    files['variants'][var_label],
                    remove_tmp_prefix_from_file_path(item['variants'][var_ix]['rel_url'])
                )
                new_item['variants'].append({'rel_url': files['variants'][var_label]})
            self.assertUploadedFilesExist({'uploaded': [new_item]})
