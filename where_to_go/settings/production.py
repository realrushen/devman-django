import environs

from where_to_go.settings.common import *

env = environs.Env()
env.read_env(str(BASE_DIR / '.env'))

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

STATIC_ROOT = BASE_DIR / 'static'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# HTTP Strict Transport Security settings
SECURE_HSTS_SECONDS = 1
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

