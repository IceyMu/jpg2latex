import os
import unittest
import options


class TestOptions(unittest.TestCase):
    # Verbose option tests
    def test_verbose(self):
        for j in ('-v', '--verbose'):
            self.test_obj = options.Options(v=False)
            self.assertFalse(self.test_obj.verbose)
            self.test_obj.read_options([j])
            self.assertTrue(self.test_obj.verbose)

    def test_verbose_no_switch(self):
        self.test_obj = options.Options(v=False)
        self.assertFalse(self.test_obj.verbose)
        self.test_obj.read_options(['-z'])
        self.assertFalse(self.test_obj.verbose)

    # Quiet option test
    def test_quiet(self):
        for j in ('-q', '--quiet'):
            self.test_obj = options.Options(v=True)
            self.assertTrue(self.test_obj.verbose)
            self.test_obj.read_options([j])
            self.assertFalse(self.test_obj.verbose)

    # Cleanup option test
    def test_cleanup(self):
        for j in ('-c', '--cleanup'):
            self.test_obj = options.Options(c=False)
            self.assertFalse(self.test_obj.cleanup)
            self.test_obj.read_options([j])
            self.assertTrue(self.test_obj.cleanup)

    def test_no_cleanup(self):
        for j in ('-nc', '--no-cleanup'):
            self.test_obj = options.Options(c=True)
            self.assertTrue(self.test_obj.cleanup)
            self.test_obj.read_options([j])
            self.assertFalse(self.test_obj.cleanup)

    def test_name_default(self):
        self.test_obj = options.Options()
        self.assertEqual(self.test_obj.name, os.path.basename(os.getcwd()) + '.tex')

    def test_name_append_tex(self):
        for j in ('-n', '--name'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, 'test'])
            self.assertEqual(self.test_obj.name, 'test.tex')

    def test_name_no_append(self):
        for j in ('-n', '--name'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, 'test.tex'])
            self.assertTrue(self.test_obj.name, 'test.tex')

    def test_name_input_dir_change(self):
        self.test_obj = options.Options()
        self.test_obj.read_options(['-d', 'folder'])
        self.assertEqual(self.test_obj.name, 'folder.tex')

    def test_directory(self):
        for j in ('-d', '--dir', '--directory'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, 'folder'])
            self.assertEqual(self.test_obj.input_dir, 'folder')
            self.assertEqual(self.test_obj.lop, os.listdir('folder'))

    def test_directory_no_input(self):
        self.test_obj = options.Options()
        try:
            self.test_obj.read_options(['-d'])
            self.fail('No exception thrown')
        except IndexError:
            pass  # This exception should be thrown
        except:
            self.fail("Wrong type of exception")

    def test_directory_dne(self):
        self.test_obj = options.Options()
        try:
            self.test_obj.read_options(['-d', 'no_folder'])
            self.fail('No exception thrown')
        except FileNotFoundError:
            pass  # This exception should be thrown
        except:
            self.fail('Wrong exception thrown')

    def test_scale(self):
        for j in ('-s', '--scale'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, '0.5'])
            self.assertEqual(self.test_obj.scale, 0.5)

    def test_scale_no_input(self):
        try:
            self.test_obj = options.Options()
            self.test_obj.read_options(['-s'])
            self.fail('No exception thrown')
        except IndexError:
            pass # This exception should be thrown
        except:
            self.fail("Wrong type of exception")

    def test_scale_non_float_input(self):
        try:
            self.test_obj = options.Options()
            self.test_obj.read_options(['-s', 'one'])
            self.fail('No exception thrown')
        except ValueError:
            pass  # This exception should be thrown
        except not ValueError:
            self.fail("Wrong type of exception")


if __name__ == '__main__':
    unittest.main()
