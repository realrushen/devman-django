from where_to_go.settings.common import *

DEBUG = True

SECRET_KEY = 'django-insecure-9bu(j)x@32x&e&0(gq*eto^=(+fqa%ith+se#1k40#%^)t&l5c'

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
