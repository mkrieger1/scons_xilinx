from subprocess import check_output
from os.path import expanduser

base = ['scons', 'install', '-n', '-Q']
def output(args):
    return check_output(base+args).strip()

assert(output([]) == '/usr/share/scons')
assert(output(['--user']) == expanduser('~/.scons'))
assert(output(['--location=spam']) == 'spam')
assert(output(['--user', '--location=spam']) == 'spam')
assert(output(['--location=spam', '--user']) == 'spam')

print 'all tests passed'
