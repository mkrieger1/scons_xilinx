from SCons.Script import *
import tempfile
from util import get_suffix, replace_suffix

#----------------------------------------------------------
# builder: HDL files -> .ngc, .syr
# intermediate steps: create .prj and .xst files
#----------------------------------------------------------

enforced_options = {
    'ifmt': 'mixed',
    'ofmt': 'NGC'
}

def xst_targets(env, target, source):
    syr_file = replace_suffix(str(target[0]), '.syr')
    target.append(syr_file)
    return target, source

def run_xst(env, target, source):
    ngc_file, syr_file = map(str, target)
    prj = tempfile.NamedTemporaryFile(suffix='.prj', dir='.')
    prj_file = prj.name
    tmpdir = tempfile.mkdtemp(dir='.')

    for s in source:
        lang = {'.v': 'verilog',
                '.vhd': 'vhdl'}[get_suffix(str(s))]
        print >> prj, '%s work "%s"' % (lang, str(s))
    prj.flush()

    options = env['options']
    options['ifn'] = prj_file
    options['ofn'] = ngc_file
    options['tmpdir'] = tmpdir
    options.update(enforced_options)

    with tempfile.NamedTemporaryFile(suffix='.xst', dir='.') as f:
        print >> f, "run"
        for k, v in options.iteritems():
            print >> f, "-%s %s" % (k, str(v))
        f.flush()
        env.Execute('xst -ifn %s -ofn %s' % (f.name, syr_file))

    prj.close()
    for suf in ['.lso', '.ngc_xst.xrpt']:
        Execute(Delete(replace_suffix(ngc_file, suf)))
    Execute(Delete(tmpdir))
    Execute(Delete('xst'))
    Execute(Delete('_xmsgs'))

#----------------------------------------------------------

def generate(env, **kw):
    xst_ngc_builder = Builder(action=run_xst,
                              suffix='.ngc',
                              src_suffix='.prj',
                              emitter=xst_targets)

    env.Append(BUILDERS={'XstSynthesis': xst_ngc_builder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('xst')

