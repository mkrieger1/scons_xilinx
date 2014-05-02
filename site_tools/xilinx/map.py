from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: .ngd -> _map.ncd, _map.mrp, .pcf
#----------------------------------------------------------

def map_targets(env, target, source):
    ngd_file = str(source[0])
    ncd_file = str(target[0])
    target.append(replace_suffix(ncd_file, '.mrp'))
    target.append(replace_suffix(ngd_file, '.pcf'))
    return target, source

def run_map(env, target, source):
    try:
        options = env['options']
    except KeyError:
        options = {}
    try:
        flags = env['flags']
    except KeyError:
        flags = []

    ngd_file = str(source[0])
    ncd_file, mrp_file, pcf_file = map(str, target)
    options['o'] = ncd_file

    opt_str = ' '.join('-%s %s' % (k, v) for (k, v) in options.iteritems())
    flag_str = ' '.join('-%s' % f for f in flags)
    
    status = env.Execute('map %s %s %s %s' % (
                         opt_str, flag_str, ngd_file, pcf_file))

    for suf in ['_summary.xml', '_usage.xml']:
        Execute(Delete(replace_suffix(ngd_file, suf)))
    # _map.xrpt is actually prefixed with the top-level module, not the
    # NGD filename -> get xst_top from env
    try:
        Execute(Delete(env['xst_top']+'_map.xrpt'))
    except KeyError:
        pass
    for suf in ['.map', '.ngm']:
        Execute(Delete(replace_suffix(ncd_file, suf)))
    Execute(Delete('_xmsgs'))

    return status

#----------------------------------------------------------

map_builder = Builder(action=run_map,
                      suffix='_map.ncd',
                      src_suffix='.ngd',
                      emitter=map_targets)

