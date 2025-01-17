from spack.package import *
from spack.pkg.builtin.freetype import Freetype as BuiltinFreetype


class Freetype(BuiltinFreetype):
    __doc__ = BuiltinFreetype.__doc__

    # they do not import Byte and on mac it fails with older versions
    version("2.13.3", sha256="5c3a8e78f7b24c20b25b54ee575d6daa40007a5f4eea2845861c3409b3021747")
