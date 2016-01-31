import datetime
from contextlib import contextmanager
from django.test import TestCase
from dju_image.maintenance import remove_old_tmp_files
from dju_image.tools import make_permalink, upload_from_fs
from .tools import create_test_image, clean_media_dir, save_img_file, CleanTmpDirMixin


@contextmanager
def patch_utcnow(timeshift=None, dt=None):
    if timeshift is None:
        timeshift = datetime.timedelta()
    if dt is None:
        dt = datetime.datetime(2016, 1, 2, 15, 20, 35, 112233)

    class ShiftedDateTime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return dt + timeshift

    old = datetime.datetime
    datetime.datetime = ShiftedDateTime
    yield
    datetime.datetime = old


class TestMaintenance(TestCase, CleanTmpDirMixin):
    def setUp(self):
        super(TestCase, self).setUp()
        clean_media_dir()
        self._clean_tmp_dir()

    def tearDown(self):
        super(TestCase, self).tearDown()
        clean_media_dir()
        self._clean_tmp_dir()

    def test_remove_old_tmp_files(self, ):
        fn = save_img_file('t1.jpeg', create_test_image(600, 600))
        with patch_utcnow(-datetime.timedelta(hours=10)):
            upload_from_fs(fn, profile='simple1')
        with patch_utcnow(-datetime.timedelta(hours=11)):
            make_permalink(upload_from_fs(fn, profile='simple0'))

        with patch_utcnow():
            deleted, total = remove_old_tmp_files(['simple1'], max_lifetime=12)
            self.assertEqual((deleted, total), (0, 5))

            deleted, total = remove_old_tmp_files(max_lifetime=12)
            self.assertEqual((deleted, total), (0, 5))

            deleted, total = remove_old_tmp_files(['simple1'], max_lifetime=9)
            self.assertEqual((deleted, total), (5, 5))
