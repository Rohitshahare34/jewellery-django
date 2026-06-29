import os
from pathlib import Path
from decouple import config

# --- Base directory setup ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security settings ---
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)


ALLOWED_HOSTS = ['aashutoshjewellers.in', 'www.aashutoshjewellers.in', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://aashutoshjewellers.in', 'https://www.aashutoshjewellers.in', 'http://aashutoshjewellers.in', 'http://www.aashutoshjewellers.in']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# --- Metal Price API Configuration ---
GOLD_API_KEY = config('GOLD_API_KEY', default='')
API_UPDATE_INTERVAL = config('API_UPDATE_INTERVAL', default=300, cast=int)

# --- Installed apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'shop',  # Your app
]

# --- Allauth settings ---
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Redirect URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Additional allauth settings for easier testing and seamless Google login
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Don't require username for signup
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False  # Don't ask for password twice
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True  # Auto-signup with social accounts
SOCIALACCOUNT_EMAIL_REQUIRED = True  # Email is required from social provider
SOCIALACCOUNT_QUERY_EMAIL = True  # Ask Google for email (already in scope)

# Social account provider settings (Google)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',  # Optional: let user choose Google account (remove for auto-login)
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': '222058147156-4tkmq42mb6ij82tdkun9cvm5hb8o7cgm.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
        }
    }
}

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# --- URL and WSGI ---
ROOT_URLCONF = 'aashutosh_jewelerys.urls'
WSGI_APPLICATION = 'aashutosh_jewelerys.wsgi.application'

# --- Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # optional if you add global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_context',
                'shop.context_processors.metal_prices_context',
                'shop.context_processors.popup_context',
                'shop.context_processors.wishlist_context',
            ],
        },
    },
]

# --- Database ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 30,  # 30 seconds busy timeout
        }
    }
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static and media files ---
STATIC_URL = '/static/'
# Let Django automatically discover static files inside each app and root static folder
STATICFILES_DIRS = [
    BASE_DIR / 'shop' / 'static',  # app's static folder
    BASE_DIR / 'static',  # root static folder
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # for production (collectstatic)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
