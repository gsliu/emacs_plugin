#!/usr/bin/python -t
# -*- Python -*-
# $Id: test-sighandle.py.in,v 1.2 2009/03/06 08:51:46 rockyb Exp $
"Unit test for Extended Python debugger's signal handling commands "
import os, time, sys, unittest, signal

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, os.path.join(top_builddir, 'pydb'))
top_srcdir = ".."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

import pydb, sighandler

builddir     = "."
if builddir[-1] != os.path.sep:
    builddir += os.path.sep

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep

srcdir = "."
if srcdir[-1] != os.path.sep:
    srcdir += os.path.sep

pydir        = os.path.join(top_builddir, "pydb")
pydb_short   = "pydb.py"
pydb_path    = os.path.join(pydir, pydb_short)
outfile      = 'sighandler.out'
program      = 'sigtestexample.py'

class PdbTest(pydb.Pdb):
    def __init__(self):
        pydb.Pdb.__init__(self)
        self.errLines = []
        self.msgLines = []
        self.msg_last_nocr = False
        self.stack = self.curframe = self.botframe = None

    def resetmsg(self):
        self.msgLines=[]

    def errmsg(self, msg):
        self.errLines.append(msg)

    def msg(self, msg):
        if self.msg_last_nocr:
            self.msgLines[-1] += msg
        else:
            self.msgLines.append(msg)
        self.msg_last_nocr = False

    def msg_nocr(self, msg):
        if self.msg_last_nocr:
            self.msgLines[-1] += msg
        else:
            self.msgLines.append(msg)
        self.msg_last_nocr = True

class SigTests(unittest.TestCase):

    def test_settings(self):
        """Test setting signals"""
        p = PdbTest()
        h = sighandler.SignalManager(p)
        # Set to known value
        h.action('SIGUSR1 print pass')
        h.info_signal(['USR1'])
        correct = ["Signal        Stop	Print	Stack	Pass	Description",
                   "SIGUSR1       No  	Yes 	Yes  	No  	User-defined signal 1"]
        self.assertEqual(p.msgLines, correct)
        p.resetmsg()
        # noprint implies no stop
        h.action('SIGUSR1 noprint stack pass')
        h.info_signal(['USR1'])
        correct = ["Signal        Stop	Print	Stack	Pass	Description",
                   "SIGUSR1       No  	No  	Yes  	Yes 	User-defined signal 1"]
        self.assertEqual(p.msgLines, correct)
        # stop keyword implies print and nopass
        p.resetmsg()
        h.action('SIGUSR1 stop')
        h.info_signal(['USR1'])
        correct = ["Signal        Stop	Print	Stack	Pass	Description",
                   "SIGUSR1       Yes 	Yes 	No   	Yes 	User-defined signal 1"]
        self.assertEqual(p.msgLines, correct)
         
if __name__ == '__main__':
    unittest.main()
