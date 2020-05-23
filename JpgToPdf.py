import os
import sys
import options
from PIL import Image

# Handle arguments
options.read_options(sys.argv[1:])

# Print variables for testing
#print('input_dir: ', input_dir)
#print('verbose: ', verbose)
#print('cleanup ', cleanup)
#print('name ', name)
#print('scale', scale)
#print('quality', quality)
#print('angle', angle)
#print('formats', formats)
#print('lop', lop)

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
        ls.append(r'\incgraph[paper=graphics][angle={%d}, scale=0.3]{%s}' % (angle, 'compressed/' + p))

# finish and close the document
write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

# compile the document
os.chdir(input_dir)
os.system('pdflatex ' + name)
