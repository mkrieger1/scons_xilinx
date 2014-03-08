from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: _map.ncd, .pcf -> .ncd, .par
#----------------------------------------------------------

def par_emitter(env, target, source):
    ncd_file = str(target[0])
    target.append(replace_suffix(ncd_file, '.par'))
    source.append(replace_suffix(ncd_file, '.pcf'))
    return target, source

def run_par(env, target, source):
    try:
        options = env['options']
    except KeyError:
        options = {}
    try:
        flags = env['flags']
    except KeyError:
        flags = []

    ncd_map, pcf_file = map(str, source)
    ncd_file, par_file = map(str, target)

    opt_str = ' '.join('-%s %s' % (k, options[k]) for k in options)
    flag_str = ' '.join('-%s' % f for f in flags)
    
    env.Execute('par %s %s %s %s %s' % (opt_str, flag_str,
                                        ncd_map, ncd_file, pcf_file))

    #for suf in ['.map', '_map.xrpt', '.ngm',
    #            '_summary.xml', '_usage.xml']:
    #    Execute(Delete(replace_suffix(ncd_file, suf)))
    #Execute(Delete('_xmsgs'))

#----------------------------------------------------------

def generate(env, **kw):
    par_builder = Builder(action=run_par,
                          suffix='.ncd',
                          src_suffix='_map.ncd',
                          emitter=par_emitter)

    env.Append(BUILDERS={'PlaceRoute': par_builder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('par')

