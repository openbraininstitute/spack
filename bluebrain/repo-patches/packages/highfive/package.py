# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Highfive(CMakePackage):
    """HighFive - Header-only C++ HDF5 interface"""

    homepage = "https://github.com/highfive-devs/highfive"
    git = "https://github.com/highfive-devs/highfive.git"
    url = "https://github.com/highfive-devs/highfive/archive/refs/tags/v3.0.0.tar.gz"

    # Main branch for development
    version("main", branch="main")
    # Released versions
    version("3.3.0", sha256="325cfbcf0c0296a6dd26f3b088801b7ebb8d6f109c0565c11d2d8c4af3253bff")
    version("3.2.0", sha256="01ea2eed7dbce1cf5dfff59476cfa113a7822b641aecbd99c674592fe7a4e630")
    version("3.1.1", sha256="622034f34badda41255d7793e1c5a3046954dcf0875b0bca076e7c77088a8890")
    version("3.1.0", sha256="8c5aec8621b95b26028e129bb4f38e8c388cb7d1781e9721b1e5f8827b812b3b")
    version(
        "3.0.0-beta3", sha256="555acee773ae2cf49c987fcf77397f348d287d1ce74fd5871dfe0abd0b814af2"
    )
    version("3.0.0", sha256="cf9ad114b79bfa2c1deceefc6d4e710b882451ebaa81c063e2eb1de908e7c989")

    # Optional dependencies
    variant("boost", default=False, description="Support Boost")
    variant("mpi", default=True, description="Support MPI")
    variant("eigen", default=False, description="Support Eigen")
    variant("xtensor", default=False, description="Support xtensor")

    # Boost required for tests/examples
    conflicts("~boost", when="@main")

    depends_on("boost @1.41: +serialization+system", when="+boost")
    depends_on("hdf5")
    depends_on("hdf5 ~mpi", when="~mpi")
    depends_on("hdf5 +mpi", when="+mpi")
    depends_on("eigen", when="+eigen")
    depends_on("xtensor", when="+xtensor")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        return [
            "-DUSE_BOOST:Bool=" + str(self.spec.satisfies("+boost")),
            "-DUSE_EIGEN:Bool=" + str(self.spec.satisfies("+eigen")),
            "-DUSE_XTENSOR:Bool=" + str(self.spec.satisfies("+xtensor")),
            "-DHIGHFIVE_PARALLEL_HDF5:Bool=" + str(self.spec.satisfies("+mpi")),
            "-DHIGHFIVE_EXAMPLES:Bool=" + str(self.spec.satisfies("@main")),
            "-DHIGHFIVE_UNIT_TESTS:Bool=" + str(self.spec.satisfies("@main")),
            "-DHIGHFIVE_TEST_SINGLE_INCLUDES:Bool=" + str(self.spec.satisfies("@main")),
            "-DHIGHFIVE_USE_INSTALL_DEPS:Bool=Off",
        ]
