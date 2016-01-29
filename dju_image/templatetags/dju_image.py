from django import template
from django.conf import settings
from ..tools import get_relative_path_from_img_id


register = template.Library()


@register.simple_tag
def dju_img_url(img_id, label=None, ext=None):
    if not img_id:
        return ''
    return settings.MEDIA_URL + get_relative_path_from_img_id(img_id, variant_label=label, ext=ext)
