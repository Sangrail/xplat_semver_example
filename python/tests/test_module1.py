import unittest
from src.moduleToTest import add, SimplePoco, process_list_of_pocos

class TestModule1(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1,2), 3)
        self.assertEqual(add(0,0), 0)
        self.assertEqual(add(-1,1), 0)

    def test_process_list_of_pocos(self):
        self.assertTrue(process_list_of_pocos([SimplePoco(1, "a"), SimplePoco(2, "b")]))
        with self.assertRaises(ValueError):
            process_list_of_pocos([])
        with self.assertRaises(ValueError):
            process_list_of_pocos([SimplePoco(1, "a"), None])
        with self.assertRaises(ValueError):
            process_list_of_pocos([None, SimplePoco(1, "a")])


if __name__ == '__main__':
    unittest.main()