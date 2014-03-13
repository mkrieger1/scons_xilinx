from coregen import coregen_builder
from xst import xst_ngc_builder
from ngdbuild import ngdbuilder
from map import map_builder
from par import par_builder
from bitgen import bitgen_builder

def generate(env, **kw):
    env.Append(BUILDERS={'Coregen': coregen_builder,
                         'XstSynthesis': xst_ngc_builder,
                         'NgdBuild': ngdbuilder,
                         'Map': map_builder,
                         'PlaceRoute': par_builder,
                         'BitGen': bitgen_builder})

# this is not actually called by scons...
def exists(env):
    return all([env.Detect(cmd) for cmd in ['coregen', 'xst', 'ngdbuild',
                                            'map', 'par', 'bitgen']])
