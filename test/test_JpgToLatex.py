"""Test class for testing the JpgToLatex script"""

import os
from os.path import dirname, abspath
import unittest
import options
import JpgToLatex


def reset_directory():
    # The script changes the working directory a lot this makes writing tests easier
    os.chdir(dirname(abspath(__file__)))


class TestJpgToLatex(unittest.TestCase):
    def setUp(self):
        reset_directory()
        self.test_obj = options.Options()
        self.test_obj.read_options('-d folder')

    def tearDown(self):
        reset_directory()
        for j in ['test.pdf', 'test.aux', 'test.log', 'test.tex']:
            if os.path.exists(j):
                os.remove(j)

        if os.path.exists('compressed'):
            for j in os.listdir('compressed'):
                os.remove('compressed\\' + j)
            os.rmdir('compressed')

    def test_use_default(self):
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.path.exists('test.pdf'))

    def test_preserve_image(self):
        self.test_obj.read_options(['-nc', '-jq', '100', '-r', '1'])
        JpgToLatex.main(self.test_obj)
        self.assertFalse(os.path.exists('compressed'))
        self.assertTrue(os.path.exists('test.pdf'))

    def test_name_option(self):
        def cleanup_foo():
            if os.path.exists('foo.pdf'):
                os.remove('foo.pdf')

        self.addCleanup(cleanup_foo)
        self.test_obj.read_options(['-n', 'foo'])
        JpgToLatex.main(self.test_obj)
        self.assertTrue('foo.pdf')


if __name__ == '__main__':
    unittest.main()
