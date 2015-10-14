"""
Django settings for hotspot project.

"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bv_%&gouv8t(ns-qu^1-mlcmmf==q#l5_i8q)ybnweh&bhjukz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SERVE_STATIC_WITH_DJANGO = False

# Use SSL redirects (courtesy of django-ssl-redirect)
if DEBUG:
    SSL_ON = False
else:
    SSL_ON = True

# Force loading of analytics even when DEBUG=True
# normally false because we dont want to analytics to track hits while developing
DEBUG_USERVOICE = True
DEBUG_ANALYTICS = True

TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# use admin interface provided by Xadmin instead of default one
USE_XADMIN = True

ADMINS = (
     ('Nick Sweeting', 'nikisweeting+django@gmail.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ["hotspot.nicksweeting.com", "localhost"]

# Application definition

INSTALLED_APPS = (
    # Django Defaults
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin Apps,
    'django.contrib.admin',
    'xadmin',
    'crispy_forms',

    # Docs
    'django.contrib.admindocs',    # using sphinx instead
    'django_extensions',            # generate graphviz diagrams using ./manage.py graph_models -a -g > docs/full.dot

    # Debugging
    'debug_toolbar',
    'werkzeug_debugger_runserver',

    # Auth Apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # DB Migrations
    'south',

    # APIs
    'hotspot.api',
    'hotspot.public-api',
    'hotspot.legacy-api',
    'rest_framework',

    # View-Handling Apps
    'hotspot.apps.web',
    'hotspot.apps.dashboard',
)

MIDDLEWARE_CLASSES = [
    'ssl_redirect.middleware.SSLRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Debug toolbar
def show_toolbar(request):
    return request.user.is_superuser

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'hotspot.settings.show_toolbar',
}


ROOT_URLCONF = 'hotspot.urls'
WSGI_APPLICATION = 'hotspot.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'TIME-ZONE':'PST',
        'NAME':'django-hotspot',
        'USER':'root',
        'PASSWORD':'XxxxxXXxXxx',
    }
}
if DEBUG:
    DATABASES['default']['HOST'] = 'localhost'


# Graphviz graphing
GRAPH_MODELS = {
  'all_applications': False,
  'group_models': False,
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_DOC_ROOT = os.path.join(BASE_DIR, "static/docs")
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

# Analytics
SEGMENT_ANALYTICS_KEY = "1qkc7byfcl"

# Django User model
AUTH_USER_MODEL = "api.User"

# REST API Settings
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'django.contrib.auth,
    # ]
}


### Allauth settings
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",

    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    "hotspot.context_processors.analytics",
)

AUTHENTICATION_BACKENDS = (
    "hotspot.auth_backend.OAuthTokenBackend",
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk' # instead of 'oauth2'
    }
}
