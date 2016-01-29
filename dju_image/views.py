# coding=utf-8
from django.conf import settings
from django.http import HttpResponseNotAllowed
from django.utils.translation import ugettext_lazy
from dju_common.http import send_json
from dju_image.image import image_get_format, adjust_image, is_image
from dju_image.tools import (get_profile_configs, save_file, generate_img_id,
                             get_relative_path_from_img_id, get_variant_label, media_path)
from dju_image import settings as dju_settings


ERROR_MESSAGES = {
    'no_uploaded_files': ugettext_lazy('Uploaded files not found.'),
    'wrong_file_format': ugettext_lazy('Format of uploaded file "%(name)s" is not allowed. '
                                       'Allowed formats is: %(formats)s.'),
    'wrong_profile': ugettext_lazy('')
}


def upload_image(request):
    """
    Вюха, яка зберігає завантажений файл.
    Структура запиту:
        FILES
            images[]: файли зображеннь
        POST DATA
            profile: назва профілю (для визначення налаштувань збреження) (опціонально)
            label: додаток до назви файлу при збереженні (опціонально)
    Структура відповіді:
        Тип відповіді: JSON
        {
            'uploaded': [
                {
                    'url': 'повний url до головного файла',
                    'rel_url': 'відносний від MEDIA url головного файла',
                    'img_id': 'ідентифікатор для збереження в БД',  // 'profilename:abcdef_abcd_label.png',
                    'variants': {
                        'variant label': {
                            'url': 'повний url до варіанта',
                            'rel_url': 'відносний від MEDIA url головного файла'
                        },
                        ...
                    }
                },
                ...
            ],
            'errors': ['error message', ...]
        }
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))
    result = {'uploaded': [], 'errors': []}
    files = request.FILES.getlist('images[]')
    if not files:
        result['errors'].append(unicode(ERROR_MESSAGES['no_uploaded_files']))
        return send_json(result)
    try:
        profile = request.POST.get('profile', 'default')
        conf = get_profile_configs(profile)
    except ValueError, e:
        result['errors'].append(unicode(e))
        return send_json(result)
    for i in xrange(min(len(files), dju_settings.DJU_IMG_UPLOAD_MAX_FILES)):
        f = files[i]
        if not is_image(f, types=conf['TYPES']):
            result['errors'].append(
                unicode(ERROR_MESSAGES['wrong_file_format']) %
                {'name': f.name, 'formats': ', '.join(map(lambda t: t.upper(), conf['TYPES']))}
            )
            continue
        adjust_image(f, max_size=conf['MAX_SIZE'], new_format=conf['FORMAT'],
                     jpeg_quality=conf['JPEG_QUALITY'], fill=conf['FILL'], stretch=conf['STRETCH'])
        img_id = generate_img_id(profile, ext=image_get_format(f),
                                 label=request.POST.get('label'), tmp=True)
        relative_path = get_relative_path_from_img_id(img_id)
        full_path = media_path(relative_path)
        save_file(f, full_path)
        data = {
            'url': settings.MEDIA_URL + relative_path,
            'rel_url': relative_path,
            'img_id': img_id,
            'variants': {},
        }
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
            data['variants'][label] = {
                'url': settings.MEDIA_URL + v_relative_path,
                'rel_url': v_relative_path,
            }
        result['uploaded'].append(data)
    return send_json(result)
