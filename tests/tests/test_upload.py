import hashlib
import os
import re
from django.conf import settings
from django.test import TestCase
from dju_image.image import image_get_format
from dju_image.upload import (get_relative_path_from_img_id, generate_img_id, get_profile_configs,
                              get_variant_label, save_file)
from dju_image import settings as dju_settings
from tests.tests.tools import get_img_file, create_test_image, clean_media_dir


class TestUpload(TestCase):
    def setUp(self):
        super(TestUpload, self).setUp()
        clean_media_dir()

    def tearDown(self):
        super(TestUpload, self).tearDown()
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
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', ext='png'),
            'upload-img/common/34/abcde1234_ab12__m_93c87b2a66.png'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', variant_label='test'),
            'upload-img/common/34/abcde1234_ab12__v_b8a30d0227_test.jpeg'
        )
        self.assertEqual(
            get_relative_path_from_img_id('default:abcde1234_ab12.jpeg', variant_label='test', ext='png'),
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
