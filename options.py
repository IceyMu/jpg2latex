import os


# TODO read  options from default file
class Options:
    def __init__(self, s=1, r=1, q=0.85, a=270, f=['.png'], v=True, c=True,
                 d=os.getcwd(), n=os.path.basename(os.getcwd()) + '.tex'):

        self.input_dir = d
        self.verbose = v
        self.cleanup = c
        self.name = n
        self.scale = s
        self.ratio = r
        self.quality = q  # 0.85
        self.angle = a  # 270
        self.formats = f
        self.lop = os.listdir(self.input_dir)

        self.__ind = 0
        self.__skip_next = 0
        self.__name_set = False
        self.__loo = []

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
                print('Quiet option')

            elif j in ('-v', '--verbose'):
                self.verbose = True
                print('Verbose option')

            elif j in ('-c', '--cleanup'):
                self.cleanup = True
                print('Cleanup option')

            elif j in ('-nc', '--no-cleanup'):
                self.cleanup = False
                print('No Cleanup option')

            elif j in ('-n', '--name'):
                self.name = self.__next_arg()
                self.__name_set = True
                print("Name option with: ", self.name)

            elif j in ('-d', '--dir', '--directory'):
                self.input_dir = self.__next_arg()
                print("Directory option with:", self.input_dir)
                self.lop = os.listdir(self.input_dir)

            elif j in ('-s', '--scale'):
                self.scale = self.__next_arg()
                print("Scale option with: ", self.scale)

            elif j in ('-r', '--resize', '--ratio'):
                self.ratio = self.__next_arg()
                print('Resize option with:', self.ratio)

            elif j in ('-cq', '--quality', '--compression-quality'):
                self.quality = self.__next_arg()
                print('Compression quality option with:', self.quality)

            elif j in ('-a', '--angle'):
                self.angle = self.__next_arg()
                print('Angle option with:', self.angle)

            elif j in ('-f', '--formats'):
                self.formats = []
                for s in loo[self.__ind:]:
                    if s[0] == '-':
                        break
                    else:
                        self.formats.append(self.__next_arg())

                print('Formats set as: ', self.formats)

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
