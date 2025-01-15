from spack.pkg.builtin.py_mpi4py import PyMpi4py as BuiltinPyMpi4py


class PyMpi4py(BuiltinPyMpi4py):
    __doc__ = BuiltinPyMpi4py.__doc__

    def setup_build_environment(self, env):
        # the shared is wrong on mac. Probably also in other cases.
        # https://github.com/spack/spack/pull/41362
        env.set("MPICC", self.spec["mpi"].mpicc)
