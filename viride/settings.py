from datetime import timedelta
import os
from pathlib import Path

# added for bootstrap breadcrumbs -> fix error with smart_text
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.postgres',
    # 'django.contrib.sites',
    'common',
    'search',
    'index',
    'catalog',
    'plants',
    'pricelist',
    'contacts',
    'images',
    'conifers',
    'deciduous',
    'fruits',
    'roses',
    'perennials',
    'other',
    'profiles',
    'favorites',
    'django_ckeditor_5',
    # 'smart_selects',
    'django_db_logger',
    'compressor',
    'easy_thumbnails',
    'adminsortable2',
    'file_resubmit',
    'axes',
    'carts',
    'orders',
    'solo',
    # 'phonenumber_field',
    'django_recaptcha',
    # 'django_select2',
    'pure_pagination',
    'django_bootstrap_breadcrumbs',
    'markdownify.apps.MarkdownifyConfig',
    'django_cleanup.apps.CleanupConfig',
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'viride.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'common.context_processors.main',
            ],
        },
    },
]

WSGI_APPLICATION = 'viride.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# COMPRESS_ROOT = STATIC_ROOT

COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter',]


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USE_DJANGO_JQUERY = True
# JQUERY_URL = True
# SELECT2_CACHE_BACKEND = "select2"

CODEMIRROR_PATH = "codemirror"
CODEMIRROR_MODE = "htmlmixed"

MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            'a',
            'abbr',
            'acronym',
            'b',
            'blockquote',
            'em',
            'i',
            'li',
            'ol',
            'p',
            'strong',
            'ul',
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
        ],
        "WHITELIST_ATTRS": [
            'href',
            'src',
            'alt',
            'title',
            'rel',
        ]
    }
}

THUMBNAIL_BASEDIR = 'i'
# THUMBNAIL_SUBDIR = 'thumbs'
# THUMBNAIL_QUALITY = 95
THUMBNAIL_DEBUG = False
THUMBNAIL_PRESERVE_EXTENSIONS = ('png', 'gif')
# THUMBNAIL_NAMER = 'easy_thumbnails.namers.hashed'
THUMBNAIL_HIGHRES_INFIX = '@2x'

THUMBNAIL_ALIASES = {
    '': {
        # '360w_poor': {'crop': 'smart', 'size': (360, 360), 'quality': 10, 'bw': True},
        # '360w': {'crop': 'smart', 'size': (360, 360), 'quality': 95, },

        # '720w_poor': {'crop': 'smart', 'size': (720, 720), 'quality': 10, 'bw': True},
        # '720w': {'crop': 'smart', 'size': (720, 720), 'quality': 95, },

        # '1080w_poor': {'crop': 'smart', 'size': (1080, 1080), 'quality': 10, 'bw': True},
        # '1080w': {'crop': 'smart', 'size': (1080, 1080), 'quality': 95, },

        # '1920w_poor': {'crop': 'scale', 'size': (1920, 1920), 'quality': 10, 'bw': True},
        # '1920w': {'crop': 'scale', 'size': (1920, 1920), 'quality': 95, },

        'list': {'crop': ',0', 'size': (270, 320)},

        'detail_thumbnail': {'crop': ',0', 'size': (60, 60)},
        
        'detail': {'crop': 'scale', 'size': (720, 720)},

        # '90w': {'crop': 'scale', 'size': (90, 90), 'quality': 95, },

        # '360w_poor': {'crop': 'scale', 'size': (360, 360), 'quality': 10, 'bw': True},
        # '360w': {'crop': 'scale', 'size': (360, 360), 'quality': 95, },

        # '540w_poor': {'crop': 'scale', 'size': (540, 540), 'quality': 10, 'bw': True},
        # '540w': {'crop': 'scale', 'size': (540, 540), 'quality': 95, },

        # '720w_poor': {'crop': 'scale', 'size': (720, 720), 'quality': 10, 'bw': True},
        # '720w': {'crop': 'scale', 'size': (720, 720), 'quality': 95, },

        # '1080w_poor': {'crop': 'scale', 'size': (1080, 1080), 'quality': 10, 'bw': True},
        # '1080w': {'crop': 'scale', 'size': (1080, 1080), 'quality': 95, },
    }
}


SESSION_COOKIE_AGE = 15778463
SESSION_SAVE_EVERY_REQUEST = True

AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=5)
AXES_LOCKOUT_TEMPLATE = 'axes/lockout.html'
# AXES_USERNAME_FORM_FIELD = 'email'
AXES_ONLY_ADMIN_SITE = True


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 1,
    # 'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}


LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_SIGNUP_FORM_CLASS = 'common.forms.RecaptchaSignupForm'
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_ADAPTER = 'profiles.allauth.adapters.NoUsernameAccountAdapter'
ACCOUNT_USERNAME_BLACKLIST = [
    'administrator',
    'account',
    'support',
    'profile',
    'user',
    'test',
]
ACCOUNT_FORMS = {
    'signup': 'profiles.allauth.forms.RecaptchaSignupForm',
    'login': 'profiles.allauth.forms.CustomLoginForm',
    'change_password': 'profiles.allauth.forms.CustomChangePasswordForm',
    'set_password': 'profiles.allauth.forms.CustomSetPasswordForm',
    'reset_password': 'profiles.allauth.forms.RecaptchaResetPasswordForm',
}

CKEDITOR_5_FILE_STORAGE = 'common.storages.CkeditorCustomStorage'
CKEDITOR_5_CONFIGS = {
    'default': {
        # 'toolbar': ['undo', 'redo', '|', 'heading', '|', 'bold', 'italic', 'link',
        #             'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'toolbar': ['undo', 'redo', '|', 'paragraph', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'superscript', 'subscript', 'sourceEditing', 'specialCharacters',],
        'language': 'ru',
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    },
}

if os.environ.get("DEBUG"):
    try:
        from viride.settings_docker import *
    except ImportError:
        raise ImportError("Couldn't import settings_docker.py")
else:
    try:
        from viride.settings_local import *
    except ImportError:
        raise ImportError("Couldn't import settings_local.py")
