from spack.package import *
from spack.pkg.builtin.boost import Boost as BuiltinBoost


class Boost(BuiltinBoost):
    __doc__ = BuiltinBoost.__doc__

    version("1.87.0", sha256="af57be25cb4c4f4b413ed692fe378affb4352ea50fbe294a11ef548f4d527d89")

    variant(
        "cxxstd",
        default="98",
        values=(
            conditional("98", when="@:1.83.0"),
            "11",
            "14",
            conditional("17", when="@1.63.0:"),
            conditional("2a", when="@1.73.0:"),
            conditional("20", when="@1.77.0:"),
            conditional("23", when="@1.79.0:"),
            conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
