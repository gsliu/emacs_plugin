#!/usr/bin/python -t
'Unit test for pydb.bytecode'
import inspect, os, sys, unittest

top_srcdir = "../.."
if top_srcdir[-1] != os.path.sep:
    top_srcdir += os.path.sep
sys.path.insert(0, os.path.join(top_srcdir, 'pydb'))

from bytecode import op_at_frame, stmt_contains_make_function, is_def_stmt

class TestByteCode(unittest.TestCase):

    def test_contains_make_function(self):
        def sqr(x):
            return x * x
        frame = inspect.currentframe()
        co = frame.f_code
        lineno = frame.f_lineno
        self.assertTrue(stmt_contains_make_function(co, lineno-4))
        self.assertFalse(stmt_contains_make_function(co, lineno))
        return

    def test_op_at_frame(self):
        frame = inspect.currentframe()
        self.assertEqual('CALL_FUNCTION', op_at_frame(frame))
        return

    def test_is_def_frame(self):
        # Not a "def" statement because frame is wrong spot
        frame = inspect.currentframe()
        self.assertFalse(is_def_stmt('foo(): pass', frame))
        return
        
if __name__ == '__main__':
    unittest.main()
