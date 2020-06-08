import os
import unittest
import options


class TestOptions(unittest.TestCase):
    def make_test_obj(self):
        self.test_obj = options.Options('test_defaults.txt')

    def exception_test(self, inputs, error):
        try:
            self.make_test_obj()
            self.test_obj.read_options(inputs)
            self.fail("No exception thrown")
        except error:
            pass  # This exception should be thrown
        except not error:
            self.fail("Wrong type of exception")

    def defaults_exception_test(self, file, error):
        try:
            options.Options(file)
            self.fail('No exception thrown')
        except error:
            pass  # This exception should be thrown
        except not error:
            self.fail('Wrong type of exception')

    def test_defaults(self):
        self.make_test_obj()
        self.assertFalse(self.test_obj.verbose)
        self.assertTrue(self.test_obj.cleanup)
        self.assertEqual(1, self.test_obj.resize)
        self.assertEqual(270, self.test_obj.angle)
        self.assertEqual(10, self.test_obj.quality)
        self.assertEqual(['.jpg', '.png'], self.test_obj.formats)

    def test_defaults_no_value(self):
        self.defaults_exception_test('test_no_value_default.txt', IndexError)

    def test_defaults_no_default_file(self):
        self.defaults_exception_test('non_existent.txt', FileNotFoundError)

    def test_defaults_missing_key(self):
        self.defaults_exception_test('test_missing_key_defaults.txt', KeyError)

    # Verbose option tests
    def test_verbose(self):
        for j in ('-v', '--verbose'):
            self.make_test_obj()
            self.assertFalse(self.test_obj.verbose)
            self.test_obj.read_options([j])
            self.assertTrue(self.test_obj.verbose)

    def test_verbose_no_switch(self):
        self.make_test_obj()
        self.assertFalse(self.test_obj.verbose)
        self.test_obj.read_options(['-z'])
        self.assertFalse(self.test_obj.verbose)

    # Quiet option test
    def test_quiet(self):
        for j in ('-q', '--quiet'):
            self.make_test_obj()
            self.test_obj.verbose = True
            self.assertTrue(self.test_obj.verbose)
            self.test_obj.read_options([j])
            self.assertFalse(self.test_obj.verbose)

    # Cleanup option test
    def test_cleanup(self):
        for j in ('-c', '--cleanup'):
            self.make_test_obj()
            self.test_obj.cleanup = False
            self.assertFalse(self.test_obj.cleanup)
            self.test_obj.read_options([j])
            self.assertTrue(self.test_obj.cleanup)

    def test_no_cleanup(self):
        for j in ('-nc', '--no-cleanup'):
            self.make_test_obj()
            self.assertTrue(self.test_obj.cleanup)
            self.test_obj.read_options([j])
            self.assertFalse(self.test_obj.cleanup)

    def test_name_default(self):
        self.make_test_obj()
        self.assertEqual(os.path.basename(os.getcwd()) + '.tex', self.test_obj.name)

    def test_name_append_tex(self):
        for j in ('-n', '--name'):
            self.make_test_obj()
            self.test_obj.read_options([j, 'test'])
            self.assertEqual('test.tex', self.test_obj.name)

    def test_name_no_append(self):
        for j in ('-n', '--name'):
            self.make_test_obj()
            self.test_obj.read_options([j, 'test.tex'])
            self.assertTrue('test.tex', self.test_obj.name)

    def test_name_input_dir_change(self):
        self.make_test_obj()
        self.test_obj.read_options(['-d', 'folder'])
        self.assertEqual('folder.tex', self.test_obj.name)

    def test_directory(self):
        for j in ('-d', '--dir', '--directory'):
            self.make_test_obj()
            self.test_obj.read_options([j, 'folder'])
            self.assertEqual('folder', self.test_obj.input_dir)
            self.assertEqual(os.listdir('folder'), self.test_obj.lop)

    def test_directory_no_input(self):
        self.exception_test(['-d'], IndexError)

    def test_directory_dne(self):
        self.exception_test(['-d', 'no_folder'], FileNotFoundError)

    def test_ratio(self):
        for j in ('-r', '--resize', '--ratio'):
            self.make_test_obj()
            self.test_obj.read_options([j, '1'])
            self.assertEqual(1, self.test_obj.resize)

    def test_ratio_no_input(self):
        self.exception_test(['-r'], IndexError)

    def test_ratio_non_float_input(self):
        self.exception_test(['-r', 'one'], ValueError)

    def test_quality(self):
        for j in ('-jq', '--quality', '--jpeg-quality'):
            self.make_test_obj()
            self.test_obj.read_options([j, '1'])
            self.assertEqual(1, self.test_obj.quality)

    def test_quality_no_input(self):
        self.exception_test(['-jq'], IndexError)

    def test_quality_non_int_input(self):
        self.exception_test(['-jq', 'one'], ValueError)

    def test_angle(self):
        for j in ('-a', '--angle'):
            self.make_test_obj()
            self.test_obj.read_options([j, '0'])
            self.assertEqual(0, self.test_obj.angle)

    def test_angle_no_input(self):
        self.exception_test(['-a'], IndexError)

    def test_angle_non_float_input(self):
        self.exception_test(['-a', 'one'], ValueError)

    def test_formats(self):
        for j in ('-f', '--formats'):
            self.make_test_obj()
            self.test_obj.read_options([j, '.jpg'])
            self.assertEqual(['.jpg'], self.test_obj.formats)

    def test_formats_add_dot(self):
        self.make_test_obj()
        self.test_obj.read_options(['-f', 'jpg'])
        self.assertEqual(['.jpg'], self.test_obj.formats)

    def test_formats_lower_and_add_dot(self):
        self.make_test_obj()
        self.test_obj.read_options(['-f', 'JPG'])
        self.assertEqual(['.jpg'], self.test_obj.formats)

    def test_formats_no_input(self):
        self.exception_test(['-f'], IndexError)

    def test_formats_break_for_other_option(self):
        self.make_test_obj()
        self.test_obj.read_options(['-f', 'jpg', '-v'])
        self.assertEqual(['.jpg'], self.test_obj.formats)

    def test_formats_many_inputs(self):
        self.make_test_obj()
        self.test_obj.read_options(['-f', '.jpg', '.png'])
        self.assertEqual(['.jpg', '.png'], self.test_obj.formats)

    def test_formats_unsupported_format(self):
        self.exception_test(['-f', '.zzz'], ValueError)


if __name__ == '__main__':
    unittest.main()
