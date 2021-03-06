#!/usr/bin/python -t
# -*- Python -*-
# $Id: test-sig.py.in,v 1.4 2009/01/22 03:50:13 rockyb Exp $
"Unit test for Extended Python debugger's signal handling commands "
import os, sys, unittest, signal

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, os.path.join(top_builddir, 'pydb'))
top_srcdir = ".."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

import sighandler

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
program      = os.path.join(srcdir, 'sigtestexample.py')

class SigTests(unittest.TestCase):
    def tearDown(self):
        try:
            os.unlink(outfile)
        except OSError:
            pass
        try:
            os.unlink('log')
        except OSError:
            pass

    def create_pydb_proc(self, cmds,arg=None):
        """Run pydb on program with command string 'cmds', and pass arg if
        that is given. Debugger output is stored in outfile. Note that
        there is also output produced by the debugged program.
        """
        os.environ['PYTHONPATH']=os.pathsep.join(sys.path)
        if arg:
            pid = os.spawnlp(os.P_WAIT, pydb_path, pydb_path, '--sigcheck',
                             '-o', outfile,
                             '-e', '%s' % cmds, program, arg)
        else:
            pid = os.spawnlp(os.P_NOWAIT, pydb_path, pydb_path, '--sigcheck',
                             '-o', outfile,
                             '-e', '%s' % cmds, program)
        return pid

    def test_signum_name(self):
        """Test that signal name and number lookup work """
        for signum in range(signal.NSIG):
            signame = sighandler.lookup_signame(signum)
            if signame is not None:
                self.assertEqual(signum, sighandler.lookup_signum(signame))
                # Try without the SIG prefix
                self.assertEqual(signum, sighandler.lookup_signum(signame[3:]))

    def test_noprint_nostop_pass(self):
        """Check to see the debugger does not intercepts a USR1 signal,
        doesn't print intercepting it but passes it along to the program."""

        self.tearDown()
        cmds = 'handle SIGUSR1 noprint nostop pass;;next 10;;quit'
        pid = self.create_pydb_proc(cmds, 'signal')
        f = open(outfile, 'r')
        lines = f.readlines()
        f.close()
        self.assertEqual(False,'Program received signal SIGUSR1\n' in lines) 
        f = open('log', 'r')
        line = f.readline()
        f.close()
        self.assertEqual(line, 'signal received\n')
        os.unlink('log')

    def test_noprint_nostop_nopass(self):
        """Check to see the debugger does not intercepts a USR1 signal,
        doesn't print intercepting and doesn't pass it along to the program."""

        self.tearDown()
        cmds = 'handle SIGUSR1 noprint nostop nopass;;set sigcheck on;;continue;;quit'
        pid = self.create_pydb_proc(cmds, 'signal')
        f = open(outfile, 'r')
        lines = f.readlines()
        f.close()
        self.assertEqual(False,'Program received signal SIGUSR1\n' in lines) 
        self.assertRaises(IOError, open, 'log', 'r')

    def test_print_nostop_nopass(self):
        """Check to see the debugger intercepts a USR1 signal,
        prints it and doesn't pass it along to the program.
        """
        self.tearDown()
        cmds = "handle SIGUSR1 print nostop nopass;;set sigcheck on;;continue;;quit"
        pid = self.create_pydb_proc(cmds, 'signal')
        f = open(outfile, 'r')
        lines = f.readlines()
        f.close()

        self.assertEqual(True,'Program received signal SIGUSR1\n' in lines)
        self.assertRaises(IOError, open, 'log', 'r')

    def test_print_nostop_pass(self):
        """Check to see the debugger intercepts a USR1 signal,
        prints it and passes it along to the program.
        """
        self.tearDown()
        cmds = "handle SIGUSR1 print nostop pass;;next 10;;quit"
        pid = self.create_pydb_proc(cmds, 'signal')
        f = open(outfile, 'r')
        lines = f.readlines()
        f.close()

        self.assertEqual(True,'Program received signal SIGUSR1\n' in lines)
        f = open('log', 'r')
        line = f.readline()
        f.close()
        self.assertEqual(line, 'signal received\n')
        os.unlink('log')

    def test_print_stop(self):
        """Check to see the debugger intercepts a USR1 signal and stops."""

        self.tearDown()
        cmds = 'set basename on;;handle SIGUSR1 print stop;;continue;;where;;quit'
        pid = self.create_pydb_proc(cmds, 'signal')
        f = open(outfile, 'r')
        lines = f.readlines()
        f.close()
        self.assertEqual(True, 'Program received signal SIGUSR1\n' in lines)
        if sys.hexversion < 0x02050000:
            self.assertEqual(True,
                             "-> 0 in file 'sigtestexample.py' at line 20\n"
                             in lines)
        else:
            self.assertEqual(True,
                             "-> 0 <module> execfile() file 'sigtestexample.py' at line 20\n"
                             in lines)
        self.assertRaises(IOError, open, 'log', 'r')

if __name__ == '__main__':
    unittest.main()
