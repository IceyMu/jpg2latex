import os

cwd = os.getcwd()
input_dir = ''

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


def write_to_tex(los):
    global tex
    s = '\n'.join(los + ['\n'])
    tex.write(s)


write_to_tex([r'\documentclass{article}',
              r'\usepackage{incgraph, tikz}',
              r'\begin{document}'])


ls = []
for p in lop:
    if p[-4:] not in ('.jpg', '.JPG'):
        continue
    else:
        print(p)
        ls.append(r'\incgraph[paper=graphics][angle=270, scale=0.3]{%s}' % p)

write_to_tex(ls)
tex.write(r'\end{document}')
tex.close()

os.chdir(input_dir)
os.system('pdflatex ' + name)
