from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: HDL file lists -> .prj
#----------------------------------------------------------

def create_prj(env, target, source):
    hdl_files = source[0].read()
    with open(str(target[0]), 'w') as f:
        for lang in ['verilog', 'vhdl']:
            for s in hdl_files[lang]:
                print >> f, '%s work "%s"' % (lang, str(s))

#----------------------------------------------------------
# builder: XST .prj -> .ngc, .syr
# intermediate step: create .xst file
#----------------------------------------------------------

def xst_targets(env, target, source):
    syr_file = replace_suffix(str(target[0]), '.syr')
    target.append(syr_file)
    return target, source

def run_xst(env, target, source):
    ngc_file, syr_file = map(str, target)
    prj_file = str(source[0])

    options = env['options']
    options['ifn'] = prj_file
    options['ofn'] = ngc_file

    with tempfile.NamedTemporaryFile(suffix='.xst', dir='.') as f:
        print >> f, "run"
        for k, v in options.iteritems():
            print >> f, "-%s %s" % (k, str(v))
        f.flush()
        env.Execute('xst -ifn %s -ofn %s' % (f.name, syr_file))

    for suf in ['.lso', '.ngc_xst.xrpt']:
        Execute(Delete(replace_suffix(ngc_file, suf)))
    Execute(Delete('_xmsgs'))
    Execute(Delete('xst'))

#----------------------------------------------------------

def generate(env, **kw):
    xst_prj_builder = Builder(action=create_prj,
                              suffix='.prj')

    xst_ngc_builder = Builder(action=run_xst,
                              suffix='.ngc',
                              src_suffix='.prj',
                              emitter=xst_targets)

    env.Append(BUILDERS={'XstProject': xst_prj_builder,
                         'XstRun': xst_ngc_builder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('xst')

