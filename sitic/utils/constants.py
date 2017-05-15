DEFAULT_PUBLIC_PATH='public/'
DEFAULT_CONTENT_PATH='content/'
DEFAULT_STATIC_PATH='static/'
DEFAULT_TEMPLATES_PATH='templates/'
DEFAULT_LOCALES_PATH='locales/'

VALID_CONTENT_EXTENSIONS=['.md']
VALID_TEMPLATES_EXTENSIONS=['.html']

# Ignore files starting with «.»
IGNORE_FILES_PATTERN = ['^\..*$']

# Server constants
DEFAULT_PORT=8000

DATE_FORMATS = ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]

# Singular - Plural
DEFAULT_TAXONOMIES = {
    'category': 'categories',
    'tag': 'tags',
}

DEFAULT_LANG = None

GETTEXT_DOMAIN = 'sitic'

STATUS_OK = 0
STATUS_KO = 1

DEFAULT_RSS_LIMIT = 20
