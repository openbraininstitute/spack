# OBI Spack Setup (macOS)

These steps describe how to set up a working Spack environment for OBI’s macOS systems.  
Use **Clang 16** as the compiler. Newer LLVM versions are not stable for key Python and scientific packages (e.g., `scipy`, `numpy`).

## Prerequisites

1. Ensure no old Spack configuration interferes:
```bash
mv ~/.spack ~/.spack.bak.$(date +%Y%m%d)
```
2. Make sure Spack is **not sourced** in any shell startup file. Or, if it is, be aware that the changes refer to that spack installation.
3. Use a **fresh clone** of Spack.
4. We assume from now on that homebrew installs in the default directory: `/opt/homebrew` and spack points to the default configuration directory: `~/.spack`.

Install basic dependencies using Homebrew:

```bash
brew install llvm@16 gcc@15 binutils flex bison thrift libffi openblas fmt openssl git curl gmake m4
```

If you encounter build errors due to missing headers (e.g., stdio.h), set:

```bash
export SDKROOT=$(xcrun --sdk macosx --show-sdk-path)
```

## Clone and Initialize Spack

```bash
git clone -c feature.manyFiles=true git@github.com:openbraininstitute/spack.git
. spack/share/spack/setup-env.sh
spack compiler find
spack external find
```

By default, the compilers are listed (for macOS) under `~/.spack/darwin/compilers.yaml`. Go there and edit the file to list only the llvm 16 compiler, effectively erasing the mac native one:

```yaml
compilers:
- compiler:
    spec: clang@=16.0.6
    paths:
      cc: /opt/homebrew/opt/llvm@16/bin/clang
      cxx: /opt/homebrew/opt/llvm@16/bin/clang++
      f77: /opt/homebrew/bin/gfortran-15
      fc: /opt/homebrew/bin/gfortran-15
    flags: {}
    operating_system: macos
    target: aarch64
    modules: []
    environment: {}
    extra_rpaths: []
```

Notice that `clang` does not provide a fortran compiler. We added it here with homebrew.

## External Packages


All these packages game me headaches sooner or later in the installation process. It is just simpler to use `homebrew`. 

Create or edit `~/.spack/packages.yaml`:

```yaml
packages:
  openssh:
    externals:
    - spec: openssh@9.9p2
      prefix: /usr
  openssl:
    externals:
    - spec: openssl@3.4.0
      prefix: /opt/homebrew
  bison:
    externals:
    - spec: bison@3.8.2
      prefix: /opt/homebrew/opt/bison
    buildable: false
  curl:
    externals:
    - spec: curl@8.7.1+gssapi+ldap+nghttp2
      prefix: /usr
  git:
    externals:
    - spec: git@2.39.5~tcltk
      prefix: /usr
  gmake:
    externals:
    - spec: gmake@3.81
      prefix: /usr
  m4:
    externals:
    - spec: m4@1.4.6
      prefix: /usr
  flex:
    externals:
    - spec: flex@2.6.4+lex
      prefix: /opt/homebrew/opt/flex
    buildable: false
  binutils:
    externals:
    - spec: binutils@2.43.1
      prefix: /opt/homebrew/opt/binutils
    buildable: false
  thrift:
    externals:
    - spec: thrift@0.21.0
      prefix: /opt/homebrew/opt/thrift
    buildable: false
  libffi:
    externals:
    - spec: libffi@3.5.1
      prefix: /opt/homebrew/opt/libffi
    buildable: false
  openblas:
    externals:
    - spec: openblas@0.3.24
      prefix: /opt/homebrew/opt/openblas
    buildable: false
  fmt:
    externals:
    - spec: fmt@11.2.0
      prefix: /opt/homebrew/opt/fmt
    buildable: false
  all:
    providers:
      mpi: [openmpi]
```

## Verification

```bash
spack find
spack spec python
```

If both commands run without errors, your Spack setup is ready for OBI macOS systems.

## Problems with newer Python (3.10+)

If you get an error like:

```bash
==> Error: cannot bootstrap the "clingo" Python module from spec "clingo-bootstrap@spack+python ..."
spack-install raised AttributeError: module 'ast' has no attribute 'Str'
```

it usually means you installed a version of Python newer than 3.9, and `python3` resolves to that version. Spack cannot work with Python 3.10+ and porting all the changes from the original Spack to support it is a major effort.  

The simplest solution is to remove the Homebrew `python3` symlink:

```bash
rm /opt/homebrew/bin/python3
```

This forces Spack to use the system Python (usually 3.9).

**Drawback**: to use Homebrew Python, you now need to call `python3.xx` (e.g., `python3.14` or `python3.11`). In practice, if you use virtual environments, this is rarely needed.
