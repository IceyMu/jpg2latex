import os


class DefaultFileError(Exception):
    pass


# TODO read  options from default file
class Options:
    def __init__(self, file='defaults.txt'):

        self.__compatible_formats = ('jpg', 'png')
        self.__ind = 0
        self.__skip_next = 0
        self.__name_set = False
        self.__loo = []

        self.defaults = {}
        try:
            with open(file, 'r') as f:
                for line in f:
                    ls = line.split()
                    if ls[0] == 'formats':
                        self.defaults['formats'] = ls[1:]
                    else:
                        self.defaults[ls[0]] = ls[1]
        except IndexError:
            raise DefaultFileError
        except FileNotFoundError:
            raise DefaultFileError

        def str_to_bool(s):
            return s and not s.lower() == 'false'

        # input_dir and name do not get an entry for default behaviour
        try:
            self.input_dir = os.getcwd()
            self.lop = os.listdir(self.input_dir)
            self.name = os.path.basename(os.getcwd()) + '.tex'
            self.verbose = str_to_bool(self.defaults['verbose'])
            self.cleanup = str_to_bool(self.defaults['cleanup'])
            self.ratio = float(self.defaults['ratio'])
            self.quality = int(self.defaults['quality'])
            self.angle = float(self.defaults['angle'])
            self.formats = self.defaults['formats']
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
                self.ratio = float(self.__next_arg())
                # print('Resize option with:', self.ratio)

            elif j in ('-cq', '--quality', '--compression-quality'):
                self.quality = int(self.__next_arg())  # This value must be an integer to work with PIL
                # print('Compression quality option with:', self.quality)

            elif j in ('-a', '--angle'):
                self.angle = float(self.__next_arg())  # This needs to be a float to work with incgraph
                # print('Angle option with:', self.angle)

            elif j in ('-f', '--formats'):  # only compatible formats with both PIL and incgraph are jpg and png
                self.formats = []
                rest = loo[self.__ind]

                if not rest:
                    raise IndexError

                for s in loo[self.__ind:]:
                    if s[0] == '-':
                        break
                    elif s in self.__compatible_formats:
                        self.formats.append(s)
                        self.__skip_next += 1
                    else:
                        raise ValueError

            """
            except IndexError:
                print('No value given for', j, 'option')
                # exit(1)
            except FileNotFoundError:
                print('Directory ', self.input_dir, 'not found')
                # exit(1)
        """

        for j in range(len(self.formats)):
            self.formats[j] = self.formats[j].lower()

        if not self.__name_set:
            self.name = os.path.basename(self.input_dir)

        if self.name[-4:] != '.tex':
            self.name += '.tex'
