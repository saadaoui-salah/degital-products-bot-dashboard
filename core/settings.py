from pathlib import Path
import os

JAZZMIN_SETTINGS = {
    "site_title": "DPS Gross Bot",
    "site_header": "DPS Gross Bot",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "DPS Gross Bot",

    "welcome_sign": "Welcome to DPS Gross Bot Dashboard",

    # Copyright on the footer
    "copyright": "Salah Saadaoui | salahsaadaoui8@gmail.com",

}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1$5ey=2do4^%*pxpt5pc-$n-5mydwx_i&&kc5gsh^(77g^j-or'

DEBUG = True

ALLOWED_HOSTS = ["*"]



INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.md.HeaderCheckMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],  # Set to the host where your PostgreSQL server is running
        'PORT': '20936',      # Set to the port your PostgreSQL server is listening on
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CSRF_TRUSTED_ORIGINS = [
    "https://stale-connection-production.up.railway.app",
]

LANGUAGE_CODE = 'en-us'
STATIC_ROOT = 'admin'
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
