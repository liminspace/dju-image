from django.http import QueryDict
from django.template import Template, Context
from django.test import TestCase
from dju_image import settings as dju_settings


class TestTemplatetagsDjUtils(TestCase):
    class R(object):
        def __init__(self, query):
            self.GET = QueryDict(query)

    def get_tpl_f(self, tpl, context=None):
        return lambda: Template('{% load dju_image %}' + tpl).render(Context(context))

    # def test_make_thumb_url(self):  # todo do it
    #     suf = dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
    #
    #     t = self.get_tpl_f("{% make_thumb_url '/media/a/b/abc.jpeg' as v %}{{ v }}")
    #     self.assertEqual(t(), '/media/a/b/abc{suf}.jpeg'.format(suf=suf))
    #
    #     t = self.get_tpl_f(
    #         "{% make_thumb_url '/media/a/b/abc{suf}.jpeg' as v %}{{ v }}".replace('{suf}', suf)
    #     )
    #     self.assertEqual(t(), '/media/a/b/abc{suf}.jpeg'.format(suf=suf))
    #
    #     t = self.get_tpl_f("{% make_thumb_url '/media/a/b/abc.dat' label='tst' ext='png' as v %}{{ v }}")
    #     self.assertEqual(t(), '/media/a/b/abc{suf}tst.png'.format(suf=suf))
    #
    #     t = self.get_tpl_f("{% make_thumb_url '/media/a/b/abc.dat' label='tst' ext='png' as v %}{{ v }}")
    #     self.assertEqual(t(), '/media/a/b/abc{suf}tst.png'.format(suf=suf))
    #
    #     t = self.get_tpl_f("{% make_thumb_url '/media/a/b/abc.dat' label='tst' ext='.png' as v %}{{ v }}")
    #     self.assertEqual(t(), '/media/a/b/abc{suf}tst.png'.format(suf=suf))
