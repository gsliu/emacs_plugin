#!/usr/bin/python -t
# $Id: test-setshow.py.in,v 1.5 2008/12/10 13:31:26 rockyb Exp $ -*- Python -*-
"Unit test of the file command for Extended Python debugger "
import difflib, os, time, sys, unittest

top_builddir = ".."
if top_builddir[-1] != os.path.sep:
    top_builddir += os.path.sep
sys.path.insert(0, os.path.join(top_builddir, 'pydb'))
top_srcdir = ".."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

builddir     = "."
if builddir[-1] != os.path.sep:
    builddir += os.path.sep

srcdir = "."
if srcdir[-1] != os.path.sep:
    srcdir += os.path.sep

pydir        = os.path.join(top_builddir, "pydb")
pydb_short   = "pydb.py"
pydb_path    = os.path.join(pydir, pydb_short)

def run_debugger(testname, pythonfile, pydb_opts='', args='',
                 rightfile=None):
    global srcdir, builddir, pydir

    if rightfile is None:
        rightfile = os.path.join(srcdir, 'data',
                                 "%s.right" % testname)

    os.environ['PYTHONPATH']=os.pathsep.join(sys.path)
    cmdfile     = os.path.join(srcdir, "%s.cmd"   % testname)
    outfile     = "%s.out" % testname
    outfile_opt = '--output=%s ' % outfile

    # print "builddir: %s, cmdfile: %s, outfile: %s, rightfile: %s" % \
    # (builddir, cmdfile, outfile, rightfile)

    if os.path.exists(outfile): os.unlink(outfile)

    cmd = "%s --command %s %s %s %s %s" % \
          (pydb_path, cmdfile, outfile_opt, pydb_opts, args, pythonfile)
    
    os.system(cmd)
    fromfile  = rightfile
    fromdate  = time.ctime(os.stat(fromfile).st_mtime)
#   fromlines = open(fromfile, 'U').readlines()[0:-1]
    fromlines = open(fromfile, 'U').readlines()
    tofile    = outfile
    todate    = time.ctime(os.stat(tofile).st_mtime)
#   tolines   = open(tofile, 'U').readlines()[0:-1]
    tolines   = open(tofile, 'U').readlines()
    diff = list(difflib.unified_diff(fromlines, tolines, fromfile,
                                     tofile, fromdate, todate))
    if len(diff) == 0:
        os.unlink(outfile)
    for line in diff:
        print line,
    return len(diff) == 0
    
class PdbTests(unittest.TestCase):

    def test_setshow(self):
        """Test running program via the 'file' command"""

        try: 
            import readline
            rightfile = os.path.join(srcdir, 'data',
                                     "setshow.right")
        except ImportError:
            rightfile = os.path.join(srcdir, 'data',
                                     "setshow-no-rl.right")

        result=run_debugger(testname='setshow', pythonfile='',
                            pydb_opts='--basename', rightfile=rightfile)
        self.assertEqual(True, result, "pydb 'set/show' command comparision")
        return

if __name__ == "__main__":
    unittest.main()
