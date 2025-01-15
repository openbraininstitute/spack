from spack.package import *
from spack.pkg.builtin.sundials import Sundials as BuiltinSundials


class Sundials(BuiltinSundials):
    __doc__ = BuiltinSundials.__doc__
    # required for building
    depends_on("python", type="build")
