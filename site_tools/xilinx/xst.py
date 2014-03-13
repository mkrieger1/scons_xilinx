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
    syr_file = replace_suffix(target[0], '.syr')
    target.append(syr_file)
    return target, source

def run_xst(env, target, source):
    ngc_file, syr_file = map(str, target)
    prj = tempfile.NamedTemporaryFile(suffix='.prj', dir='.')
    prj_file = prj.name
    tmpdir = tempfile.mkdtemp(dir='.')
    try:
        libraries = env['libraries']
    except KeyError:
        libraries = {}

    # The keys in `libraries` can be relative paths, but we try to look
    # them up using `str(s)` (`s` being a `File` object), which is
    # probably an absolute path -- to make sure that the filenames are in
    # the same format, we also apply `str(File(f))` to all keys `f` in the
    # dictionary:
    libraries = {str(File(f)): L for (f, L) in libraries.iteritems()}
    for s in source:
        lang = {'.v': 'verilog',
                '.vhd': 'vhdl'}[get_suffix(s)]
        lib = libraries.get(str(s), 'work')
        print >> prj, '%s %s "%s"' % (lang, lib, str(s))
    prj.flush()

    options = env['options']
    options['ifn'] = prj_file
    options['ofn'] = ngc_file
    options['tmpdir'] = tmpdir
    options.update(enforced_options)
    try:
        intstyle = '-intstyle %s' % (options.pop('intstyle'))
    except KeyError:
        intstyle = ''

    with tempfile.NamedTemporaryFile(suffix='.xst', dir='.') as f:
        print >> f, "run"
        for k, v in options.iteritems():
            print >> f, "-%s %s" % (k, str(v))
        f.flush()
        env.Execute('xst %s -ifn %s -ofn %s' % (
                    intstyle, f.name, syr_file))

    prj.close()
    for suf in ['.lso', '.ngc_xst.xrpt']:
        Execute(Delete(replace_suffix(ngc_file, suf)))
    Execute(Delete(tmpdir))
    Execute(Delete('xst'))
    Execute(Delete('_xmsgs'))

#----------------------------------------------------------

xst_ngc_builder = Builder(action=run_xst,
                          suffix='.ngc',
                          emitter=xst_targets)

