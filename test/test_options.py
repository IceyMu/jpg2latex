import os
import unittest
import options


class TestOptions(unittest.TestCase):
    def exception_test(self, inputs, error):
        try:
            self.test_obj = options.Options()
            self.test_obj.read_options(inputs)
            self.fail("No exception thrown")
        except error:
            pass  # This exception should be thrown
        except not error:
            self.fail("Wrong type of exception")

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
        self.exception_test(['-d'], IndexError)

    def test_directory_dne(self):
        self.exception_test(['-d', 'no_folder'], FileNotFoundError)

    def test_ratio(self):
        for j in ('-r', '--resize', '--ratio'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, '1'])
            self.assertEqual(self.test_obj.ratio, 1)

    def test_ratio_no_input(self):
        self.exception_test(['-r'], IndexError)

    def test_ratio_non_float_input(self):
        self.exception_test(['-r', 'one'], ValueError)

    def test_quality(self):
        for j in ('-cq', '--quality', '--compression-quality'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, '1'])
            self.assertEqual(self.test_obj.quality, 1)

    def test_quality_no_input(self):
        self.exception_test(['-cq'], IndexError)

    def test_quality_non_int_input(self):
        self.exception_test(['-cq', 'one'], ValueError)

    def test_angle(self):
        for j in ('-a', '--angle'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, '0'])
            self.assertEqual(self.test_obj.angle, 0)

    def test_angle_no_input(self):
        self.exception_test(['-a'], IndexError)

    def test_angle_non_float_input(self):
        self.exception_test(['-a', 'one'], ValueError)

    def test_formats(self):
        for j in ('-f', '--formats'):
            self.test_obj = options.Options()
            self.test_obj.read_options([j, 'jpg'])
            self.assertEqual(self.test_obj.formats, ['jpg'])

    def test_formats_no_input(self):
        self.exception_test(['-f'], IndexError)

    def test_formats_break_for_other_option(self):
        self.test_obj = options.Options()
        self.test_obj.read_options(['-f', 'jpg', '-v'])
        self.assertEqual(self.test_obj.formats, ['jpg'])

    def test_formats_many_inputs(self):
        self.test_obj = options.Options()
        self.test_obj.read_options(['-f', 'jpg', 'png'])
        self.assertEqual(self.test_obj.formats, ['jpg', 'png'])

    def test_formats_unsupported_format(self):
        self.exception_test(['-f', '.zzz'], ValueError)


if __name__ == '__main__':
    unittest.main()
