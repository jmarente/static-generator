# -*- condig: utf-8 -*-
import os
import sys

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from sitic.config import config
from sitic.utils import constants, call_subprocess
from sitic.logging import logger


def clean_msg(msg):
    return [s.strip() for s in msg.splitlines()]


class MakeMessages(object):

    msguniq_options = ['--to-code=utf-8']
    msgmerge_options = ['-q', '--previous']

    def __init__(self):

        languages = config.get_languages()
        if len(languages) == 1 and languages[0] == constants.DEFAULT_LANG:
            logger.error('No languages configuration detected, can\'t create messages')
            sys.exit(1)

        loader = FileSystemLoader(config.files_path)

        self.env = Environment(extensions=['jinja2.ext.i18n'], loader=loader)
        self.env.filters['clean_msg'] = clean_msg

        self.translations = []
        self.pot_filename = '{}.pot'.format(constants.GETTEXT_DOMAIN)
        self.po_filename = '{}.po'.format(constants.GETTEXT_DOMAIN)
        self.pot_file_path = os.path.join(config.locales_path, self.pot_filename)

    def run(self):

        self.extract_translations()
        self.generate_pot_file()
        self.generate_po_file()
        self.delete_pot_file()

    def extract_translations(self):
        for root, directory, files in os.walk(config.templates_path):
            for f in files:
                if not f.endswith(tuple(constants.VALID_TEMPLATES_EXTENSIONS)):
                    continue
                file_path = os.path.join(root, f)
                relative_file_path = file_path.replace(config.base_path, '')
                with open(file_path, 'r') as content:
                    translations = self.env.extract_translations(content.read())
                    for t in translations:
                        t = list(t)
                        t.insert(0, relative_file_path)
                        self.translations.append(t)

    def generate_pot_file(self):
        pot_template = self.env.get_template('pot_template.jinja')
        pot_content = pot_template.render({'translations': self.translations})

        if not os.path.isdir(config.locales_path):
            os.makedirs(config.locales_path)

        with open(self.pot_file_path, 'w', encoding='utf-8') as f:
            f.write(pot_content)

        msguniq_args = ['msguniq'] + self.msguniq_options + [self.pot_file_path]
        output, errors, status = call_subprocess(msguniq_args)

        if status != constants.STATUS_OK and errors:
            logger.error("errors happened while running msguniq\n{}".format(errors))
            sys.exit(1)
        elif errors:
            logger.error(errors)

        # Replace pot file with msguniq output
        with open(self.pot_file_path, 'w', encoding='utf-8') as f:
            f.write(output)

    def generate_po_file(self):
        for language in config.get_languages():
            locale_path = os.path.join(config.locales_path, language, 'LC_MESSAGES')
            po_file_path = os.path.join(locale_path, self.po_filename)

            po_content = ''
            if not os.path.isdir(locale_path):
                os.makedirs(locale_path)

            if not os.path.exists(po_file_path):
                with open(self.pot_file_path, 'r') as f:
                    po_content = f.read()
            else:
                msgmerge_args = ['msgmerge'] + self.msgmerge_options + [po_file_path, self.pot_file_path]
                po_content, errors, status = call_subprocess(msgmerge_args)
                if status != constants.STATUS_OK and errors:
                    logger.error("errors happened while running msgmerge\n{}".format(errors))
                    sys.exit(1)
                elif errors:
                    logger.error(errors)

            with open(po_file_path, 'w', encoding='utf-8') as f:
                f.write(po_content)

            logger.info('«.po» file generated for language «{}» at «{}»'.format(language, po_file_path))

    def delete_pot_file(self):
        os.remove(self.pot_file_path)
