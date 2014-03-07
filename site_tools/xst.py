from SCons.Script import *
import tempfile
from util import replace_suffix

#----------------------------------------------------------
# builder: HDL files -> .ngc, .syr
# intermediate steps: create .prj and .xst files
#----------------------------------------------------------

def xst_targets(env, target, source):
    # append list of HDL files to source
    lang_map = source[0].read()
    for lang, files in lang_map.iteritems():
        for f in files:
            source.append(f)
    # append .syr to target
    syr_file = replace_suffix(str(target[0]), '.syr')
    target.append(syr_file)
    return target, source

def run_xst(env, target, source):
    # hdl_language_map, hdl_files = source
    lang_map = source[0].read()
    ngc_file, syr_file = map(str, target)
    prj_file = tempfile.NamedTemporaryFile(suffix='.prj', dir='.')

    for lang, files in lang_map.iteritems():
        for f in files:
            print >> prj_file, '%s work "%s"' % (lang, str(f))
    prj_file.flush()

    options = env['options']
    options['ifn'] = prj_file.name
    options['ofn'] = ngc_file

    with tempfile.NamedTemporaryFile(suffix='.xst', dir='.') as f:
        print >> f, "run"
        for k, v in options.iteritems():
            print >> f, "-%s %s" % (k, str(v))
        f.flush()
        env.Execute('xst -ifn %s -ofn %s' % (f.name, syr_file))

    prj_file.close()
    for suf in ['.lso', '.ngc_xst.xrpt']:
        Execute(Delete(replace_suffix(ngc_file, suf)))
    Execute(Delete('_xmsgs'))
    Execute(Delete('xst'))

#----------------------------------------------------------

def generate(env, **kw):
    xst_ngc_builder = Builder(action=run_xst,
                              suffix='.ngc',
                              src_suffix='.prj',
                              emitter=xst_targets)

    env.Append(BUILDERS={'XstRun': xst_ngc_builder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('xst')

