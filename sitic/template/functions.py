from jinja2 import contextfunction

from sitic.config import config

@contextfunction
def get_search_url(context):
    url_parts = []

    language = context['site'].get('language', None)

    if language and (language != context['site']['main_language'] or not config.main_language_as_root):
        url_parts.append(context['site']['language'])

    # TODO make search url configurable
    url_parts.append('search')

    return '/' + '/'.join(url_parts)
