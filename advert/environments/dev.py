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

EMAIL_FROM = ''
EMAIL_MESSAGES = {
    'sign_up': [
        'Advert - registration',
        'Hello!<br>You are now signed up. Your login: <%LOGIN%> <br><br>'
    ],
    'new_answer': [
        'Advert - added new answer to your question',
        'Hello!<br>New answer to your question has been added. You can find it on this page: <%LINK%> <br><br>'
    ]
}

EMAIL_SIGN = 'With best wishes,<br>Advert'

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
            'filename': '/work/advert/debug.log',
            'formatter': 'simple'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/work/advert/error.log',
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/work/advert/info.log',
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

