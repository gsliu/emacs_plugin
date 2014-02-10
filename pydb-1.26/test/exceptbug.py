#!/usr/bin/python -t
from __future__ import with_statement
import os, sys

import threading

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, os.path.join(top_builddir, 'pydb'))
top_srcdir = ".."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

def f():
    l = threading.Lock()
    with l:
        print "hello"
        raise Exception("error")
        print "world"

try:
    f()
except:
   import pydb
   # pydb.pm()
   pydb.pm(['set basename on','set interactive off', 'where','quit'])
