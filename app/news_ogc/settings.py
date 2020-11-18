"""
Django settings for wbm_viz project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'unsafe-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', "True") == "True"

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

# People who get error notification emails
ADMINS = [('Daniel Vignoles', 'dvignoles@gc.cuny.edu'), ]

INTERNAL_IPS = [
    '127.0.0.1',
]

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'leaflet',
    'bootstrap4',
    'crispy_forms',
    'bootstrap_datepicker_plus',
    'news_ogc'
]

BOOTSTRAP4 = {
    'include_jquery': True,
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# https://pypi.org/project/django-leaflet
LEAFLET_CONFIG = {
    'PLUGINS': {
        'leaflet-pip': {
            #https://github.com/mapbox/leaflet-pip : Point in Polygon functionality
            'js': 'https://unpkg.com/@mapbox/leaflet-pip@1.1.0/leaflet-pip.js',
            'auto-include': True,
        },
        'leaflet-timedimension': {
            'js': 'https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.min.js',
            'css': 'https://cdn.jsdelivr.net/npm/leaflet-timedimension@1.1.1/dist/leaflet.timedimension.control.min.css',
            'auto-include': True,
        },
        'leaflet-sidebar-v2': {
            'js': 'https://cdn.jsdelivr.net/npm/leaflet-sidebar-v2@3.2.3/js/leaflet-sidebar.min.js',
            'css': 'https://cdn.jsdelivr.net/npm/leaflet-sidebar-v2@3.2.3/css/leaflet-sidebar.min.css',
            'auto-include': True,
        },
        'leaflet-draw': {
            'js': "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.js",
            'css': "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.css",
            'auto-include': True
        },
        'leaflet-spin': {
            'js': 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.Spin/1.1.2/leaflet.spin.min.js',
            'auto-include': True
        }
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news_ogc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'news_ogc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': os.environ.get('DB_HOST', None),
        'PORT': os.environ.get('DB_PORT', None),
        'NAME': 'news_ogc',
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'TEST': {
            'DEPENDENCIES': [],
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'lax'
