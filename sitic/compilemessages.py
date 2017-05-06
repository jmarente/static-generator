# -*- condig: utf-8 -*-
import os

from sitic.utils import constants, call_subprocess
from sitic.config import config
from sitic.logging import logger


def has_bom(fn):
    import codecs
    with open(fn, 'rb') as f:
        sample = f.read(4)
    return sample.startswith((codecs.BOM_UTF8, codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE))


class CompileMessages(object):

    msgfmt_options = ['--check-format']

    def __init__(self):

        languages = config.get_languages()
        if len(languages) == 1 and languages[0] == constants.DEFAULT_LANG:
            logger.error('No languages configuration detected, can\'t create messages')
            sys.exit(1)

        self.po_filename = '{}.po'.format(constants.GETTEXT_DOMAIN)
        self.mo_filename = '{}.mo'.format(constants.GETTEXT_DOMAIN)

    def compile(self):
        for language in config.get_languages():
            locale_path = os.path.join(config.locales_path, language, 'LC_MESSAGES')
            po_file_path = os.path.join(locale_path, self.po_filename)
            mo_file_path = os.path.join(locale_path, self.mo_filename)

            if has_bom(po_file_path):
                logger.error("The {} file has a BOM (Byte Order Mark). "
                             "Sitic only supports .po files encoded in "
                             "UTF-8 and without any BOM.".format(po_file_path))

            if not os.path.exists(po_file_path):
                logger.warning("Not .po file found for language «{}»."
                               "Run «makemessages» to generate it.".format(language))
                continue

            msgmt_args = ['msgfmt'] + self.msgfmt_options + ['-o', mo_file_path, po_file_path]
            output, errors, status = call_subprocess(msgmt_args)

            if status != constants.STATUS_OK and errors:
                logger.error("errors happened while running msgmerge\n{}".format(errors))
                sys.exit(1)
            elif errors:
                logger.error(errors)

            logger.info('Messages successfully compiled for language «{}»'.format(language))

        logger.warning('Please, keep in mind that «msgfmt» won\'t generate any «.mo» file if no translation modified')

