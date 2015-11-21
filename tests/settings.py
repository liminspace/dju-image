import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'test'

DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

INSTALLED_APPS = (
    'dju_common',
    'dju_image',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tests.urls'

WSGI_APPLICATION = 'tests.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'dju',
        # 'USER': 'root',
        # 'PASSWORD': '',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

EMAIL_SUBJECT_PREFIX = '[Django test] '
EMAIL_RETURN_PATH = 'return.path@mail.com'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
            ),
        },
    },
]

DJU_IMG_USE_JPEGTRAN = True
DJU_IMG_CONVERT_JPEG_TO_RGB = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TMP_DIR = os.path.join(BASE_DIR, 'tmp')

DJU_IMG_UPLOAD_PROFILES = {
    'simple0': {
        'PATH': 's0',
        'MAX_SIZE': (120, 220),
        'VARIANTS': [
            {'MAX_SIZE': (20, 30), 'FORMAT': 'PNG'},
            {'MAX_SIZE': (20, None), 'FORMAT': 'GIF'},
            {'MAX_SIZE': (20, 30), 'FORMAT': 'JPEG', 'LABEL': 'lab0'},
        ],
    },
    'simple1': {
        'PATH': 's1',
        'MAX_SIZE': (100, 200),
        'VARIANTS': [
            {'MAX_SIZE': (20, 30)},
            {'MAX_SIZE': (20, None)},
            {'MAX_SIZE': (None, 30)},
            {'MAX_SIZE': (20, 30), 'LABEL': 'lab1'},
        ],
    },
}
