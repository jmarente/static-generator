# -*- condig: utf-8 -*-

class Menu(object):

    def __init__(self, id, title, weight, url):
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
