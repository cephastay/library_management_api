from datetime import timedelta
from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    'SECRET_KEY'
)

# Determine the environment (default is development)
ENVIRONMENT = config('ENVIRONMENT', default='development')

DEBUG = config(f'DEBUG_{ENVIRONMENT.upper()}', default=False, cast=bool)

# Configure ALLOWED_HOSTS based on environment
if ENVIRONMENT == 'production':
    ALLOWED_HOSTS = config('ALLOWED_HOSTS_PRODUCTION', cast=Csv())
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS_DEVELOPMENT', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'accounts',
    'api',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'drf_yasg'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'LMS.urls'

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

WSGI_APPLICATION = 'LMS.wsgi.application'

# Determine if using SQL DataBase
SQL_Database = config('MySQL', default=False, cast= bool)

# Database configuration based on environment
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': config('DATABASE_PRODUCTION', cast=db_url)
    }
    if SQL_Database:
        DATABASES['default']['OPTIONS'] = {
            'sql_mode': 'STRICT_TRANS_TABLES',
            }
else:
    DATABASES = {
        'default': config('DATABASE_DEVELOPMENT', cast=db_url)
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIR = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "static/staticfiles"


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'EXCEPTION_HANDLER': 'utils.exceptionhandler.customexceptionhandler',

}

# JWT settings
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Token',),
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=4),
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
}

#swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        # Basic Authentication
        'Basic': {
            'type': 'basic',  
        },
        # Bearer Token Authentication (JWT)
        'Bearer': {
            'type': 'apiKey',  
            'name': 'Authorization',  
            'in': 'header',  
            'description': 'JWT token for user authentication',  
        },
        # Token Authentication (DRF token authentication)
        'Token': {
            'type': 'apiKey', 
            'name': 'Authorization', 
            'in': 'header',  
            'description': 'Token for user authentication',  
        }
    },    
}

# Added security settings for mock project
    # ONLY USE IN DEPLOYMENT
if ENVIRONMENT == 'production':  
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True  
    SECURE_HSTS_PRELOAD = True  
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 