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



if __name__ == '__main__':
    try:
        __file__
    except NameError:
        path = '.'
    else:
        path = os.path.split(__file__)[0]
    d = {}
    for filename in os.listdir(path):
        if filename.startswith('test_'):
            filepath = os.path.join(path, filename)
            modname, ext = os.path.splitext(filename)
            if os.path.isfile(filepath) and ext.lower() in ('py', 'pyw'):
                mod = __import__(modname)
            else:
                try:
                    mod = __import__(modname)
                except ImportError:
                    ty, er, tb = sys.exc_info()
                    if tb.tb_next:
                        traceback.print_exception(ty, er, tb)
                    continue
        
            if hasattr(mod, 'test_module'):
                mod.test_module()
                
                
