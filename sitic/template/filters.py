# -*- condig: utf-8 -*-
import json

from sitic.config import config

def get_json(path):
    print('get_json', path)
    with open(path, 'r') as f:
        content = json.load(f)
        return content
