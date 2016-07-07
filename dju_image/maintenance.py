# coding=utf-8
import os
import re
import datetime
from django.conf import settings
from dju_common.tools import dtstr_to_datetime
from .image import adjust_image, image_get_format
from .tools import get_profile_configs, get_variant_label, get_relative_path_from_img_id, media_path, save_file
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


def remake_images_variants(profiles, clear=True):
    """
    Перестворює варіанти для картинок згідно налаштувань.
    profiles - список профілів, для картинок яких треба перестворити варіанти.
    clear - якщо True, тоді перед створенням варіантів будуть видалені ВСІ попередні варіанти.
    """
    assert isinstance(profiles, (list, tuple)) or profiles is None
    if profiles is None:
        profiles = dju_settings.DJU_IMG_UPLOAD_PROFILES.keys()
    profiles = set(('default',) + tuple(profiles))
    removed = remade = 0
    for profile in profiles:
        conf = get_profile_configs(profile=profile)
        root_path = os.path.join(settings.MEDIA_ROOT, dju_settings.DJU_IMG_UPLOAD_SUBDIR, conf['PATH'])
        if clear:
            for fn in get_files_recursive(root_path):
                if dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX in os.path.basename(fn):
                    os.remove(fn)
                    removed += 1
        for fn in get_files_recursive(root_path):
            filename = os.path.basename(fn)
            if dju_settings.DJU_IMG_UPLOAD_VARIANT_SUFFIX in filename:
                continue
            if dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX not in filename:
                continue
            img_id = '{profile}:{name}'.format(
                profile=profile,
                name=filename[:filename.find(dju_settings.DJU_IMG_UPLOAD_MAIN_SUFFIX)]
            )
            with open(fn, 'rb') as f:
                for v_conf in conf['VARIANTS']:
                    label = v_conf['LABEL']
                    if not label:
                        label = get_variant_label(v_conf)
                    v_f = adjust_image(f, max_size=v_conf['MAX_SIZE'], new_format=v_conf['FORMAT'],
                                       jpeg_quality=v_conf['JPEG_QUALITY'], fill=v_conf['FILL'],
                                       stretch=v_conf['STRETCH'], return_new_image=True)
                    v_relative_path = get_relative_path_from_img_id(img_id, variant_label=label,
                                                                    ext=image_get_format(v_f))
                    v_full_path = media_path(v_relative_path)
                    save_file(v_f, v_full_path)
                    remade += 1
    return removed, remade


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
