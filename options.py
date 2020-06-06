import os


# TODO read  options from default file
class Options:
    def __init__(self, r=1, q=0.85, a=270, f=['.png'], v=True, c=True,
                 d=os.getcwd(), n=os.path.basename(os.getcwd()) + '.tex'):

        self.__compatible_formats = ('jpg', 'png')
        self.__ind = 0
        self.__skip_next = 0
        self.__name_set = False
        self.__loo = []

        # TODO we don't need so many parameters just initialize them here by reading from the defaults file
        # the parameters were created to aid testing but they are not used
        self.defaults = {}
        with open('defaults.txt', 'r') as f:
            for line in f:
                (key, val) = line.split()
                self.defaults[str(key)] = val

        # input_dir and name do not get an entry for default behaviour
        try:
            self.input_dir = os.getcwd()
            self.lop = os.listdir(self.input_dir)
            self.name = os.path.basename(os.getcwd()) + '.tex'
            self.verbose = self.defaults['verbose']
            self.cleanup = self.defaults['cleanup']
            self.name = self.defaults['name']
            self.ratio = self.defaults['ratio']
            self.quality = self.defaults['quality']  # 0.85
            self.angle = self.defaults['angle']  # 270
            self.formats = self.defaults['formats']
        except KeyError:
            pass  # todo add error behaviour for incorrect keys

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
