# -*- condig: utf-8 -*-
from datetime import datetime

from sitic.utils import constants


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
