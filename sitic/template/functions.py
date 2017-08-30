
from jinja2 import contextfunction

@contextfunction
def get_search_url(context):
    url_parts = []

    if context['site'].get('language', None):
        url_parts.append(context['site']['language'])

    # TODO make search url configurable
    url_parts.append('search')

    return '/' + '/'.join(url_parts)
