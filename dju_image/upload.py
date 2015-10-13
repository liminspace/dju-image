# coding=utf-8
import copy
import glob
import hashlib
import os
import re
import datetime
from django.conf import settings
from django.utils.crypto import get_random_string
from dju_common.file import make_dirs_for_file_path
from dju_common.tools import dtstr_to_datetime, datetime_to_dtstr
from django.utils.translation import ugettext as _
from .image import image_get_format, is_image, adjust_image
from . import settings as dju_settings


_profile_configs_cache = {}


def get_profile_configs(profile=None, use_cache=True):
    """
    Return upload configs for profile.
    """
    if use_cache and profile in _profile_configs_cache:
        return _profile_configs_cache[profile]
    profile_conf = None
    if profile is not None:
        try:
            profile_conf = dju_settings.DJU_IMG_UPLOAD_PROFILES[profile]
        except KeyError:
            if profile != 'default':
                raise ValueError(_('Unknown profile "%s".') % profile)
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
    Generate filename.
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
    Повертає шлях до файлу відносно MEDIA_URL.
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


# def add_tmp_prefix_to_filename(filename):
#     """ Додає префікс тимчасового файлу до імені файлу. """
#     if not filename.startswith(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):
#         filename = dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX + filename
#     return filename


# def add_thumb_suffix_to_filename(filename, label=None):
#     """ Додає суфікс мініатюри до імені файла. Якщо суфікс вже є, тоді буде помилка ValueError. """
#     return add_ending_to_filename(filename, '{}{}'.format(dju_settings.DJU_IMG_UPLOAD_THUMB_SUFFIX, label or ''))


# def add_ending_to_filename(filename, ending):
#     """ Додає закінчення до імені файла. Якщо ім'я файлу має суфікс thumb, тоді буде помилка ValueError. """
#     if dju_settings.DJU_IMG_UPLOAD_THUMB_SUFFIX in filename:
#         raise ValueError('Arg filename has thumb suffix "{suffix}": {fn}'.format(
#             suffix=dju_settings.DJU_IMG_UPLOAD_THUMB_SUFFIX, fn=filename
#         ))
#     ending = re.sub(r'[^a-z0-9_\-]', '', ending, flags=re.I)[:60]
#     if ending:
#         if not ending.startswith('_'):
#             ending = '_' + ending
#         fn, ext = os.path.splitext(filename)
#         filename = '{fn}{ending}{ext}'.format(fn=fn, ending=ending, ext=ext)
#     return filename


# def get_subdir_for_filename(filename, default='other'):
#     """ Повертає назву підпапки для файлу (dtstr[-2:]). """
#     if filename.startswith(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):
#         filename = filename[len(dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX):]
#     m = re.match(r'^([a-z0-9]+?)_.+', filename)
#     if m:
#         return m.group(1)[-2:]
#     return default


# def get_filepath_of_url(url):
#     """ Повертає шлях до файлу MEDIA по URL-адресі. """
#     if url.startswith(settings.MEDIA_URL):
#         url = url[len(settings.MEDIA_URL):]
#     fn = os.path.join(settings.MEDIA_ROOT, os.path.normpath(url)).replace('\\', '/')
#     return fn


# def make_thumb_url(url, label=None, ext=None):
#     """
#     Генерує URL до мініатюри з URL основної картинки, label мініатюри та розширення.
#     Якщо URL вже є на мініатюру, тоді повертає None.
#     """
#     path, filename = os.path.split(url)
#     try:
#         filename = add_thumb_suffix_to_filename(filename, label=label)
#     except ValueError:
#         return None
#     if ext:
#         if not ext.startswith('.'):
#             ext = '.' + ext
#         filename = os.path.splitext(filename)[0] + ext
#     return os.path.join(path, filename).replace('\\', '/')


def get_variant_label(v_conf):
    """
    Генерує назву для мініатюри на основі налаштувань (розмірів мініатюри)
    """
    if v_conf['MAX_SIZE'][0] is None:
        return 'h{}'.format(v_conf['MAX_SIZE'][1])
    if v_conf['MAX_SIZE'][1] is None:
        return 'w{}'.format(v_conf['MAX_SIZE'][0])
    return '{}x{}'.format(*v_conf['MAX_SIZE'])


# def remove_file_by_url(url, with_thumbs=True):
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


# def get_thumbs_for_image(filepath, label=None):
#     """
#     Повертає список шляхів на мініатюри для файлу filepath.
#     Якщо переданий label, тоді буде додаткове відсіювання.
#     """
#     dir_path, filename = os.path.split(os.path.abspath(filepath))
#     name = add_thumb_suffix_to_filename(os.path.splitext(filename)[0], label=label)
#     pattern = os.path.join(dir_path, name).replace('\\', '/') + '*.*'
#     return [fn.replace('\\', '/') for fn in glob.iglob(pattern)
#             if os.path.splitext(fn)[1].lstrip('.').lower() in dju_settings.DJU_IMG_UPLOAD_IMG_EXTS]


# def move_to_permalink(url, with_thumbs=True):
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


def save_file(f, full_path):
    """
    Збереження файлу.
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


# def remove_old_tmp_files(dirs, max_lifetime=(7 * 24), recursive=True):
#     """
#     Видалення старих тимчасових файлів.
#     Запускати функцію періодично раз на добу або рідше.
#     dirs -- список шляхів до папок, в яких треба зробити чистку (шлях має бути абсолютний)
#     max_lifetime -- час життя файлу, в годинах.
#     Запуск в консолі:
#     # python manage.py shell
#     > from dj_utils.upload import remove_old_tmp_files
#     > remove_old_tmp_files(['images'], (4 * 24))
#     """
#     def get_files_recursive(path):
#         for w_root, w_dirs, w_files in os.walk(path):
#             for w_file in w_files:
#                 yield os.path.join(w_root, w_file).replace('\\', '/')
#
#     def get_files(path):
#         pattern = os.path.join(path, dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX + '*').replace('\\', '/')
#         for filepath in glob.iglob(pattern):
#             if os.path.isfile(filepath):
#                 yield filepath
#
#     old_dt = datetime.datetime.utcnow() - datetime.timedelta(hours=max_lifetime)
#     r = re.compile(
#         r"^%s(?P<dtstr>[a-z0-9]+?)_[a-z0-9]+?(?:_.+?)?\.[a-z0-9]{1,8}$" % dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX,
#         re.I
#     )
#     find_files = get_files_recursive if recursive else get_files
#     total = removed = 0
#     for dir_path in dirs:
#         if not os.path.isdir(dir_path):
#             continue
#         for fn_path in find_files(dir_path):
#             m = r.match(os.path.basename(fn_path))
#             if not m:
#                 continue
#             total += 1
#             fdt = dtstr_to_datetime(m.group('dtstr'))
#             if fdt and old_dt > fdt:
#                 os.remove(fn_path)
#                 removed += 1
#     return removed, total


# def remake_thumbs(profiles, clean=True):
#     """
#     Перестворює мініатюри для картинок згідно налаштувань.
#     profiles - список з профілями, для яких треба застосувати дану функцію.
#     clean - чи потрібно перед створення видалити ВСІ мініатюри для вказаних профілів.
#     """
#     def get_files_recursive(path):
#         for w_root, w_dirs, w_files in os.walk(path):
#             for w_file in w_files:
#                 yield os.path.join(w_root, w_file).replace('\\', '/')
#
#     removed = created = 0
#     for profile in profiles:
#         conf = get_profile_configs(profile)
#         profile_path = os.path.join(settings.MEDIA_ROOT, dju_settings.DJU_IMG_UPLOAD_SUBDIR,
#                                     conf['PATH']).replace('\\', '/')
#         if clean:
#             for fn in get_files_recursive(profile_path):
#                 if dju_settings.DJU_IMG_UPLOAD_THUMB_SUFFIX in os.path.basename(fn):
#                     os.remove(fn)
#                     removed += 1
#         for fn in get_files_recursive(profile_path):
#             filename = os.path.basename(fn)
#             if dju_settings.DJU_IMG_UPLOAD_THUMB_SUFFIX in filename:
#                 continue  # пропускаємо файли, які мають суфікс мініатюри
#             with open(fn, 'rb') as f:
#                 if not is_image(f, types=conf['TYPES']):
#                     continue
#                 for tn_conf in conf['THUMBNAILS']:
#                     tn_f = adjust_image(f, max_size=tn_conf['MAX_SIZE'], new_format=tn_conf['FORMAT'],
#                                         jpeg_quality=tn_conf['JPEG_QUALITY'], fill=tn_conf['FILL'],
#                                         stretch=tn_conf['STRETCH'], return_new_image=True)
#                     tn_fn = os.path.splitext(filename)[0] + '.' + image_get_format(tn_f)
#                     tn_fn = add_thumb_suffix_to_filename(tn_fn, tn_conf['LABEL'] or gen_thumb_label(tn_conf))
#                     save_file(tn_f, tn_fn, conf['PATH'])
#                     created += 1
#     return removed, created
