# -*- condig: utf-8 -*-
import numbers

class Scoper(object):

    def __init__(self):
        self.variables = {}

    def get(self, var):
        return self.variables.get(var, None)

    def set(self, var, value):
        self.variables[var] = value
        return ''

    def add(self, var, value):
        current_value = self.variables.get(var, None)
        if isinstance(current_value, list):
            current_value.append(value)
            new_value = current_value
        elif isinstance(current_value, numbers.Real):
            new_value = current_value + value
        else:
            new_value = value
        self.variables[var] = new_value
        return ''

    def set_in_dict(self, dict_name, key, value):
        dict_content = self._get_dict(dict_name)
        dict_content[key] = value
        return ''

    def get_in_dict(self, dict_name, key):
        dict_content = self._get_dict(dict_name)
        return dict_content.get(key, None)

    def get_sorted_in_dict(self, dict_name, key):
        dict_content = self._get_dict(dict_name)
        return sorted(dict_content.values())

    def _get_dict(self, dict_name):
        dict_content = self.variables.get(dict_name, {})
        if not isinstance(dict_name, dict):
            dict_content = {}
        return dict_content
