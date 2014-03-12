# ex: set syntax=python:

from os import listdir, environ
from os.path import join, expanduser

env = Environment(ENV=environ)


# installation of xilinx build tools

AddOption('--user', dest='user', action='store_true')

path = (expanduser('~/.scons')
        if GetOption('user') else '/usr/share/scons')

target = [join(path, 'site_scons/site_tools/xilinx')]
source = [join('xilinx', f) for f in listdir('xilinx')]

Alias('install', Install(target, source))


# build readme

readme_html = env.Command('readme.html', 'readme.rst',
                          'rst2html.py $SOURCE > $TARGET')
Alias('doc', readme_html)
Default(None) # must explicitly call `scons doc`

