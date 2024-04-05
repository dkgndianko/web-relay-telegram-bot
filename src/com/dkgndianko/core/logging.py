import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO',
        },
        'file_info': {
            'class': 'logging.FileHandler',
            'filename': 'info.log',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_debug': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'detailed',
            'level': 'DEBUG',
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'detailed',
            'level': 'ERROR',
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file_info'],
            'level': 'INFO',
        },
        'com.dkgndianko': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app.module2': {
            'handlers': ['console', 'file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


logging.config.dictConfig(LOGGING_CONFIG)


__LOGGERS__ = {}

def get_logger(name: str):
    try:
        return __LOGGERS__[name]
    except KeyError:
        logger = logging.getLogger(__name__)
        __LOGGERS__[name] = logger
        return logger