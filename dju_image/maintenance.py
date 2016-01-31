# coding=utf-8
import os
import re
import datetime
from django.conf import settings
from dju_common.tools import dtstr_to_datetime
from .tools import get_profile_configs
from . import settings as dju_settings


re_tmp = re.compile(r'^{pref}(?P<dtstr>[a-z0-9]{7,9})_[a-z0-9]{4}.*$'.replace(
    '{pref}', dju_settings.DJU_IMG_UPLOAD_TMP_PREFIX
))


def get_files_recursive(path):
    for root, dirs, files in os.walk(path):
        for fn in files:
            yield os.path.join(root, fn).replace('\\', '/')


def remove_old_tmp_files(profiles=None, max_lifetime=(7 * 24)):
    """
    Removes old temp files that is older than expiration_hours.
    If profiles is None then will be use all profiles.
    """
    assert isinstance(profiles, (list, tuple)) or profiles is None
    if profiles is None:
        profiles = dju_settings.DJU_IMG_UPLOAD_PROFILES.keys()
    profiles = set(('default',) + tuple(profiles))
    total = removed = 0
    old_dt = datetime.datetime.utcnow() - datetime.timedelta(hours=max_lifetime)
    for profile in profiles:
        conf = get_profile_configs(profile=profile)
        root_path = os.path.join(settings.MEDIA_ROOT, dju_settings.DJU_IMG_UPLOAD_SUBDIR, conf['PATH'])
        for file_path in get_files_recursive(root_path):
            m = re_tmp.match(os.path.basename(file_path))
            if m is None:
                continue
            total += 1
            fdt = dtstr_to_datetime(m.group('dtstr'))
            if fdt and old_dt > fdt:
                os.remove(file_path)
                removed += 1
    return removed, total


def remake_images_variants(profiles, clean=True):
    """
    Перестворює варіанти для картинок згідно налаштувань.
    profiles - список профілів, для картинок яких треба перестворити варіанти.
    clean - якщо True, тоді перед створенням варіантів будуть видалені ВСІ попередні варіанти.
    """
    pass  # todo do it


# def remake_thumbs(profiles, clean=True):  # todo remove it
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


def update_wrong_hashes():
    """
    Оновлює хеші в назвах файлів.
    Запускати після зміни ключа DJU_IMG_UPLOAD_KEY.
    """
    pass  # todo do it


def clean():
    """
    Видаляє файли, в яких невірний хеш та зайві варіанти.
    """
    pass  # todo do it
