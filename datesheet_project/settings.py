"""
Django settings for datesheet_project project.

This configuration uses:
- SQLite locally (with real migrations).
- A dummy database and no migrations on Vercel, with sessions stored in cookies.
"""

import os
from pathlib import Path
from decouple import config

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect Vercel environment
VERCEL = os.environ.get("VERCEL") is not None

# SECURITY
# If you forget to set SECRET_KEY in .env or in Vercel env vars,
# this default will keep Django from crashing—but you MUST override
# it with a real secret in production.
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key')

# DEBUG: default off in Vercel, on locally if not set explicitly
DEBUG = config('DEBUG', default=not VERCEL, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    # Any LAN IPs you need
    ".vercel.app",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # sessions must stay enabled
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'datesheet_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',   # sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datesheet_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # adjust if needed
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

WSGI_APPLICATION = 'datesheet_project.wsgi.application'



# ---------------------
# DATABASE & SESSIONS
# ---------------------

if VERCEL:
    # 1) Dummy DB — no real connections allowed
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.dummy',
        }
    }
    # 2) Store sessions in signed cookies (no DB writes)
    SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
    # 3) Disable all migrations (skip the migration-check at startup)
    MIGRATION_MODULES = {
        app_label: None
        for app_label in [
            'admin',
            'auth',
            'contenttypes',
            'sessions',
            'messages',
            'staticfiles',
            'datesheet_app'
        ]
    }

else:
    # Local development: SQLite + normal migrations
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # Default session engine (DB-backed)
    # SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    # No need to define MIGRATION_MODULES here — use the defaults.




# ---------------------
# AUTH & PASSWORD VALIDATION
# ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ---------------------
# INTERNATIONALIZATION
# ---------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------
# STATIC FILES
# ---------------------
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
