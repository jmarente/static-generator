# -*- condig: utf-8 -*-
from sitic.content.frontmatter_handlers import YamlHander, TomlHandler


handlers = [handler() for handler in [YamlHander, TomlHandler]]

def __get_handler(text):
    text_handler = None

    for handler in handlers:
        if handler.has_format(text):
            text_handler = handler
            break

    return handler


def __parse(text, handler):
    text = text.strip()
    metadata = {}

    handler = handler or __get_handler(text)
    if not handler:
        return metadata, text


    try:
        metadata, text = handler.split(text)
    except ValueError:
        return metadata, text

    metadata = handler.load(metadata)

    return metadata, text


def load(file_path, handler=None):
    text = ''

    with open(file_path, 'r') as f:
        text = f.read()

    text = text.strip()
    handler = handler or __get_handler(text)
    return loads(text, handler)


def loads(text, handler=None):
    handler = handler or __get_handler(text)
    return __parse(text, handler)
