# -*- condig: utf-8 -*-
import os
import inspect
import gettext
import importlib.util

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from sitic.config import config
from sitic.template import filters, functions
from sitic.utils import constants
from sitic.logging import logger

class Render(object):
    environment = None
    loader = None

    def __init__(self, language):
        self.loader = FileSystemLoader([config.templates_path, config.files_path])
        self.environment = Environment(loader=self.loader,
                                       extensions=['jinja2.ext.i18n'])

        translations = self.get_translations(language)
        self.environment.install_gettext_translations(translations, True)

        for name, function in inspect.getmembers(filters, predicate=inspect.isfunction):
            self.environment.filters[name] = function

        self.environment.globals['get_search_url'] = functions.get_search_url

        if config.custom_filters:
            spec = importlib.util.spec_from_file_location("custom_filters", config.custom_filters)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            for name, function in inspect.getmembers(foo, predicate=inspect.isfunction):
                if not name.startswith('custom_'):
                    name = '{}_{}'.format('custom', name)
                self.environment.filters[name] = function

    def render(self, content, output_path, context, meta_tag, js_includes):
        template = self.get_content_template(content)
        if template:

            content = template.render(**context)
            content = content.replace('</head>', "{}\n\n</head>".format(meta_tag))

            js_includes = '\n'.join(js_includes)
            content = content.replace('</body>', "{}\n\n</body>".format(js_includes))

            with open(output_path, 'w') as output_file:
                output_file.write(content)
        else:
            logger.warning('No template found for content - {}'.format(content))

    def get_content_template(self, content):
        template = None
        possible_templates = content.get_templates()

        for template_name in possible_templates:
            template = self.get_template(template_name)
            if template:
                break;

        return template

    def get_template(self, template_name):
        try:
            template = self.environment.get_template(template_name)
        except TemplateNotFound as e:
            template = None
        return template

    def get_translations(self, language):
        locale_dir = config.locales_path
        if language == constants.DEFAULT_LANG:
            translations = gettext.NullTranslations()
        else:
            langs = [language]
            try:
                translations = gettext.translation(constants.GETTEXT_DOMAIN, locale_dir, langs)
            except (IOError, OSError):
                logger.warning((
                    "Cannot find translations for language '{}'."
                    " Installing NullTranslations.").format(
                        language, constants.GETTEXT_DOMAIN))
                translations = gettext.NullTranslations()
        return translations
