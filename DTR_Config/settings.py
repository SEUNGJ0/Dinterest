import os
from .get_secret import get_secret
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'App_Auth', # 계정 관리
    'App_Boards', # 저장된 핀들을 보관하는 카테고리
    'App_Pins', # 유저들이 업로드하는 이미지들
    'App_Profiles', # 사용자 프로필 정보 관리
    # Installed Library
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt', # JWT
    'rest_framework_simplejwt.token_blacklist',

    'allauth', # django-allauth - 거의 대부분의 소셜 로그인을 지원하고 회원가입 기능을 제공.
    'allauth.account',
    'allauth.socialaccount'
]

#django-allauth
SITE_ID = 1                               # 해당 도메인의 id
ACCOUNT_UNIQUE_EMAIL = True               # User email unique 사용 여부
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # User username type
ACCOUNT_USERNAME_REQUIRED = False         # User username 필수 여부
ACCOUNT_EMAIL_REQUIRED = True             # User email 필수 여부
ACCOUNT_AUTHENTICATION_METHOD = 'email'   # 로그인 인증 수단
ACCOUNT_EMAIL_VERIFICATION = 'none'       # Email 인증 필수 여부


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # Pagination 클래스와 페이지 크기를 정의
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 
    'PAGE_SIZE': 10
}
REST_USE_JWT = True # JWT 사용 여부

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12), # Access Token의 유효기간 설정
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7), # Refresh Token의 유효기간 설정
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_USER_CLASS': 'App_Auth.User', 
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # allauth 미들웨어
]

ROOT_URLCONF = 'DTR_Config.urls'

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

WSGI_APPLICATION = 'DTR_Config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DB_NAME'),
        'USER': 'ksj',
        'PASSWORD': get_secret('MySQL_Password'),
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]

# Media files

MEDIA_URL = '/media/' # 파일을 브라우저로 서빙할 때 보여줄 가상의 URL, 보안을 위해 필요
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'
# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'App_Auth.User'
