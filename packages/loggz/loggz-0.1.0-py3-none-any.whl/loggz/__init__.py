#!/usr/bin/env python3


# @see: https://gist.github.com/pmav99/49c01313db33f3453b22
import logging
import logging.config
import os
import sys
from socket import socket

from loggz.formatters import LogstashFormatter

DEFAULT_LOGGER_NAME = 'root' or os.environ.get('LOGGZ_DEFAULT_LOGGER_NAME')
""" The default logger name.
"""

DEFAULT_LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'logstash_formatter': {'()': LogstashFormatter, }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'logstash_formatter',
            'level': 'DEBUG',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}


def setup(config: dict = DEFAULT_LOG_SETTINGS):
    logging.config.dictConfig(config=config)


def factory(name: str = DEFAULT_LOGGER_NAME, suffix: str = None):
    if isinstance(suffix, str) and len(suffix) > 0:
        try:
            return logging.getLogger(name=name).getChild(suffix=suffix)
        except Exception as e:
            return logging.getLogger(name)
    return logging.getLogger(name)
