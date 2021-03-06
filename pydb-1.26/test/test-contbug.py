#!/usr/bin/python -t
# -*- Python -*-
# $Id: test-contbug.py.in,v 1.3 2008/12/08 00:40:57 rockyb Exp $
"Unit test for Extended Python debugger's runl and runv commands "
import difflib, os, sys, unittest, signal, time

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, os.path.join(top_builddir, 'pydb'))
top_srcdir = ".."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

import pydb

builddir     = "."
if builddir[-1] != os.path.sep:
    builddir += os.path.sep

srcdir = "."
if srcdir[-1] != os.path.sep:
    srcdir += os.path.sep

pydir        = os.path.join(top_builddir, "pydb")
pydb_short   = "pydb.py"
pydb_path    = os.path.join(pydir, pydb_short)

def diff_files(outfile, rightfile):
    fromfile  = rightfile
    fromdate  = time.ctime(os.stat(fromfile).st_mtime)
    fromlines = open(fromfile, 'U').readlines()
    tofile    = outfile
    todate    = time.ctime(os.stat(tofile).st_mtime)
    tolines   = open(tofile, 'U').readlines()
    
    diff = list(difflib.unified_diff(fromlines, tolines, fromfile,
                                     tofile, fromdate, todate))
    if len(diff) == 0:
        os.unlink(outfile)
    for line in diff:
        print line,
    return len(diff) == 0

class RunTests(unittest.TestCase):

    def test_continue_bug(self):
        """Test --exec and a bug whith 'c lineno' when given initially."""
        python_script = '%shanoi.py' % srcdir

        if sys.hexversion >= 0x02050000:
            rightfile = os.path.join(srcdir, 'data', 
                                     "contbug-2.5.right")
        else:
            rightfile = os.path.join(srcdir, 'data',
                                     "contbug.right")

        outfile       = 'contbug.out'
        if os.path.exists(outfile): os.unlink(outfile)
        args = ('--basename', '--nx', '--output', outfile,
                '--exec',
                "set linetrace off;; set trace-commands on;; c 12;; quit",
                python_script)
        pydb.runv(args)
        result = diff_files(outfile, rightfile)
        self.assertEqual(True, result, "continue bug (via runv)")

if __name__ == '__main__':
    unittest.main()
