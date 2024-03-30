import os

def str2bool(s):
    if s in ('1', 'True'):
        return True
    elif s in ('0', 'False'):
        return False
    else:
        raise ValueError("Cannot covert {} to a bool".format(s))
    
def str2admins(s):
    lst_str = s.split(',')
    lst_lst = []
    for val in lst_str:
        tmp = val.strip().split(' ')
        if isinstance(tmp, list) and len(tmp) == 2:
            lst_lst.append(tmp)
    return lst_lst

DEBUG = str2bool(os.environ.get("DEBUG"))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
SECRET_KEY = os.environ.get("SECRET_KEY")


ADMINS = str2admins(os.environ.get('ADMINS'))
LIST_OF_EMAIL_RECIPIENTS = os.environ.get("EMAIL_RECIPIENTS").split(" ")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")  # str comming, maybe need num
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER

COMPRESS_ENABLED = True

RECAPTCHA_PUBLIC_KEY = os.environ.get("SITE_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("SECRET_KEY")


# CACHE_BACKEND = 'django.core.cache.backends.dummy.DummyCache'
# CACHE_BACKEND = 'django.core.cache.backends.memcached.PyMemcacheCache'
# CACHE_BACKEND = 'django.core.cache.backends.locmem.LocMemCache'

CACHE_TIMEOUT = os.environ.get("CACHE_TIMEOUT")
CACHE_LOCATION = os.environ.get("CACHE_LOCATION")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        # 'LOCATION': 'default',
        'LOCATION': CACHE_LOCATION,
        'TIMEOUT': CACHE_TIMEOUT,
        # 'OPTIONS': {
        #     'MAX_ENTRIES': 3000,
        # }
    },
    'axes': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        # 'LOCATION': 'axes',
        'LOCATION': CACHE_LOCATION,
        'TIMEOUT': CACHE_TIMEOUT,
    },
    'file_resubmit': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/file_resubmit/',
        'TIMEOUT': 3600,
    },
    'sitemap': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/sitemap/',
        'TIMEOUT': 86400 if int(CACHE_TIMEOUT) > 0 else 0,
    },
}

DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = 30
DJANGO_DB_LOGGER_ENABLE_FORMATTER = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # 'logfile': {
        #     'level': 'INFO',
        #     "class": "logging.FileHandler",
        #     'filename': os.path.join(BASE_DIR, 'log', 'django.log'),
        # },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': [],
            'propagate': False,
        },
        'db': {
            'handlers': ['db_log', 'console', 'mail_admins'],
            'level': 'DEBUG'
        },
        'django.request': {  # logging 500 errors to database
            'handlers': ['db_log', 'console', 'mail_admins',],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
