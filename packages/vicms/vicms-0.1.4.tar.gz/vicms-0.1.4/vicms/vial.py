'''
vial.py:
this file contains the implementation description/version that should be changed
upon every build
'''
from flask import Blueprint, flash
from collections import namedtuple

AppArch = namedtuple('AppArch', ['bp'])

def make_blueprint(prefix=None, name='vicms'):
    prefix = prefix if prefix else '/%s'%name
    bp = Blueprint(name, __name__, url_prefix=prefix)
    return bp
