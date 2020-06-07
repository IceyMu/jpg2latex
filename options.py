import os


class DefaultFileError(Exception):
    pass


def lower_and_add_dot(s):
    if s[0] != '.':
        return '.' + s.lower()
    else:
        return s.lower()


# TODO read  options from default file
class Options:
    def __format_names(self):
        # make the strings lowercase and add a . to the front if needed
        self.formats = list(map(lower_and_add_dot, self.formats))
        self.lop = list(filter(lambda x: x[-4:].lower() in self.formats, self.lop))

    def __init__(self, file=os.path.dirname(__file__) + '/defaults.txt'):
        self.__compatible_formats = ('.jpg', '.png')
        self.__ind = 0
        self.__skip_next = 0
        self.__name_set = False
        self.__loo = []
        self.__defaults = {}
        try:
            with open(file, 'r') as f:
                for line in f:
                    ls = line.split()
                    if ls[0] == 'formats':
                        self.__defaults['formats'] = ls[1:]
                    else:
                        self.__defaults[ls[0]] = ls[1]
        except IndexError:
            raise DefaultFileError('Index Error')  # todo differentiate these errors a custom file error is likely not needed
        except FileNotFoundError:
            raise DefaultFileError('Default file not found')

        def str_to_bool(s):
            return s and not s.lower() == 'false'

        # input_dir and name do not get an entry for default behaviour
        try:
            self.input_dir = os.getcwd()
            self.lop = os.listdir(self.input_dir)  #
            self.name = os.path.basename(os.getcwd()) + '.tex'  #
            self.verbose = str_to_bool(self.__defaults['verbose'])
            self.cleanup = str_to_bool(self.__defaults['cleanup'])
            self.resize = float(self.__defaults['ratio'])
            self.quality = int(self.__defaults['quality'])
            self.angle = float(self.__defaults['angle'])
            self.formats = self.__defaults['formats']
            self.__format_names()
        except KeyError:
            raise DefaultFileError

    def __next_arg(self):
        self.__skip_next += 1
        return self.__loo[self.__ind]

    def read_options(self, loo):
        self.__loo = loo

        for j in loo:
            self.__ind += 1

            if self.__skip_next:
                self.__skip_next -= 1
                continue

            # Quiet switch
            if j in ('-q', '--quiet'):
                self.verbose = False
                # print('Quiet option')

            elif j in ('-v', '--verbose'):
                self.verbose = True
                # print('Verbose option')

            elif j in ('-c', '--cleanup'):
                self.cleanup = True
                # print('Cleanup option')

            elif j in ('-nc', '--no-cleanup'):
                self.cleanup = False
                # print('No Cleanup option')

            elif j in ('-n', '--name'):
                self.name = self.__next_arg()
                self.__name_set = True
                # print("Name option with: ", self.name)

            elif j in ('-d', '--dir', '--directory'):
                self.input_dir = self.__next_arg()
                # print("Directory option with:", self.input_dir)
                self.lop = os.listdir(self.input_dir)

            elif j in ('-r', '--resize', '--ratio'):
                self.resize = float(self.__next_arg())
                # print('Resize option with:', self.ratio)

            elif j in ('-jq', '--quality', '--jpeg-quality'):
                self.quality = int(self.__next_arg())  # This value must be an integer to work with PIL
                # print('Compression quality option with:', self.quality)

            elif j in ('-a', '--angle'):
                self.angle = float(self.__next_arg())  # This needs to be a float to work with incgraph
                # print('Angle option with:', self.angle)

            elif j in ('-f', '--formats'):  # only compatible formats with both PIL and incgraph are jpg and png
                self.formats = []
                rest = loo[self.__ind:]

                if not rest:
                    raise IndexError

                for s in rest:
                    if s[0] == '-':
                        break
                    else:
                        s = lower_and_add_dot(s)
                        if s in self.__compatible_formats:  # s needs to be lowered and have a dot added
                            self.formats.append(s)
                            self.__skip_next += 1
                            continue
                    raise ValueError

            """
            except IndexError:
                print('No value given for', j, 'option')
                # exit(1)
            except FileNotFoundError:
                print('Directory ', self.input_dir, 'not found')
                # exit(1)
        """

        self.__format_names()

        if not self.__name_set:
            self.name = os.path.basename(self.input_dir)

        if self.name[-4:] != '.tex':
            self.name += '.tex'
