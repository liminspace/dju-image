# coding=utf-8
import os
import copy
import re
import hashlib
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy
from django.conf import settings
from dju_common.file import make_dirs_for_file_path
from dju_common.tools import datetime_to_dtstr
from . import settings as dju_settings


ERROR_MESSAGES = {
    'unknown_profile': ugettext_lazy('Unknown profile "%(profile)s".')
}


_profile_configs_cache = {}


def clear_profile_configs_cache():
    _profile_configs_cache.clear()


def save_file(f, full_path):
    """
    Saves file f to full_path and set rules.
    """
    make_dirs_for_file_path(full_path, mode=dju_settings.DJU_IMG_CHMOD_DIR)
    with open(full_path, 'wb') as t:
        f.seek(0)
        while True:
            buf = f.read(dju_settings.DJU_IMG_RW_FILE_BUFFER_SIZE)
            if not buf:
                break
            t.write(buf)
    os.chmod(full_path, dju_settings.DJU_IMG_CHMOD_FILE)


def get_profile_configs(profile=None, use_cache=True):
    """
    Returns upload configs for profile.
    """
    if use_cache and profile in _profile_configs_cache:
        return _profile_configs_cache[profile]
    profile_conf = None
    if profile is not None:
        try:
            profile_conf = dju_settings.DJU_IMG_UPLOAD_PROFILES[profile]
        except KeyError:
            if profile != 'default':
                raise ValueError(unicode(ERROR_MESSAGES['unknown_profile']) % {'profile': profile})
    conf = copy.deepcopy(dju_settings.DJU_IMG_UPLOAD_PROFILE_DEFAULT)
    if profile_conf:
        conf.update(copy.deepcopy(profile_conf))
        for v_i in xrange(len(conf['VARIANTS'])):
            v = conf['VARIANTS'][v_i]
            conf['VARIANTS'][v_i] = copy.deepcopy(dju_settings.DJU_IMG_UPLOAD_PROFILE_VARIANT_DEFAULT)
            conf['VARIANTS'][v_i].update(v)
    if use_cache:
        _profile_configs_cache[profile] = conf
    return conf


def generate_img_id(profile, ext=None, label=None, tmp=False):
    """
    Generates img_id.
    """
    if ext and not ext.startswith('.'):
        ext = '.' + ext
    if label:
        label = re.sub(r'[^a-z0-9_\-]', '', label, flags=re.I)
        label = re.sub(r'_+', '_', label)
        label = label[:60]
    return '{profile}:{tmp}{dtstr}_{rand}{label}{ext}'.format(
        profile=profile,
        tmp=(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX if tmp else ''),
        dtstr=datetime_to_dtstr(),
        rand=get_random_string(4, 'abcdefghijklmnopqrstuvwxyz0123456789'),
        label=(('_' + label) if label else ''),
        ext=(ext or ''),
    )


def get_relative_path_from_img_id(img_id, variant_label=None, ext=None, create_dirs=False):
    """
    Returns path to file relative MEDIA_URL.
    """
    profile, base_name = img_id.split(':', 1)
    conf = get_profile_configs(profile)
    if not variant_label:
        status_suffix = dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX
    else:
        status_suffix = dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
    name, file_ext = os.path.splitext(base_name)
    prefix = ''
    if name.startswith(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):
        name = name[len(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):]
        prefix = dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX
    name_parts = name.split('_', 2)
    h = hashlib.sha1('_'.join(name_parts[:2]) + (variant_label or '') + dju_settings.DJU_IMG_UPLOAD_KEY).hexdigest()
    name = '{name}{status_suffix}{hash}'.format(
        name=name,
        status_suffix=status_suffix,
        hash=h[:10],
    )
    if variant_label:
        name += '_' + variant_label
    if ext:
        file_ext = ext
    elif variant_label:
        pass
        # todo file_ext = get ext from variant settings if it setted there
    if not file_ext.startswith('.'):
        file_ext = '.' + file_ext
    relative_path = os.path.join(
        dju_settings.DJU_IMG_UPLOAD_SUBDIR,
        conf['PATH'],
        name_parts[0][-2:],
        (prefix + name + file_ext)
    ).replace('\\', '/')
    if create_dirs:
        path = os.path.join(settings.MEDIA_ROOT, relative_path).replace('\\', '/')
        make_dirs_for_file_path(path, mode=dju_settings.DJU_IMG_CHMOD_DIR)
    return relative_path


def get_variant_label(v_conf):
    """
    Generates name for variant images based settings (by variants sizes).
    """
    if v_conf['MAX_SIZE'][0] is None:
        return 'h{}'.format(v_conf['MAX_SIZE'][1])
    if v_conf['MAX_SIZE'][1] is None:
        return 'w{}'.format(v_conf['MAX_SIZE'][0])
    return '{}x{}'.format(*v_conf['MAX_SIZE'])


def get_files_by_img_id(img_id):
    """
    Шукає файли для img_id.
    Повертає:
    {
        'main': 'relative path to main image',
        'variants': {
            'label': 'relative path to variant image by label',
            ...
        }
    }
    """
    pass  # todo make it
    # dir_path, filename = os.path.split(os.path.abspath(filepath))
    # name = add_thumb_suffix_to_filename(os.path.splitext(filename)[0], label=label)
    # pattern = os.path.join(dir_path, name).replace('\\', '/') + '*.*'
    # return [fn.replace('\\', '/') for fn in glob.iglob(pattern)
    #         if os.path.splitext(fn)[1].lstrip('.').lower() in dju_settings.DJU_IMG_UPLOAD_IMG_EXTS]


# def get_filepath_of_url(url):  # todo remove it
#     """ Повертає шлях до файлу MEDIA по URL-адресі. """
#     if url.startswith(settings.MEDIA_URL):
#         url = url[len(settings.MEDIA_URL):]
#     fn = os.path.join(settings.MEDIA_ROOT, os.path.normpath(url)).replace('\\', '/')
#     return fn


# def remove_file_by_url(url, with_thumbs=True):  # todo remove it
#     """
#     Видаляє файл по URL, якщо він знаходиться в папці MEDIA.
#     with_thumbs - шукати і видаляти мініатюри файлу.
#     """
#     files = [get_filepath_of_url(url)]
#     if with_thumbs:
#         files.extend(get_thumbs_for_image(files[0]))
#     for filepath in files:
#         if os.path.isfile(filepath):
#             os.remove(filepath)


# def move_to_permalink(url, with_thumbs=True):  # todo remove it
#     """
#     Видаляє з файлу маркер тимчасовості.
#     with_thumbs - шукати і застосовувати дану функцію на мініатюрах.
#     """
#     r = re.compile(r'^(.+?)(%s)(.+?)$' % dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX, re.I)
#     url_m = r.match(url)
#     if url_m:
#         main_filename = get_filepath_of_url(url)
#         if not os.path.isfile(main_filename):
#             return url
#         files = [main_filename]
#         if with_thumbs:
#             files.extend(get_thumbs_for_image(main_filename))
#         for filepath in files:
#             fn_m = r.match(filepath)
#             if fn_m:
#                 try:
#                     os.rename(filepath, fn_m.group(1) + fn_m.group(3))
#                 except EnvironmentError, e:
#                     # pass  # todo додати логування помилки
#                     raise e
#             else:
#                 pass  # todo додати логування неспівпадіння імені файлу до шаблону
#         url = url_m.group(1) + url_m.group(3)
#     return url


def make_permalink(img_id):
    """
    Видаляє з назви файлу префікс DJU_IMG_UPLOAD_TMP_PREFIX
    і перейменовує основний файл та всі його варіанти.
    Повертає img_id без префікса DJU_IMG_UPLOAD_TMP_PREFIX.
    """
    pass  # todo make it


def make_permalink_by_img_url(img_url):
    """
    Те ж що make_permalink, тільки для url картинки.
    Повертає url картинки без префікса.
    """
    pass  # todo make it
