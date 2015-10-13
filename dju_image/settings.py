from django.conf import settings


# ------------
# IMAGE UPLOAD
# ------------
# path that relatively MEDIA. For example: 'dir' or 'dir1/dir2' (without slashes in edges!)
DJU_IMG_UPLOAD_SUBDIR = getattr(settings, 'DJU_IMG_UPLOAD_SUBDIR', 'upload-img')
# key for generate hash
DJU_IMG_UPLOAD_KEY = getattr(settings, 'DJU_IMG_UPLOAD_KEY', '00000000000000000000000000000000')

# default profile (other profiles will extend from this if they won't set some parameters)
DJU_IMG_UPLOAD_PROFILE_DEFAULT = {
    'PATH': 'common',                 # subdir in DJU_IMG_UPLOAD_SUBDIR ('dir', 'dir1/dir2') (without slashes in edges!)
    'TYPES': ('GIF', 'JPEG', 'PNG'),  # allow formats
    'MAX_SIZE': (800, 800),           # max size (width, height). can has one None value (auto)
    'FILL': False,                    # image must be filled with cropping, otherwise it will be inscribed
    'STRETCH': False,                 # stretch when the image is too small
    'FORMAT': None,                   # format to save (if None then it will be saved in original format)
    'JPEG_QUALITY': 95,               # JPEG quality
    'VARIANTS': [],                   # variants settings list
}

# default variant settings
DJU_IMG_UPLOAD_PROFILE_VARIANT_DEFAULT = {
    'LABEL': None,                    # name. if None then name will be auto generated: '50x60' or 'w50' or 'h60'
    'MAX_SIZE': (160, 160),
    'FILL': True,
    'STRETCH': True,
    'FORMAT': None,
    'JPEG_QUALITY': 90,
}

# profiles
# for example:
# DJU_IMG_UPLOAD_PROFILES = {
#     'avatar': {
#         'PATH': 'avatars',
#         'MAX_SIZE': (400, None),
#         'VARIANTS': [
#             {'MAX_SIZE': (30, 30), 'LABEL': 'mini', 'FORMAT': 'PNG'},
#             {'MAX_SIZE': (200, None), 'JPEG_QUALITY': 85},
#         ],
#     },
# }
DJU_IMG_UPLOAD_PROFILES = getattr(settings, 'DJU_IMG_UPLOAD_PROFILES', {})


DJU_IMG_UPLOAD_MAX_FILES = getattr(settings, 'DJU_IMG_UPLOAD_MAX_FILES', 3)  # max uploaded files

# system settings (don't change its)
DJU_IMG_UPLOAD_TMP_PREFIX = getattr(settings, 'DJU_IMG_UPLOAD_TMP_PREFIX', '__t_')
DJU_IMG_UPLOAD_MAIN_SUFFIX = getattr(settings, 'DJU_IMG_UPLOAD_MAIN_SUFFIX', '__m_')
DJU_IMG_UPLOAD_VARIANT_SUFFIX = getattr(settings, 'DJU_IMG_UPLOAD_VARIANT_SUFFIX', '__v_')
DJU_IMG_UPLOAD_IMG_EXTS = ('jpeg', 'jpg', 'png', 'gif')  # supports image extensions

DJU_IMG_USE_JPEGTRAN = getattr(settings, 'DJU_IMG_USE_JPEGTRAN', False)  # use jpegtran util (only Linux)
# use convert util (ImageMagick) (only Linux)
DJU_IMG_CONVERT_JPEG_TO_RGB = getattr(settings, 'DJU_IMG_CONVERT_JPEG_TO_RGB', False)


# ------------
# FILESYSTEM PERMISSIONS
# ------------
DJU_IMG_CHMOD_DIR = getattr(settings, 'DJU_IMG_CHMOD_DIR', 0o775)    # permissions for new dirs
DJU_IMG_CHMOD_FILE = getattr(settings, 'DJU_IMG_CHMOD_FILE', 0o664)  # permissions for new files


# ------------
# OTHER
# ------------
DJU_IMG_RW_FILE_BUFFER_SIZE = getattr(settings, 'DJU_IMG_RW_FILE_BUFFER_SIZE', 8192)  # buffer size for read/write files
