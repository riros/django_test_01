from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'project.urls'

REST_FRAMEWORK.update({  # noqa
    'PAGE_SIZE': 1,
})
