import glob
import os
import re
import shutil
from django.conf import settings
from django.test import TestCase
from dju_image.upload import get_relative_path_from_img_id, generate_img_id


class TestUpload(TestCase):
    def setUp(self):
        super(TestUpload, self).setUp()
        self._clean_media_dir()

    def tearDown(self):
        super(TestUpload, self).tearDown()
        self._clean_media_dir()

    def _clean_media_dir(self):
        for fn in glob.glob(os.path.join(settings.MEDIA_ROOT, '*')):
            if os.path.isdir(fn):
                shutil.rmtree(fn)
            else:
                os.remove(fn)

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
