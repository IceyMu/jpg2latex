""" Class for interpreting command-line options"""

import os


def lower_and_add_dot(s):
    """
    lower_and_add_dot(s)

        Returns the given string in all lowercase and adds a . to the beginning
        if there was not already one.
    """
    if s[0] != '.':
        return '.' + s.lower()
    else:
        return s.lower()


class Options:
    """
    Options(file)

        An object representing all of the settings for creating a pdf in the
        script JpgToLatex.py when this object is initialized the options are
        read from a text file given in the only argument.

        Parameters:
            file: (String) Path to a text file to read options from.

        Attributes:
            input_dir: (String) Path to the directory containing the images to
                turn into a pdf.
            lop: (List[String]) List of filenames of the images in input_dir
            name: (String) Name of the tex source file used to compile the pdf
                this always ends in '.tex' and so the name of the pdf will be
                name[:-4].
            verbose: (Boolean) Boolean representing if the program should print
                messages about actions it takes
            cleanup: (Boolean) Boolean representing if the program should
                delete the latex files and modified images when it's done with
                them.
            sort: (Boolean) Boolean representing if lop should be sorted
                alphabetically. If False images will be ordered as given by the
                operating system.
            resize: (Float) Number representing the amount to scale the
                resolution of images e.g a value of 0.5 will scale a 100x100
                source image to 50x50 in the pdf.
            quality: (Int) Represents the jpg compression quality when
                resizing jpg images, value should be in [1, 95] see PIL
                documentation for more information.
            angle: (Float) Angle to rotate images on the pdf, 270 represents
                no rotation, increasing the value rotates the image
                counter-clockwise.
            formats: (List[String]) List of Strings representing the image
                formats to use. Currently only possible elements are '.jpg'
                and '.pdf'

        Notes:
            Setting the value of resize to 1 and quality to 100 will cause the
            the program to use the source images directly.

            The format for a text file to use as the defaults file is to have
            the words: verbose, cleanup, resize, quality, angle, and formats
            on separate lines followed by their values and separated by
            whitespace, order is not important any other lines will be ignored.
                To set verbose and cleanup to false by default you must write
            false (non case sensitive)
    """
    def __format_names(self):
        """
        __format_names()

            Modifies the strings in self.formats and self.lop such that file
            extensions are lowercase and have a .
        """
        self.formats = list(map(lower_and_add_dot, self.formats))
        self.lop = list(filter(lambda x: x[-4:].lower() in self.formats, self.lop))

    def __init__(self, file=os.path.dirname(__file__) + '/defaults.txt'):
        """
        __init__([file=os.path.dirname(__file__) + '/defaults.txt'])

            Initializes the Options object with the options provided in the
            text file at file, by default it looks in defaults.txt see class
            documentation for details on how to format the file.

            Raises:
                IndexError: Raised when an option is not given a value
                FileNotFoundError: Raised when no file is found at the path
                    given.
                KeyError: Raised when one of the options is missing
        """
        self.__compatible_formats = ('.jpg', '.png')
        self.__name_set = False
        self.__loo = []
        self.__defaults = {}

        def str_to_bool(s):
            """
            str_to_bool(s)

                Returns false if the given string is "false" (non case-sensitive)
                or if the string is empty returns True otherwise.
            """
            return s and not s.lower() == 'false'

        # Read default options
        try:
            with open(file, 'r') as f:
                for line in f:
                    ls = line.split()
                    if ls[0] == 'formats':
                        self.__defaults['formats'] = ls[1:]
                    else:
                        self.__defaults[ls[0]] = ls[1]

            # unpack dictionary into the appropriate attributes
            self.input_dir = os.getcwd()
            self.lop = os.listdir(self.input_dir)
            self.name = os.path.basename(os.getcwd()) + '.tex'
            self.verbose = str_to_bool(self.__defaults['verbose'])
            self.cleanup = str_to_bool(self.__defaults['cleanup'])
            self.sort = str_to_bool(self.__defaults['sort'])
            self.resize = float(self.__defaults['resize'])
            self.quality = int(self.__defaults['quality'])
            self.angle = float(self.__defaults['angle'])
            self.formats = self.__defaults['formats']
            self.__format_names()

        except IndexError:
            raise IndexError('Defaults file missing a value for ' + str(ls[0]))
        except FileNotFoundError:
            raise FileNotFoundError('File {} not found'.format(file))
        except ValueError:
            raise ValueError('Wrong data type for one of the options in the defaults file')

    def read_options(self, los):
        """
        read_options(los)

            Interprets a list of strings and changes the options using the following commands

            -v, --verbose
                Sets Verbose to True.

            -q, --quiet
                Sets verbose to False.

            -c, --cleanup
                Sets cleanup to True.

            -nc, --no-cleanup
                Sets cleanup to False.

            -s, --sort
                Sets sort to True

            -ns --no-sort
                Sets sort to False

            -n, --name
                Sets name to the following argument.

            -d, -dir, --directory
                Sets input_dir to the path given by the following argument.

            -r, --resize, --ratio
                Sets resize to the following argument interpreted as a Float.

            -jq, --quality, --jpeg-quality
                Sets quality to the following argument interpreted as
                an integer value should be in [1, 95] see PIL documentation
                for more information.

            -a, --angle
                Sets the angle to the following argument interpreted as a
                float.

            -f, --formats
                Sets formats to the list of the remaining arguments up until
                the next one that starts with a '-' this method will
                automatically make the entries lowercase and begin with a '.'
                currently the only supported formats are .jpg and .png


            Raises:
                IndexError: Raised when when a switch that needs another
                    value is given at the end of the list.
                FileNotFoundError: Raised when the directory path given after
                    the -d option cannot be found.
                ValueError: Raised when an unsupported format is given for the
                    -f option, also raised when the wrong data type is given
                    for an option.
        """
        skip_next = 0
        ind = 0

        def __next_arg():
            nonlocal skip_next, ind
            skip_next += 1
            return los[ind]

        try:
            for j in los:
                ind += 1

                if skip_next:
                    skip_next -= 1
                    continue

                if j in ('-v', '--verbose'):
                    self.verbose = True

                elif j in ('-q', '--quiet'):
                    self.verbose = False

                elif j in ('-c', '--cleanup'):
                    self.cleanup = True

                elif j in ('-nc', '--no-cleanup'):
                    self.cleanup = False

                elif j in ('-s', '--sort'):
                    self.sort = True

                elif j in ('-ns', '--no-sort'):
                    self.sort = False

                elif j in ('-n', '--name'):
                    self.name = __next_arg()
                    self.__name_set = True

                elif j in ('-d', '--dir', '--directory'):
                    self.input_dir = __next_arg()
                    self.lop = os.listdir(self.input_dir)

                elif j in ('-r', '--resize', '--ratio'):
                    self.resize = float(__next_arg())

                elif j in ('-jq', '--quality', '--jpeg-quality'):
                    self.quality = int(__next_arg())  # This value must be an integer to work with PIL

                elif j in ('-a', '--angle'):
                    self.angle = float(__next_arg())

                elif j in ('-f', '--formats'):  # only compatible formats with both PIL and incgraph are jpg and png
                    self.formats = []
                    rest = los[ind:]

                    if not rest:
                        raise IndexError

                    for s in rest:
                        if s[0] == '-':
                            break
                        else:
                            s = lower_and_add_dot(s)
                            if s in self.__compatible_formats:
                                self.formats.append(s)
                                skip_next += 1
                                continue
                            raise ValueError('Unsupported format ', s)

        except IndexError:
            raise IndexError('No value given for', j, 'option')
        except FileNotFoundError:
            raise FileNotFoundError('Directory ', self.input_dir, 'not found')

        # ensure all strings follow the correct format
        self.__format_names()

        # unless a name was given use the directory as the default name
        if not self.__name_set:
            self.name = os.path.basename(self.input_dir)

        if self.name[-4:] != '.tex':
            self.name += '.tex'

        # sort lop alphabetically if needed
        if self.sort:
            self.lop.sort()
