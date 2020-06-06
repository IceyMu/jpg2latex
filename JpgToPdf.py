import os
import sys
import options
from PIL import Image

# Handle arguments
opt = options.Options().read_options(sys.argv[1:])

path = opt.input_dir + '/' + opt.name
tex = open(path, 'w')

# Create directory for compressed images
try:
    os.mkdir(opt.input_dir + '/compressed')
except FileExistsError:
    pass  # in this case the directory already exists and no action is needed


def write_to_tex(los):
    # writes the collection of strings into the tex file where each string is a line
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


def compress(f_name):
    # create a compressed version of the picture with the file name f_name in input_dir and save it to compressed
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
    if not p[-4:].lower() == '.jpg':
        continue
    else:
        print(p)
        compress(p)
        ls.append(r'\incgraph[paper=graphics][angle={%d}, scale=0.3]{%s}' % (opt.angle, 'compressed/' + p))

# finish and close the document
write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

# compile the document
os.chdir(opt.input_dir)
os.system('pdflatex ' + opt.name)
