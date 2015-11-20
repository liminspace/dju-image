# coding=utf-8


def remove_old_tmp_files(dirs, expiration_days=(7 * 24), recursive=True):
    """
    Видаляє файли тимчасові файли старші за expiration_days.
    dirs - список шляхів (абсолютних) до папок, в котрих буде відбуватись пошук файлів.
    expiration_days - термін в днях, після якого файл має бути видалений
    """
    pass  # todo do it


# def remove_old_tmp_files(dirs, max_lifetime=(7 * 24), recursive=True):  # todo remove it
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
