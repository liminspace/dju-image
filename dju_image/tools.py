# coding=utf-8
import glob
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
    'unknown_profile': ugettext_lazy('Unknown profile "%(profile)s".'),
    'filename_hasnt_tmp_prefix': ugettext_lazy('Filename "%(filename)s" has not temporary prefix.'),
}

HASH_SIZE = 10


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


def get_hash(name, variant_label=None):
    # name must be without label, for example 'uniqname_rand'
    h = hashlib.sha1(name + (variant_label or '') + dju_settings.DJU_IMG_UPLOAD_KEY).hexdigest()
    return h[:HASH_SIZE]


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
    name = '{name}{status_suffix}{hash}'.format(
        name=name,
        status_suffix=status_suffix,
        hash=get_hash('_'.join(name_parts[:2]), variant_label=variant_label)
    )
    if variant_label:
        name += '_' + variant_label
    if ext:
        file_ext = ext
    elif variant_label:
        for var_conf in conf['VARIANTS']:
            var_conf_label = var_conf['LABEL'] or get_variant_label(var_conf)
            if var_conf_label == variant_label:
                if var_conf['FORMAT']:
                    file_ext = var_conf['FORMAT'].lower()
                break
    if file_ext and not file_ext.startswith('.'):
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


variant_hash_label_re = re.compile(r'^.+?{suf}([a-z0-9]{{hs}})_(.+?)(?:|\.[A-Za-z]{3,4})$'.replace(
    '{suf}', dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX
).replace(
    '{hs}', str(HASH_SIZE)
))


def get_files_by_img_id(img_id, check_hash=True):
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
    Якщо check_hash=True, тоді файли з невірним хешем будуть ігноруватись.
    Якщо файл не існує, тоді поверає None.
    Пошук варіантів відбуваться в файловій системі не залежно від налаштувань.
    """
    main_rel_path = get_relative_path_from_img_id(img_id)
    main_path = os.path.join(settings.MEDIA_ROOT, main_rel_path).replace('\\', '/')
    if not os.path.isfile(main_path):
        return None
    filename = os.path.basename(main_rel_path)
    name_left_part = filename.split(dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX, 1)[0]
    img_name = name_left_part
    if img_name.startswith(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):
        img_name = img_name[len(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):]
    img_name_parts = img_name.split('_', 2)
    img_name = '_'.join(img_name_parts[:2])
    search_pattern = name_left_part + dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX + '*'
    search_dir = os.path.dirname(main_path)
    variants = {}
    for var_path in glob.iglob(os.path.join(search_dir, search_pattern.replace('\\', '/'))):
        var_filename = os.path.basename(var_path)
        m = variant_hash_label_re.match(var_filename)
        if not m:
            continue
        var_hash, var_label = m.groups()
        if check_hash and var_hash != get_hash(img_name, var_label):
            continue
        variants[var_label] = os.path.relpath(var_path, settings.MEDIA_ROOT)
    return {
        'main': main_rel_path,
        'variants': variants,
    }


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


def remove_tmp_prefix_from_filename(filename):
    """
    Remove tmp prefix from filename.
    """
    if not filename.startswith(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):
        raise RuntimeError(ERROR_MESSAGES['filename_hasnt_tmp_prefix'] % {'filename': filename})
    return filename[len(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):]


def remove_tmp_prefix_from_file_path(file_path):
    """
    Remove tmp prefix from file path or url.
    """
    path, filename = os.path.split(file_path)
    return os.path.join(path, remove_tmp_prefix_from_filename(filename)).replace('\\', '/')


def make_permalink(img_id):
    """
    Removes tmp prefix from filename and rename main and variant files.
    Returns img_id without tmp prefix.
    """
    profile, filename = img_id.split(':', 1)
    new_img_id = profile + ':' + remove_tmp_prefix_from_filename(filename)
    urls = get_files_by_img_id(img_id)
    move_list = {(urls['main'], remove_tmp_prefix_from_file_path(urls['main']))}
    for var_label, var_file_path in urls['variants'].iteritems():
        move_list.add((var_file_path, remove_tmp_prefix_from_file_path(var_file_path)))
    for file_path_from, file_path_to in move_list:
        os.rename(
            os.path.join(settings.MEDIA_ROOT, file_path_from).replace('\\', '/'),
            os.path.join(settings.MEDIA_ROOT, file_path_to).replace('\\', '/'),
        )
    return new_img_id


def make_permalink_by_img_url(img_url):
    """
    Те ж що make_permalink, тільки для url картинки.
    Повертає url картинки без префікса.
    """
    pass  # todo do it
