import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8jv82iibz&*ms_=f*pal0-kq21*7hycou!+7%)wi4$vk7u@%%#'

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
    'setting',
    'ftp',
    'crontab',
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

ROOT_URLCONF = 'panel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'panel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data/panel.db'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_AGE = 60*30
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'

OPTIONS_FILE = '/root/oneinstack/options.conf'

# Get OneinStack install path, You can't change
with open(OPTIONS_FILE, 'r') as f:
    OPTIONS = {}
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        OPTIONS[line.split('=')[0]]=line.split('=')[1]
        if line.split('=')[0] in ('mysql_install_dir','mariadb_install_dir','percona_install_dir','alisql_install_dir'):
            if os.path.isdir(line.split('=')[1]+'/support-files'):
                OPTIONS['db_install_dir'] = line.split('=')[1]
        if line.split('=')[0] in ('mysql_data_dir','mariadb_data_dir','percona_data_dir','alisql_data_dir'):
            if os.path.isfile(line.split('=')[1]+'/mysql-bin.index'):
                OPTIONS['db_data_dir'] = line.split('=')[1]
        if line.split('=')[0] in ('nginx_install_dir','tengine_install_dir'):
            if os.path.isfile(line.split('=')[1]+'/sbin/nginx'):
                OPTIONS['web_install_dir'] = line.split('=')[1]
        if line.split('=')[0] == 'openresty_install_dir':
            if os.path.isfile(line.split('=')[1]+'/nginx/sbin/nginx'):
                OPTIONS['web_install_dir'] = line.split('=')[1]+'/nginx'
