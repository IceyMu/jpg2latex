""" Python script for compiling images into a single pdf using latex. See help.txt for usage"""

import os
import options
import subprocess
from PIL import Image


def main(opt):
    # Use the source images directly in the pdf if the images will not be changed
    if opt.resize == 1 and opt.quality == 100:
        preserve_image = True
    else:
        preserve_image = False

    def vprint(*args):
        """use the built-in print function if opt.verbose is set to True"""
        if opt.verbose:
            print(*tuple(map(str, args)))

    # Print run options
    vprint('Input directory:', opt.input_dir)
    vprint('Output name:', opt.name)
    vprint('Verbose:', opt.verbose)
    vprint('Cleanup:', opt.cleanup)
    vprint('Resize:', opt.resize)
    vprint('Quality:', opt.quality)
    vprint('Angle:', opt.angle)
    vprint('Formats', opt.formats)

    # Create latex source file
    path = opt.input_dir + '/' + opt.name
    vprint('Creating file', path)
    tex = open(path, 'w')

    # Create directory for compressed images
    if not preserve_image and not os.path.exists(opt.input_dir + '/compressed'):
        vprint('Creating directory for compressed images')
        os.mkdir(opt.input_dir + '/compressed')

    def write_to_tex(los):
        """Writes the collection of strings into the tex file where each element is a line"""
        nonlocal tex
        s = '\n'.join(los + ['\n'])
        tex.write(s)

    def resize(f_name):
        """
        resize(f_name)

            Resize the image with the file name f_name in the folder opt.input_dir
            to be opt.resize times the resolution and set the quality of the jpg
            compression algorithm to opt.quality and save the result to
            opt.input_dir/compressed
        """
        vprint('Compressing image', f_name)
        img = Image.open(opt.input_dir + '/' + f_name)
        dims = tuple(map(lambda x: int(x * opt.resize), img.size))

        img = img.resize(dims, Image.ANTIALIAS)
        if f_name[-4:].lower() == '.jpg':
            img.save(opt.input_dir + '/compressed/' + f_name, optimize=True, quality=opt.quality)
        else:
            img.save(opt.input_dir + '/compressed/' + f_name, optimize=True)

    # Write the preamble
    write_to_tex([r'\documentclass{article}',
                  r'\usepackage{incgraph}',
                  r'\begin{document}'])

    # Make each image a page in the tex document
    ls = []
    zero_size_images = []
    for p in opt.lop:
        vprint('Found image', p)
        if not preserve_image:
            try:
                resize(p)
                p = 'compressed/' + p
            except ValueError:
                vprint('Value for resize caused', p, 'to have zero size')
                zero_size_images.append(p)
                continue
        ls.append(r'\incgraph[paper=graphics][angle={%d}, scale=0.3]{%s}' % (opt.angle, p))

    for p in zero_size_images:
        opt.lop.remove(p)

    # Finish and close the latex source
    write_to_tex(ls)
    tex.write(r'\end{document}')
    tex.close()

    # compile the document
    vprint('Compiling pdf with LaTeX')
    os.chdir(opt.input_dir)
    with open(os.devnull, 'wb') as devnull:
        try:
            subprocess.check_call('pdflatex ' + opt.name, stdout=devnull)
        except subprocess.CalledProcessError:
            print('There was an error with latex check {}.log error information.'.format(opt.name[:-4]))

    # Cleanup extra files that this script creates
    if opt.cleanup:
        vprint('Removing tex source file')
        os.remove(opt.name)  # remove tex source
        vprint('Removing aux file')
        os.remove(opt.name[:-4] + '.aux')
        vprint('Removing log file')
        os.remove(opt.name[:-4] + '.log')

        if not preserve_image:
            vprint('Removing scaled images')
            for p in opt.lop:
                os.remove('compressed/' + p)

            # remove compressed folder if empty
            if not os.listdir('compressed'):
                os.rmdir('compressed')


if __name__ == '__main__':
    import sys

    # Create options object and read from defaults file
    try:
        opt = options.Options()
        opt.read_options(sys.argv[1:])
        main(opt)
    except IndexError or FileNotFoundError or ValueError as e:
        print(e)
        exit(1)
