from django import template
from django.conf import settings
from ..tools import get_relative_path_from_img_id


register = template.Library()


@register.assignment_tag  # todo move to simple_tag after migrate to django 1.9
def dju_img_url(img_id, label=None, ext=None):
    return settings.MEDIA_URL + get_relative_path_from_img_id(img_id, variant_label=label, ext=ext)
