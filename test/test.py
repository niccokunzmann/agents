import sys

sys.path.append('..')

import unittest
import winpdb

import sys
import os
import traceback

import pickle
import io

def pickle_unpickle(obj):
    s = io.BytesIO()
    pickler = pickle.Pickler(s)
    pickler.dump(obj)
    unpickler = pickle.Unpickler(s)
    s.seek(0)
    return unpickler.load()
