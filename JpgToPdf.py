import os
import sys
from PIL import Image

# Default options
input_dir = os.getcwd()
verbose = True  # TODO read  options from default files
cleanup = False
scale = 1
quality = 0.85
formats = ['.jpg']

# Handle arguments
sys.argv = sys.argv[1:]

ind = 0
skip_next = False
name_set = False


def next_arg():
    global skip_next
    skip_next = True
    return sys.argv[ind]


for j in sys.argv:
    ind += 1

    if skip_next:
        skip_next = False
        continue

    try:
        # Quiet switch
        if j in ('-q', '--quiet'):
            verbose = True
            print('Quiet option')

        elif j in ('-v', '--verbose'):
            verbose = False
            print('Verbose option')

        elif j in ('-c', '--cleanup'):
            cleanup = True
            print('Cleanup option')

        elif j in ('-nc', '--no-cleanup'):
            cleanup = False
            print('No Cleanup option')

        elif j in ('-n', '--name'):
            name = next_arg()
            name_set = True
            print("Name option with: ", name)

        elif j in ('-d', '--dir', '--directory'):
            input_dir = next_arg()
            print("Directory option with:", input_dir)
            lop = os.listdir(input_dir)

        elif j in ('-s', '--scale'):
            scale = next_arg()
            print("Scale option with: ", scale)

        elif j in ('-r', '--resize', '--ratio'):
            ratio = next_arg()
            print('Resize option with:', ratio)

        # quality option
        elif j in ('-cq', '--quality', '--compression-quality'):
            quality = next_arg()
            print('Compression quality option with:', quality)

        elif j in ('-f', '--formats'):
            print('Formats set as: ')

    except IndexError:
        print('No value given for', j, 'option')
        exit(1)
    except FileNotFoundError:
        print('Directory ', input_dir, 'not found')
        exit(1)

for j in range(len(formats)):
    formats[j] = formats[j].lower()

if not name_set:
    name = os.path.basename(input_dir)

if name[:-4] != '.tex':
    name += '.tex'

exit(0)

path = input_dir + '/' + name
tex = open(path, 'w')

# Create directory for compressed images
try:
    os.mkdir(input_dir + '/compressed')
except FileExistsError:
    pass  # in this case the directory already exists and no action is needed


def write_to_tex(los):
    # writes the collection of strings into the tex file where each string is a line
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


def compress(f_name):
    # create a compressed version of the picture with the file name f_name in input_dir and save it to compressed
    img = Image.open(input_dir + '/' + f_name)
    img = img.resize((2016, 1512), Image.ANTIALIAS)
    img.save(input_dir + '/compressed/' + f_name, optimize=True, quality=quality)


# write the preamble
write_to_tex([r'\documentclass{article}',
              r'\usepackage{incgraph}',
              r'\begin{document}'])


# for each jpg in input_dir make that a page in the tex document
ls = []
for p in lop:
    if not p[-4:].lower() == '.jpg':
        continue
    else:
        print(p)
        compress(p)
        ls.append(r'\incgraph[paper=graphics][angle=270, scale=0.3]{%s}' % ('compressed/' + p))

# finish and close the document
write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

# compile the document
os.chdir(input_dir)
os.system('pdflatex ' + name)
