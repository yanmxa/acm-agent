# coding: utf-8

def to_prompt(template, keys):
    return template.format(**keys)
