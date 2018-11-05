# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Domain settings

ALLOWED_HOSTS = ['localhost','advert.daiteco.ru']
SITE_URL = 'advert.daiteco.ru'


# E-mail settings

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'hasker123'
EMAIL_HOST_PASSWORD = 'hasker'
EMAIL_USE_SSL = True

EMAIL_FROM = 'hasker123@yandex.ru'
EMAIL_TO = 'a.egorov@daiteco.ru'


# Custom settings

USER_MODERATION = False



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/work/advert-service/debug.log',
            'formatter': 'simple'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/work/advert-service/error.log',
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/work/advert-service/info.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'advert': {
            'handlers': ['file_info', 'file_error'],
            'propagate': True,
        },
    },
}

