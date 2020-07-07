"""Test class for testing the JpgToLatex script"""

import os
from os.path import dirname, abspath
import unittest
import options
import JpgToLatex


def reset_directory():
    # Changes the working directory a lot this makes writing tests easier
    os.chdir(dirname(abspath(__file__)))
    os.chdir('folder')


class TestJpgToLatex(unittest.TestCase):
    def setUp(self):
        reset_directory()
        self.test_obj = options.Options()

    def tearDown(self):
        reset_directory()
        for j in ['.pdf', '.aux', '.log', '.tex']:
            j = 'folder' + j
            if os.path.exists(j):
                os.remove(j)

        if os.path.exists('compressed'):
            for j in os.listdir('compressed'):
                os.remove('compressed\\' + j)
            os.rmdir('compressed')

    def test_use_default(self):
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.path.exists('folder.pdf'))
        self.assertGreater(os.path.getsize('folder.pdf'), 0)

    def test_preserve_image(self):
        self.test_obj.read_options(['-nc', '-jq', '100', '-r', '1'])
        JpgToLatex.main(self.test_obj)
        self.assertFalse(os.path.exists('compressed'))
        self.assertTrue(os.path.exists('folder.pdf'))
        self.assertGreater(os.path.getsize('folder.pdf'), 0)

    def test_name_option(self):
        def cleanup_foo():
            if os.path.exists('foo.pdf'):
                os.remove('foo.pdf')

        self.addCleanup(cleanup_foo)
        self.test_obj.read_options(['-n', 'foo'])
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.path.exists('foo.pdf'))
        self.assertGreater(os.path.getsize('foo.pdf'), 0)

    def test_compressed_already_exists(self):
        if not os.path.exists('compressed'):
            os.mkdir('compressed')
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.path.exists('folder.pdf'))
        self.assertGreater(os.path.getsize('folder.pdf'), 0)

    def test_shrink_images(self):
        self.test_obj.read_options(['-r', '0.5', '-nc'])
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.listdir('compressed'))
        self.assertTrue(os.path.exists('folder.pdf'))
        self.assertGreater(os.path.getsize('folder.pdf'), 0)

    def test_zero_size_images(self):
        self.test_obj.read_options(['-r', '0'])
        JpgToLatex.main(self.test_obj)
        self.assertTrue(os.path.exists('folder.pdf'))
        self.assertEqual(os.path.getsize('folder.pdf'), 0)


if __name__ == '__main__':
    unittest.main()
