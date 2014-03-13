# ex: set syntax=python:

from os import listdir
from os.path import join, expanduser

loc_user = expanduser('~/.scons/site_scons')
loc_sys = '/usr/share/scons/site_scons'

AddOption('--user', dest='site', action='store_const', const=loc_user)
AddOption('--prefix', dest='site', action='store', default=loc_sys)
# resulting priority of options:
# if --prefix=foo --> foo
# elif --user     --> loc_user
# else            --> loc_sys

source_dir = 'site_tools/xilinx'
target = [join(GetOption('site'), source_dir)]
source = [join(source_dir, f) for f in listdir(source_dir)]

Alias('install', Install(target, source))

