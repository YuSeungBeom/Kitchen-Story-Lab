from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sddtxr9v4(!2&8y_02imp7dov4wwjl&f%gd%90zz!0vr9qndrl'

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
    'blog',
    'accounts',
    'widget_tweaks',
    'tinymce',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'accounts.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'blog:post_list'
LOGIN_URL = 'accounts:login'
LOGOUT_REDIRECT_URL = 'blog:post_list'


TINYMCE_API_KEY = 'pypz0os5nocw3u5memwasz6cq8su53ar4dv5ksp9wep1hh80'
TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/pypz0os5nocw3u5memwasz6cq8su53ar4dv5ksp9wep1hh80/tinymce/6/tinymce.min.js'
TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {
    'api_key': 'pypz0os5nocw3u5memwasz6cq8su53ar4dv5ksp9wep1hh80',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        advlist autolink lists link image charmap preview anchor
        searchreplace visualblocks code fullscreen
        insertdatetime media table paste code help wordcount
    ''',
    'toolbar': '''
        undo redo | formatselect | bold italic backcolor | 
        alignleft aligncenter alignright alignjustify | 
        bullist numlist outdent indent | removeformat | 
        image media link | help
    ''',
    'menubar': 'file edit view insert format tools table help',
    'content_style': 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 16px; }',
    'browser_spellcheck': True,
    'contextmenu': 'link image',
    'removed_menuitems': 'newdocument',
    'paste_data_images': True,
    'image_advtab': True,
    'relative_urls': False,  # false -> False로 수정
    'remove_script_host': False,  # false -> False로 수정
    'referrer_policy': 'origin',
    'protect': [
        r'<!--[\s\S]*?-->',  # 이스케이프 시퀀스 수정
        r'<!\[CDATA\[[\s\S]*?\]\]>',  # 이스케이프 시퀀스 수정
        r'<script[\s\S]*?>'  # 이스케이프 시퀀스 수정
    ],
    'verify_html': True,
    'document_base_url': "{{ request.scheme }}://{{ request.get_host }}/",
    'allow_script_urls': True,
    'convert_urls': False  # false -> False로 수정
}