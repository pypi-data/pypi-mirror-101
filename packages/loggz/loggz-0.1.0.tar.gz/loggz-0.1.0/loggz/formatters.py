#!/usr/bin/env python3

import traceback
import logging
import socket
from datetime import datetime
import json


class JsonFormatter(logging.Formatter):
    """ Base class to format logs as JSON.

    """

    def __init__(self):
        """ Create a new instance of JsonFormatter.
        """
        pass

    @classmethod
    def format_timestamp(cls, time):
        """ Format a timestamp as ISO.

        :param time: Time to format.
        :return: The ISO formatted time.
        """
        tstamp = datetime.utcfromtimestamp(time)
        return tstamp.strftime("%Y-%m-%dT%H:%M:%S") + ".%03d" % (tstamp.microsecond / 1000) + "Z"

    @classmethod
    def format_exception(cls, exc_info):
        """ Format a Python exception.

        :param exc_info: Exception.
        :return: The formatted exception.
        """
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    @classmethod
    def serialize(cls, message):
        """ Serialize a message as JSON.

        :param message: The message.
        :return: The serialized message in JSON.
        """
        return json.dumps(message)


class LogstashFormatter(JsonFormatter):
    """ A Logstash formatter for logging.

    :author: [Israel-FL](https://github.com/israel-fl/).
    :see: https://github.com/israel-fl/python3-logstash/tree/master/logstash
    """

    def __init__(self, message_type='Logstash', tags=None, fqdn=False):
        """ Create an instance of JsonFormatter.

        :param message_type: Log type.
        :param tags: Optional related tags.
        :param fqdn: Optional FQDN.
        """
        super(LogstashFormatter, self).__init__()

        self.message_type = message_type
        self.tags = tags if tags is not None else []

        if fqdn:
            self.host = socket.getfqdn()
        else:
            self.host = socket.gethostname()

    def get_extra_fields(self, record):
        """ Returns extra fields of the provided log record.

        The list contains all the attributes listed in [Python logging documentation](http://docs.python.org/library/logging.html#logrecord-attributes).

        :param record: The record.
        :return:
        """
        skip_list = (
            'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
            'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
            'msecs', 'msecs', 'message', 'msg', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'extra')

        easy_types = (str, bool, dict, float, int, list, type(None))

        fields = {}

        for key, value in record.__dict__.items():
            if key not in skip_list:
                if isinstance(value, easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    def get_debug_fields(self, record):
        """ Returns debug fields of the provided log record.

        :record: The log record.
        :returns: debug fields of the provided log record.
        """
        fields = {
            'stack_trace': self.format_exception(record.exc_info),
            'lineno': record.lineno,
            'process': record.process,
            'thread_name': record.threadName,
        }

        # funcName was added in 2.5
        if not getattr(record, 'funcName', None):
            fields['funcName'] = record.funcName

        # processName was added in 2.6
        if not getattr(record, 'processName', None):
            fields['processName'] = record.processName

        return fields

    @classmethod
    def format_source(cls, message_type, host, path):
        """ Format source of log as URI.

        :param message_type: The message type.
        :param host: The host.
        :param path: The path.
        :return: The formatted source as URI.
        """
        return "%s://%s/%s" % (message_type, host, path)

    def format(self, record):
        """ Format record.

        :param record: The log record.
        :return: The formatted record.
        """
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)
