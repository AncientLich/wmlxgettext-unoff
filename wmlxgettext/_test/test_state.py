import unittest
from pywmlx.state.state import State



class Test_State(unittest.TestCase):
    def test_class_state(self):
        state = State(regex="rx", run="run", iffail="fail")
        self.assertEqual(state.regex, 'rx')
        self.assertEqual(state.run, 'run')
        self.assertEqual(state.iffail, 'fail')


