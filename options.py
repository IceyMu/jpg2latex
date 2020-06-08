import os


def lower_and_add_dot(s):
    if s[0] != '.':
        return '.' + s.lower()
    else:
        return s.lower()


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
            raise IndexError(str(ls[0]))
        # throws IndexError and FileNotFoundError

        def str_to_bool(s):
            return s and not s.lower() == 'false'

        # input_dir and name do not get an entry for default behaviour

        self.input_dir = os.getcwd()
        self.lop = os.listdir(self.input_dir)
        self.name = os.path.basename(os.getcwd()) + '.tex'
        self.verbose = str_to_bool(self.__defaults['verbose'])
        self.cleanup = str_to_bool(self.__defaults['cleanup'])
        self.resize = float(self.__defaults['resize'])
        self.quality = int(self.__defaults['quality'])
        self.angle = float(self.__defaults['angle'])
        self.formats = self.__defaults['formats']
        self.__format_names()

        # throws KeyError

    def __next_arg(self):
        self.__skip_next += 1
        return self.__loo[self.__ind]

    def read_options(self, loo):
        self.__loo = loo

        try:
            for j in loo:
                self.__ind += 1

                if self.__skip_next:
                    self.__skip_next -= 1
                    continue

                # Quiet switch
                if j in ('-q', '--quiet'):
                    self.verbose = False

                elif j in ('-v', '--verbose'):
                    self.verbose = True

                elif j in ('-c', '--cleanup'):
                    self.cleanup = True

                elif j in ('-nc', '--no-cleanup'):
                    self.cleanup = False

                elif j in ('-n', '--name'):
                    self.name = self.__next_arg()
                    self.__name_set = True

                elif j in ('-d', '--dir', '--directory'):
                    self.input_dir = self.__next_arg()
                    self.lop = os.listdir(self.input_dir)

                elif j in ('-r', '--resize', '--ratio'):
                    self.resize = float(self.__next_arg())

                elif j in ('-jq', '--quality', '--jpeg-quality'):
                    self.quality = int(self.__next_arg())  # This value must be an integer to work with PIL

                elif j in ('-a', '--angle'):
                    self.angle = float(self.__next_arg())  # This needs to be a float to work with incgraph

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

        except IndexError:
            raise IndexError('No value given for', j, 'option')
        except FileNotFoundError:
            raise FileNotFoundError('Directory ', self.input_dir, 'not found')

        self.__format_names()

        if not self.__name_set:
            self.name = os.path.basename(self.input_dir)

        if self.name[-4:] != '.tex':
            self.name += '.tex'
