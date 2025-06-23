from spack.package import *
from spack.pkg.builtin.meson import Meson as BuiltinMeson


class Meson(BuiltinMeson):
    __doc__ = BuiltinMeson.__doc__

    version("1.4.0", sha256="61382f295378bddcd9bebb3a9a9065b1cbc671fa41b80964ab02726f9a5f3a88")

    patch("pgmath.patch", when="target=aarch64:")
