import unittest
import main

class TestMain(unittest.TestCase):

    def test_process_event(self):
        event = {}
        result = main.process_event(event, None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()