# -*- condig: utf-8 -*-

class Menu(object):

    def __init__(self, generator, id, title, weight, url):
        self.generator = generator
        self.id = id
        self.title = title
        self.weight = weight
        self.url = url
        self.parent = None
        self._children = []

    def add_children(self, menu):
        if menu not in self._children:
            self._children.append(menu)
            menu.set_parent(self)

    def set_parent(self, menu):
        if menu != self.parent:
            self.parent = menu

    @property
    def has_children(self):
        return len(self._children) > 0

    @property
    def children(self):
        return sorted(self._children, key=lambda x: (x.weight, x.title))

    @property
    def has_current(self):

        if isinstance(sef.generator, str):
            return False

        menu_elements = [self]
        has_current = False

        while len(menu_elements) > 0:
            element = menu_elements.pop(0)
            if element.is_current:
                has_current = True
                break

            if element.has_children:
                menu_elements += element.children

        return has_current

    @property
    def is_current(self):
        is_current = False
        if isinstance(self.generator.current_url, str):
            is_current = self.generator.current_url.lstrip('/') == self.url.strip('/')
        return is_current
