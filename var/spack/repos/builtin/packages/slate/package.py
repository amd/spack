# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Slate(CMakePackage, CudaPackage, ROCmPackage):
    """The Software for Linear Algebra Targeting Exascale (SLATE) project is
    to provide fundamental dense linear algebra capabilities to the US
    Department of Energy and to the high-performance computing (HPC) community
    at large. To this end, SLATE will provide basic dense matrix operations
    (e.g., matrix multiplication, rank-k update, triangular solve), linear
    systems solvers, least square solvers, singular value and eigenvalue
    solvers."""

    homepage = "https://icl.utk.edu/slate/"
    git      = "https://bitbucket.org/icl/slate"
    url      = 'https://bitbucket.org/icl/slate/downloads/slate-2020.10.00.tar.gz'
    maintainers = ['G-Ragghianti', 'mgates3']

    version('master', branch='master')
    version('2021.05.01', sha256='d9db2595f305eb5b1b49a77cc8e8c8e43c3faab94ed910d8387c221183654218')
    version('2020.10.00', sha256='ff58840cdbae2991d100dfbaf3ef2f133fc2f43fc05f207dc5e38a41137882ab')

    variant('mpi',    default=True, description='Build with MPI support (without MPI is experimental).')
    variant('openmp', default=True, description='Build with OpenMP support.')
    variant('shared', default=True, description='Build shared library')

    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('blaspp ~cuda', when='~cuda')
    depends_on('blaspp +cuda', when='+cuda')
    depends_on('blaspp ~rocm', when='~rocm')
    for val in ROCmPackage.amdgpu_targets:
        depends_on('blaspp +rocm amdgpu_target=%s' % val, when='amdgpu_target=%s' % val)
    depends_on('lapackpp@2021.04.00:', when='@2021.05.01:')
    depends_on('lapackpp@2020.10.02', when='@2020.10.00')
    depends_on('lapackpp@master', when='@master')
    depends_on('scalapack')

    cpp_17_msg = 'Requires C++17 compiler support'
    conflicts('%gcc@:5', msg=cpp_17_msg)
    conflicts('%xl', msg=cpp_17_msg)
    conflicts('%xl_r', msg=cpp_17_msg)
    conflicts('%intel@19:', msg='Does not currently build with icpc >= 2019')
    conflicts('+rocm', when='@:2020.10.00', msg='ROCm support requires SLATE 2021.05.01 or greater')
    conflicts('+rocm', when='+cuda', msg='SLATE only supports one GPU backend at a time')

    def cmake_args(self):
        spec = self.spec
        backend_config = '-Duse_cuda=%s' % ('+cuda' in spec)
        if self.version >= Version('2021.05.01'):
            backend = 'none'
            if '+cuda' in spec:
                backend = 'cuda'
            if '+rocm' in spec:
                backend = 'hip'
            backend_config = '-Dgpu_backend=%s' % backend

        return [
            '-Dbuild_tests=%s'       % self.run_tests,
            '-Duse_openmp=%s'        % ('+openmp' in spec),
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            backend_config,
            '-Duse_mpi=%s'           % ('+mpi' in spec),
            '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs.joined(';')
        ]
