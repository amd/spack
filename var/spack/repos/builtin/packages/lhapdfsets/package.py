# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Lhapdfsets(BundlePackage):
    """A set of disretised data files of parton density functions ,
       to be used with the LHAPDF library"""

    homepage = "https://lhapdf.hepforge.org/pdfsets.html"

    tags = ['hep']

    maintainers = ['vvolkl']

    version('6.3.0')

    depends_on('lhapdf', type='build')

    phases = ['install']

    # use a dummy executables for spack external support
    executables = [r'^lhapdf$']

    variant('sets', description="Individiual lhapdf sets to install", values=('all', 'default'), default='default')

    def install(self, spec, prefix):
        mkdirp(self.prefix.share.lhapdfsets)
        lhapdf = which('lhapdf')
        sets = self.spec.variants['sets'].value
        if sets == 'all':
            # parse set names from index file
            all_sets = [_line.split()[1] for _line in
                        open(join_path(os.path.dirname(__file__),
                             'pdfsets.index')).readlines()]
            sets = all_sets
        elif sets == 'default':
            default_sets = ["MMHT2014lo68cl", "MMHT2014nlo68cl", "CT14lo", "CT14nlo"]
            sets = default_sets
        lhapdf("--pdfdir=" + self.prefix.share.lhapdfsets,
               "install", *sets)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('LHAPDF_DATA_PATH', self.prefix.share.lhapdfsets)

    def setup_run_environment(self, env):
        env.set('LHAPDF_DATA_PATH', self.prefix.share.lhapdfsets)

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        path = os.environ.get('LHAPDF_DATA_PATH', None)
        # unfortunately the sets are not versioned -
        # just hardcode the current version and hope it is fine
        s = Spec.from_detection('lhapdfsets@6.3.0')
        s.external_path = path
        return s if path else None
