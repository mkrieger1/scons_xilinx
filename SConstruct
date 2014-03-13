# ex: set syntax=python:

from os import listdir
from os.path import join, expanduser

AddOption('--user', dest='user', action='store_true')

path = (expanduser('~/.scons')
        if GetOption('user') else '/usr/share/scons')

target = [join(path, 'site_scons/site_tools/xilinx')]
source = [join('xilinx', f) for f in listdir('xilinx')]

Alias('install', Install(target, source))

