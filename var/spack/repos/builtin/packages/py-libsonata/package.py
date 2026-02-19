# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLibsonata(PythonPackage):
    """SONATA files reader"""

    homepage = "https://github.com/openbraininstitute/libsonata"
    git = "https://github.com/openbraininstitute/libsonata.git"
    pypi = "libsonata/libsonata-0.1.14.tar.gz"

    maintainers("cattabiani", "mikeg")

    version("develop", branch="master")
    version("master", branch="master")
    version("0.1.34", sha256="a9015e42da17d08a473c47cb6104deb06d1280e065af956d00ac95894295c323")
    version("0.1.31", sha256="4de060b4c613f706a28cb0ef267b8a05dfbe3cdc7d1f5e3694c0a1ba103e19cf")
    version("0.1.30", sha256="964c50235456f8e1d2e75b0c35e9a19d645046f701f28cbcde33bf0b9c9e0084")
    version("0.1.28", sha256="9421366a2b2cd5b3c0d0f62a5aaea852949e60bac3032a3161bf0bbb107dada9")
    version("0.1.26", sha256="b653cbefbc511fe24ccf5cce7d80253954ec280800af5fd33700f0faea93fd4c")
    version("0.1.25", sha256="b332efa718123ee265263e1583a5998eaa945a13b8a22903873764cf1d8173fa")

    depends_on("catch2@2.13:", type="test")
    depends_on("cmake@3.16:", type="build")
    depends_on("fmt@7.1:")
    depends_on("hdf5@1.14:")
    depends_on("highfive@2.9:", when="@:0.1.31")
    depends_on("highfive@3.0.0-beta2:", when="@0.1.32:")
    depends_on("nlohmann-json@3.9.1")
    depends_on("py-pybind11@2.11.0:")

    depends_on("py-numpy@1.17.3:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build", when="@0.1:")
    depends_on("py-setuptools-scm@3.4:", type="build", when="@0.1:")

    def patch(self):
        filter_file("-DEXTLIB_FROM_SUBMODULES=ON", "-DEXTLIB_FROM_SUBMODULES=OFF", "setup.py")
