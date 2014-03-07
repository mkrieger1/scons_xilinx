from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: .ngc files + .ucf -> .ngd, .bld
#----------------------------------------------------------

enforced_options = ['sd', 'uc']

def ngdbuild_emitter(env, target, source):
    bld_file = replace_suffix(str(target[0]), '.bld')
    target.append(bld_file)
    source.extend(env['ucf_files'])
    if 'search_dirs' in env:
        source.extend(map(Dir, env['search_dirs']))
    return target, source

def run_ngdbuild(env, target, source):
    options = env['options']
    for k in enforced_options:
        if k in options:
            del options[k]
    tmpdir = tempfile.mkdtemp(dir='.')
    options['dd'] = tmpdir

    opt_list = list(options.iteritems())
    opt_list.extend(('uc', f) for f in env['ucf_files'])
    if 'search_dirs' in env:
        opt_list.extend(('sd', d) for d in env['search_dirs'])
    opt_str = ' '.join('-%s %s' % (k, v) for (k, v) in opt_list)
    
    ngc_file = str(source[0])
    ngd_file, bld_file = map(str, target)
    env.Execute('ngdbuild %s %s %s' % (opt_str, ngc_file, ngd_file))

    Execute(Delete(tmpdir))
    Execute(Delete(replace_suffix(ngc_file, '_ngdbuild.xrpt')))
    Execute(Delete('xlnx_auto_0_xdb'))
    Execute(Delete('_xmsgs'))


#----------------------------------------------------------

def generate(env, **kw):
    ngdbuilder = Builder(action=run_ngdbuild,
                         suffix='.ngd',
                         src_suffix='.ngc',
                         emitter=ngdbuild_emitter)

    env.Append(BUILDERS={'NgdBuild': ngdbuilder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('ngdbuild')

