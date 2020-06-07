import os
import sys
import options
from PIL import Image


# Handle arguments
opt = options.Options()  # todo error handling for this section
opt.read_options(sys.argv[1:])


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
if not opt.resize == 1:
    try:
        vprint('Creating directory for compressed images')
        os.mkdir(opt.input_dir + '/compressed')
    except FileExistsError:
        vprint('Directory already exists')  # in this case the directory already exists and no action is needed
        # todo think about what to do with name collisions for existing files


def write_to_tex(los):
    # writes the collection of strings into the tex file where each string is a line
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


def compress(f_name):
    # create a compressed version of the picture with the file name f_name in input_dir and save it to compressed
    vprint('Compressing image', f_name)
    img = Image.open(opt.input_dir + '/' + f_name)
    img = img.resize((2016, 1512), Image.ANTIALIAS)  # todo implement ratio for resizing these images
    img.save(opt.input_dir + '/compressed/' + f_name, optimize=True, quality=opt.quality)


# write the preamble
write_to_tex([r'\documentclass{article}',
              r'\usepackage{incgraph}',
              r'\begin{document}'])


# for each jpg in input_dir make that a page in the tex document
ls = []
for p in opt.lop:
    vprint('Found image', p)
    if opt.resize != 1:
        compress(p)
    ls.append(r'\incgraph[paper=graphics][angle={%d}, scale=0.3]{%s}' % (opt.angle, 'compressed/' + p))

# finish and close the document
write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

# compile the document
vprint('Compiling pdf with LaTeX')
os.chdir(opt.input_dir)
os.system('pdflatex ' + opt.name)

# TODO cleanup extra files
# TODO add case for when no ratio == 1 and no cleanup of compressed is necessary
if opt.cleanup:
    vprint('Removing tex source file')
    os.remove(opt.name)  # remove tex source
    vprint('Removing aux file')
    os.remove(opt.name[:-4] + '.aux')

    if opt.resize != 1:
        vprint('Removing scaled images')
        for p in opt.lop:
            os.remove('compressed/' + p)

        # remove compressed folder if empty
        if not os.listdir('compressed'):
            os.rmdir('compressed')

