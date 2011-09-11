import sys

sys.path.append('..')

import unittest
import winpdb

import os
import traceback

import pickle

try:
    import io
except ImportError:
    import StringIO as io

from dedicatedTest import *

def pickle_unpickle(obj):
    s = io.BytesIO()
    pickler = pickle.Pickler(s)
    pickler.dump(obj)
    unpickler = pickle.Unpickler(s)
    s.seek(0)
    return unpickler.load()

                
                
