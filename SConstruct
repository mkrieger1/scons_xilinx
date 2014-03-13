# ex: set syntax=python:

from os import listdir
from os.path import join, expanduser

loc_user = expanduser('~/.scons')
loc_sys = '/usr/share/scons'

AddOption('--user', dest='location', action='store_const', const=loc_user)
AddOption('--location', dest='location', action='store', default=loc_sys)
# resulting priority of options:
# if --location=foo --> foo
# elif --user       --> loc_user
# else              --> loc_sys

target = [join(GetOption('location'), 'site_scons/site_tools/xilinx')]
source = [join('xilinx', f) for f in listdir('xilinx')]

Alias('install', Install(target, source))

