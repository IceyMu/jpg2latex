import os
import sys
import options
from PIL import Image

# Handle arguments
try:
    opt = options.Options()
except IndexError as e:
    print('Defaults file missing a value for ', e)
    exit(1)
except FileNotFoundError:
    print('File defaults.txt not found')
    exit(1)
except ValueError:
    print('Wrong data type for one of the options in the defaults file')
    exit(1)

try:
    opt.read_options(sys.argv[1:])
except IndexError as e:
    print(e)
    exit(1)
except FileNotFoundError as e:
    print(e)
    exit(1)


if opt.resize == 1 and opt.quality == 100:
    preserve_image = True
else:
    preserve_image = False


def vprint(*args):
    if opt.verbose:
        print(*tuple(map(str, args)))


# print run options
vprint('Input directory:', opt.input_dir)
vprint('Output name:', opt.name)
vprint('Verbose:', opt.verbose)
vprint('Cleanup:', opt.cleanup)
vprint('Resize:', opt.resize)
vprint('Quality:', opt.quality)
vprint('Angle:', opt.angle)
vprint('Formats', opt.formats)

path = opt.input_dir + '/' + opt.name
vprint('Creating file', path)
tex = open(path, 'w')

# Create directory for compressed images
if not preserve_image:
    try:
        vprint('Creating directory for compressed images')
        os.mkdir(opt.input_dir + '/compressed')
    except FileExistsError:
        vprint('Directory already exists')  # in this case the directory already exists and no action is needed


def write_to_tex(los):
    # writes the collection of strings into the tex file where each string is a line
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


def compress(f_name):
    # create a compressed version of the picture with the file name f_name in input_dir and save it to compressed
    vprint('Compressing image', f_name)
    img = Image.open(opt.input_dir + '/' + f_name)
    dims = tuple(map(lambda x: int(x * opt.resize), img.size))

    img = img.resize(dims, Image.ANTIALIAS)
    if f_name[-4:].lower() == '.jpg':
        img.save(opt.input_dir + '/compressed/' + f_name, optimize=True, quality=opt.quality)
    else:
        img.save(opt.input_dir + '/compressed/' + f_name, optimize=True)


# write the preamble
write_to_tex([r'\documentclass{article}',
              r'\usepackage{incgraph}',
              r'\begin{document}'])


# for each jpg in input_dir make that a page in the tex document
ls = []
for p in opt.lop:
    vprint('Found image', p)
    if not preserve_image:
        try:
            compress(p)
        except ValueError:
            vprint('Value for resize caused ', p, ' to have zero size')
            continue
    ls.append(r'\incgraph[paper=graphics][angle={%d}, scale=0.3]{%s}' % (opt.angle, 'compressed/' + p))

# finish and close the document
write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

# compile the document
vprint('Compiling pdf with LaTeX')
os.chdir(opt.input_dir)
os.system('pdflatex ' + opt.name)

if opt.cleanup:
    vprint('Removing tex source file')
    os.remove(opt.name)  # remove tex source
    vprint('Removing aux file')
    os.remove(opt.name[:-4] + '.aux')

    if not preserve_image:
        vprint('Removing scaled images')
        for p in opt.lop:
            os.remove('compressed/' + p)

        # remove compressed folder if empty
        if not os.listdir('compressed'):
            os.rmdir('compressed')
