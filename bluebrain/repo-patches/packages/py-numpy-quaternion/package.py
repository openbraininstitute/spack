from spack.package import conflicts, version
from spack.pkg.builtin.py_numpy_quaternion import PyNumpyQuaternion as BuiltinPyNumpyQuaternion


class PyNumpyQuaternion(BuiltinPyNumpyQuaternion):
    __doc__ = BuiltinPyNumpyQuaternion.__doc__

    version("2024.0.3", sha256="cf39a8a4506eeda297ca07a508c10c08b3487df851a0e34f070a7bf8fab9f290")

    # numpy changed pointer types somewhere before at 1.26.1. Quaternion requires a newer verison
    conflicts("py-numpy-quaternion@:2021.11.4.15.26.3", when="^py-numpy@1.26.1:")
