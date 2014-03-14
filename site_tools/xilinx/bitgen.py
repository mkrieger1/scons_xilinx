from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: .ncd, .pcf -> .bit, .bgn
#----------------------------------------------------------

def bitgen_emitter(env, target, source):
    bit_file = str(target[0])
    ncd_file = str(source[0])
    target.append(replace_suffix(bit_file, '.bgn'))
    source.append(replace_suffix(ncd_file, '.pcf'))
    return target, source

def run_bitgen(env, target, source):
    try:
        options = env['options']
    except KeyError:
        options = {}
    try:
        suboptions = env['suboptions']
    except KeyError:
        suboptions = {}
    try:
        flags = set(env['flags'])
    except KeyError:
        flags = set([])
    flags -= {'j'} # would prevent .bit generation

    ncd_file, pcf_file = map(str, source)
    bit_file, bgn_file = map(str, target)

    subopt_list = []
    for k in suboptions:
        v = str(suboptions[k])
        subopt_list.append('-g %s%s' % (k, ':%s' % v if v else ''))

    subopt_str = ' '.join(subopt_list)
    opt_str = ' '.join('-%s %s' % (k, options[k]) for k in options)
    flag_str = ' '.join('-%s' % f for f in flags)
    status = env.Execute('bitgen %s %s %s %s %s %s' % (
                         opt_str, subopt_str, flag_str,
                         ncd_file, bit_file, pcf_file))

    for suf in ['_bitgen.xwbt', '_summary.xml', '_usage.xml', '.drc']:
        Execute(Delete(replace_suffix(bit_file, suf)))
    Execute(Delete('webtalk.log')) # why is this not deleted??
    Execute(Delete('_xmsgs')) # why is this not deleted??

    return status

#----------------------------------------------------------

bitgen_builder = Builder(action=run_bitgen,
                      suffix='.bit',
                      src_suffix='.ncd',
                      emitter=bitgen_emitter)

