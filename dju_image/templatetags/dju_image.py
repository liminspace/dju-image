import django
from django import template
from django.conf import settings
from ..tools import get_relative_path_from_img_id


register = template.Library()


if django.VERSION < (1, 9):
    simple_or_assignment_tag = register.assignment_tag
else:
    simple_or_assignment_tag = register.simple_tag


@simple_or_assignment_tag
def dju_img_url(img_id, label=None, ext=None):
    if not img_id:
        return ''
    try:
        return settings.MEDIA_URL + get_relative_path_from_img_id(img_id, variant_label=label, ext=ext)
    except ValueError:
        return ''
