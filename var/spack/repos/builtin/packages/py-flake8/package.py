# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlake8(PythonPackage):
    """Flake8 is a wrapper around PyFlakes, pep8 and Ned Batchelder's
    McCabe script."""

    homepage = "https://github.com/PyCQA/flake8"
    pypi     = "flake8/flake8-4.0.1.tar.gz"

    version('4.0.1', sha256='806e034dda44114815e23c16ef92f95c91e4c71100ff52813adf7132a6ad870d')
    version('4.0.0', sha256='b52d27e627676b015340c3b1c72bc9259a6cacc9341712fb8f01ddfaaa2c651a')
    version('3.9.2', sha256='07528381786f2a6237b061f6e96610a4167b226cb926e2aa2b6b1d78057c576b')
    version('3.8.2', sha256='c69ac1668e434d37a2d2880b3ca9aafd54b3a10a3ac1ab101d22f29e29cf8634')
    version('3.7.8', sha256='19241c1cbc971b9962473e4438a2ca19749a7dd002dd1a946eaba171b4114548')
    version('3.7.7', sha256='859996073f341f2670741b51ec1e67a01da142831aa1fdc6242dbf88dffbe661')
    version('3.5.0', sha256='7253265f7abd8b313e3892944044a365e3f4ac3fcdcfb4298f55ee9ddf188ba0')
    version('3.0.4', sha256='b4c210c998f07d6ff24325dd91fbc011f2c37bcd6bf576b188de01d8656e970d')
    version('2.5.4', sha256='cc1e58179f6cf10524c7bfdd378f5536d0a61497688517791639a5ecc867492f')

    extends('python', ignore='bin/(pyflakes|pycodestyle)')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@3.9.2:')
    depends_on('python@3.6:', type=('build', 'run'), when='@4.0.0:')

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-flake8 requires py-setuptools during runtime as well.
    depends_on('py-setuptools@30:', type=('build', 'run'))

    # Flake8 uses ranges for its dependencies to enforce a stable list of
    # error codes within each minor release:
    # http://flake8.pycqa.org/en/latest/faq.html#why-does-flake8-use-ranges-for-its-dependencies
    # http://flake8.pycqa.org/en/latest/internal/releases.html#releasing-flake8

    # Flake8 4.0.X
    depends_on('py-pycodestyle@2.8.0:2.8', when='@4.0.0:4.0', type=('build', 'run'))
    depends_on('py-pyflakes@2.4.0:2.4',    when='@4.0.0:4.0', type=('build', 'run'))

    # Flake8 3.9.X
    depends_on('py-pycodestyle@2.7.0:2.7', when='@3.9.0:3.9', type=('build', 'run'))
    depends_on('py-pyflakes@2.3.0:2.3',    when='@3.9.0:3.9', type=('build', 'run'))

    # Flake8 3.8.X
    depends_on('py-pycodestyle@2.6.0:2.6', when='@3.8.0:3.8', type=('build', 'run'))
    depends_on('py-pyflakes@2.2.0:2.2',    when='@3.8.0:3.8', type=('build', 'run'))

    # Flake8 3.7.X
    # FIXME @0.3.0:0.3 causes concretization to hang
    depends_on('py-entrypoints@0.3',           when='@3.7.0:3.8', type=('build', 'run'))
    depends_on('py-pyflakes@2.1.0:2.1',    when='@3.7.0:3.7', type=('build', 'run'))
    depends_on('py-pycodestyle@2.5.0:2.5', when='@3.7.0:3.7', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6',      when='@3.7.0:', type=('build', 'run'))

    # Flake8 3.5.X
    depends_on('py-pyflakes@1.5:1.6',     when='@3.5.0:3.5', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0:2.4',  when='@3.5.0:3.5', type=('build', 'run'))
    depends_on('py-mccabe@0.6.0:0.6', when='@3.5.0:3.5', type=('build', 'run'))

    # Flake8 3.0.X
    depends_on('py-pyflakes@0.8.1:1.1,1.2.3:1.2', when='@3.0.0:3.0', type=('build', 'run'))
    depends_on('py-pycodestyle@2.0.0:2.0',        when='@3.0.0:3.0', type=('build', 'run'))
    depends_on('py-mccabe@0.5.0:0.5',             when='@3.0.0:3.0', type=('build', 'run'))

    # Flake8 2.5.X
    depends_on('py-pyflakes@0.8.1:1.0',               when='@2.5.0:2.5', type=('build', 'run'))
    depends_on('py-pycodestyle@1.5.7:1.5,1.6.3:', when='@2.5.0:2.5', type=('build', 'run'))
    depends_on('py-mccabe@0.2.1:0.4',                 when='@2.5.0:2.5', type=('build', 'run'))

    # Python version-specific backports
    depends_on('py-importlib-metadata', when='@3.8.0:3.9.2 ^python@:3.7', type=('build', 'run'))
    depends_on('py-importlib-metadata@:4.2', when='@4.0.0: ^python@:3.7', type=('build', 'run'))
    depends_on('py-enum34',             when='@3.0.0: ^python@:3.3', type=('build', 'run'))
    depends_on('py-typing',             when='@3.7.0: ^python@:3.4', type=('build', 'run'))
    depends_on('py-configparser',       when='@3.0.0: ^python@:3.1', type=('build', 'run'))
    depends_on('py-functools32',        when='@3.7.4: ^python@:3.1', type=('build', 'run'))

    def patch(self):
        """Filter pytest-runner requirement out of setup.py."""
        filter_file("['pytest-runner']", "[]", 'setup.py', string=True)
