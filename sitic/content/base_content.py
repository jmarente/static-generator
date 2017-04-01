# -*- condig: utf-8 -*-

class BaseContent(object):
    name = ""
    paginable = False

    def is_paginable(self):
        return paginable

    def get_url(self):
        raise NotImplementedError()

    def get_simple_context(self):
        raise NotImplementedError()

    def get_context(self):
        raise NotImplementedError()

    def get_path(self):
        raise NotImplementedError()
