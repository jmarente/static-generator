# -*- condig: utf-8 -*-
import os
import sys

from datetime import datetime
from subprocess import PIPE, Popen

from sitic.utils import constants
from sitic.logging import logger


def boolean(element):
    value = False
    if type(element) == 'str':
        value = element.lower() in ['yes', 'y', 'true', '1']
    else:
        value = bool(element)
    return value


def get_valid_date(element, default=None):
    value = default

    if element:
        for date_format in constants.DATE_FORMATS:
            try:
                value = datetime.strptime(element, date_format)
                break;
            except ValueError:
                pass

    return value

def force_text(s, encoding='utf-8', errors='strict'):
    if issubclass(type(s), str):
        return s
    try:
        if isinstance(s, bytes):
            s = str(s, encoding, errors)
        else:
            s = str(s)
    except UnicodeDecodeError as e:
        logger.error('Error: {}'.format(str(e)))
        sys.exit(1)
    return s


def call_subprocess(args, stdout_encoding='utf-8'):
    """
    Friendly wrapper around Popen.

    Return stdout output, stderr output, and OS status code.
    """
    try:
        p = Popen(args, shell=False, stdout=PIPE, stderr=PIPE, close_fds=os.name != 'nt')
    except OSError as err:
        logger.error('Error executing: {}'.format(args[0]))
        sys.exit(1)
    output, errors = p.communicate()
    return (
        force_text(output),
        force_text(errors),
        p.returncode
    )
