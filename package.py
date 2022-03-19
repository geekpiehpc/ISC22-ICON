# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install icon
#
# You can edit this file again by typing:
#
#     spack edit icon
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from ast import In, Index
from re import S
from spack import *
import os


class Icon(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "http://10.15.89.111:8001/icon-scc-2021-isc-scc.zip"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2021-isc-scc',
            sha256='de362443b0f1a8136c415075ade6f5b4ec85d13df3db6a24565acfe92d336149')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('mpi')
    depends_on('lapack')
    depends_on('openblas')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('libxml2')
    variant('debug', default=False, description='Enable debug when compiling')
    variant('cuda', default=False, description='Enable cuda when compiling')
    depends_on('cuda', when='+cuda')

    def setup_build_environment(self, env):

        spec = self.spec

        FCFLAGSINCLUDES = []
        FCFLAGS = []
        LDFLAGS = []
        CPPFLAGS = []

        # debug
        if '+debug' in spec:
            FCFLAGS.append("-g")

        # cuda
        if '+cuda' in spec:
            LDFLAGS.append(spec["cuda"].prefix.lib)
            # print(self.compiler.cc)
            path = os.path.abspath(self.compiler.cc)
            path = os.path.join(path, "../lib")
            path = os.path.abspath(path)
            LDFLAGS.append(path)

        # O3
        FCFLAGS.append("-O2")

        # netcdf-f
        FCFLAGSINCLUDES.append(spec['netcdf-fortran'].prefix.include)
        LDFLAGS.append(spec['netcdf-fortran'].prefix.lib)

        # netcdf-c
        FCFLAGSINCLUDES.append(spec['netcdf-c'].prefix.include)
        LDFLAGS.append(spec['netcdf-c'].prefix.lib)

        # blas
        LDFLAGS.append(spec['openblas'].prefix.lib)

        # xml2
        LDFLAGS.append(spec['libxml2'].prefix.lib)
        CPPFLAGS.append(os.path.join(spec['libxml2'].prefix.include, "libxml2"))

        env.set(
            'FCFLAGS', f"{' '.join(list(map(lambda x: '-I'+x,FCFLAGSINCLUDES))+FCFLAGS)}")
        env.set('CPPFLAGS', f"{' '.join(list(map(lambda x: '-I'+x,CPPFLAGS)))}")
        env.set('LDFLAGS', f"{' '.join(list(map(lambda x: '-L'+x,LDFLAGS)))}")
        env.set('OMPI_ALLOW_RUN_AS_ROOT', 1)
        env.set('OMPI_ALLOW_RUN_AS_ROOT_CONFIRM', 1)

    def configure_args(self):
        args = []
        spec = self.spec
        LIBS = []

        # initialize the submodules locate
        #print("cd {}".format(os.getcwd()))
        #os.system("cd {}".format(os.getcwd()))
        #os.system("git submodule init")
        #os.system("git submodule update")
        #raise RuntimeError("Fuck")

        # preprocessing
        args.append("--enable-jsbach")

        # netcdf-f
        LIBS.append("netcdff")

        # netcdf-c
        LIBS.append("netcdf")
        args.append("--enable-coupling")

        # blas+lapack
        LIBS.append("openblas")

        # xml2
        LIBS.append("xml2")

        # cuda
        if '+cuda' in spec:
            LIBS.append("cudart")
            LIBS.append("stdc++")
            args.append("--enable-gpu")

        args = ["CC=%s" % spec['mpi'].mpicc, "FC=%s" %
                spec['mpi'].mpifc, f"LIBS={' '.join(list(map(lambda x: '-l'+x,LIBS)))}", ]
        return args
