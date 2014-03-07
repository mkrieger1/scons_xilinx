from SCons.Script import *
import tempfile
from util import replace_suffix, replace_path

#----------------------------------------------------------
# builder: Coregen .xco -> .v, .ngc, .xco, .log
# intermediate step: create .cgp file
#----------------------------------------------------------

# enforce generation of .v file
enforced_options = {
    'implementationfiletype': 'Ngc',
    'simulationfiles': 'Behavioral',
    'verilogsim': 'true'
}

def coregen_targets(env, target, source):
    v_file = replace_path(str(target[0]), env['outdir'])
    target = [v_file] + [replace_suffix(v_file, suf)
                         for suf in ['.ngc', '.xco', '.log']]
    return target, source

def run_coregen(env, target, source):
    xco_file = str(source[0])
    work_dir = tempfile.mkdtemp(dir='.')
    out_dir = tempfile.mkdtemp(dir='.')
    options = env['options']
    options['workingdirectory'] = work_dir
    options['outputdirectory'] = out_dir
    options.update(enforced_options)

    with tempfile.NamedTemporaryFile(suffix='.cgp', dir='.') as f:
        cgp_file = f.name
        for (k, v) in options.iteritems():
            print >> f, "SET %s = %s" % (k, str(v))
        f.flush()
        env.Execute('coregen -b %s -p %s' % (xco_file, cgp_file))

    for t in target[:-1]: # .v, .ngc, .xco
        Execute(Move(t, replace_path(str(t), out_dir)))
    Execute(Move(target[-1], 'coregen.log')) # .log
    Execute(Delete(work_dir))
    Execute(Delete(out_dir))
    Execute(Delete(replace_suffix(cgp_file, '.cgc')))

#----------------------------------------------------------

def generate(env, **kw):
    coregen_builder = Builder(action=run_coregen,
                              suffix='.v',
                              src_suffix='.xco',
                              emitter=coregen_targets)
    env.Append(BUILDERS={'Coregen': coregen_builder})
    
# this is not actually called by scons...
def exists(env):
    return env.Detect('coregen')

