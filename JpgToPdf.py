import os
from PIL import Image

cwd = os.getcwd()
input_dir = ''

# Get directory for jpg files
while input_dir == '':
    try:
        print(cwd)
        input_dir = input('Input Dir:' )

        name_input = input('Name: ')
        if name_input != '':
            name = name_input + '.tex'
        else:
            name = input_dir + '.tex'

        lop = os.listdir(input_dir)
    except OSError:
        print('Invalid dir')
        input_dir = ''

path = input_dir + '/' + name
tex = open(path, 'w')

# Create directory for compressed images
try:
    os.mkdir(input_dir + '/compressed')
except FileExistsError:
    pass


def write_to_tex(los):
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


def compress(f_name):
    img = Image.open(input_dir + '/' + f_name)
    img = img.resize((2016, 1512), Image.ANTIALIAS)
    img.save(input_dir + '/compressed/' + f_name, optimize=True, quality=85)


write_to_tex([r'\documentclass{article}',
              r'\usepackage{incgraph}',
              r'\begin{document}'])


ls = []
for p in lop:
    if p[-4:] not in ('.jpg', '.JPG'):
        continue
    else:
        print(p)
        compress(p)
        ls.append(r'\incgraph[paper=graphics][angle=270, scale=0.3]{%s}' % ('compressed/' + p))

write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

os.chdir(input_dir)
os.system('pdflatex ' + name)
