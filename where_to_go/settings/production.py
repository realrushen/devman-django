import environs

from where_to_go.settings.common import *

env = environs.Env()
env.read_env(str(BASE_DIR / '.env'))

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

