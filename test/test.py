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
    '''serializes and deserializes the object with pickle'''
    s = io.BytesIO()
    pickler = pickle.Pickler(s)
    pickler.dump(obj)
    unpickler = pickle.Unpickler(s)
    s.seek(0)
    return unpickler.load()

def do_readWrite(stream, *cls):
    '''serializes and deserializes the stream with the factory
cls are the additional stream classes required'''
    import stream.StreamFactory as StreamFactory
    import stream.StringStream as StringStream
    import stream.CachingStringStream as CachingStringStream
    import stream.DebugStream as DebugStream
    import stream.FileStream as FileStream
    fac =   StreamFactory.StreamFactory(\
             FileStream.FileStream(
              CachingStringStream.CachingStringStream(\
               StringStream.StringStream()
            )))
    for cls in cls:
        fac.registerStream(cls)
    fac.registerStream(type(stream))
    fac.write(stream)
    fac.flush()
    fac.update()
    return fac.read()

def test_factory(testCase, stream, *cls):
    s = do_readWrite(stream, *cls)
    testCase.assertIsInstance(s, type(stream))
    return s
