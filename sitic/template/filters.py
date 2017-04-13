# -*- condig: utf-8 -*-
import json
import csv
import yaml

from sitic.config import config

def get_json(path):
    with open(path, 'r') as f:
        content = json.load(f)
    return content

def get_yaml(path):
    with open(path, 'r') as f:
        content = yaml.load(f)
    return content

def get_csv(path, delimiter=",", is_dict=False):
    with open(path, 'r') as f:
        content = csv.reader(f, delimiter=delimiter) \
                if not is_dict \
                else csv.DictReader(f, delimiter=delimiter)
    return content
