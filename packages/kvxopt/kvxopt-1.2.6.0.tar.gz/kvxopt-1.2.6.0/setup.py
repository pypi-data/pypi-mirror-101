from setuptools import setup, Extension
from glob import glob
import os, sys
import platform
import versioneer
from os import path
from distutils.file_util import copy_file

# Modifiy this if BLAS and LAPACK libraries are not in /usr/lib.
BLAS_LIB_DIR = '/usr/lib'

# Default names of BLAS and LAPACK libraries
BLAS_LIB = ['blas']
LAPACK_LIB = ['lapack']
BLAS_EXTRA_LINK_ARGS = []

# Set environment variable BLAS_NOUNDERSCORES=1 if your BLAS/LAPACK do
# not use trailing underscores
BLAS_NOUNDERSCORES = False

# Set to 1 if you are using the random number generators in the GNU
# Scientific Library.
BUILD_GSL = 0

# Directory containing libgsl (used only when BUILD_GSL = 1).
GSL_LIB_DIR = '/usr/lib'

# Directory containing the GSL header files (used only when BUILD_GSL = 1).
GSL_INC_DIR = '/usr/include/gsl'

# Set to 1 if you are installing the fftw module.
BUILD_FFTW = 0

# Directory containing libfftw3 (used only when BUILD_FFTW = 1).
FFTW_LIB_DIR = '/usr/lib'

# Directory containing fftw.h (used only when BUILD_FFTW = 1).
FFTW_INC_DIR = '/usr/include'

# Set to 1 if you are installing the glpk module.
BUILD_GLPK = 0

# Directory containing libglpk (used only when BUILD_GLPK = 1).
GLPK_LIB_DIR = '/usr/lib'

# Directory containing glpk.h (used only when BUILD_GLPK = 1).
GLPK_INC_DIR = '/usr/include'

# Set to 1 if you are installing the osqp module.
BUILD_OSQP = 0

# Directory containing libglpk (used only when BUILD_OSQP = 1).
OSQP_LIB_DIR = '/usr/local/lib'

# Directory containing glpk.h (used only when BUILD_OSQP = 1).
OSQP_INC_DIR = '/usr/local/include/osqp'

# Set to 1 if you are installing the DSDP module.
BUILD_DSDP = 0

# Directory containing libdsdp (used only when BUILD_DSDP = 1).
DSDP_LIB_DIR = '/usr/lib'

# Directory containing dsdp5.h (used only when BUILD_DSDP = 1).
DSDP_INC_DIR = '/usr/include/dsdp'

# Guess {package}_LIB_DIR and {package}_INC_DIR
if sys.platform.startswith("darwin"):
    # macOS
    SUITESPARSE_LIB_DIR = '/usr/local/lib'
    SUITESPARSE_INC_DIR = '/usr/local/include'
else:
    if glob("/usr/lib/x86_64-linux-gnu/libsuitesparse*"):
        # Ubuntu/Debian
        SUITESPARSE_LIB_DIR = "/usr/lib/x86_64-linux-gnu"
        SUITESPARSE_INC_DIR = "/usr/include/suitesparse"
    elif glob("/usr/lib64/libsuitesparse*"):
        # CentOS/Fedora/RedHat
        SUITESPARSE_LIB_DIR = "/usr/lib64"
        SUITESPARSE_INC_DIR = "/usr/include/suitesparse"
    else:
        # Default
        SUITESPARSE_LIB_DIR = '/usr/lib'
        SUITESPARSE_INC_DIR = '/usr/include'



# Directory containing SuiteSparse source
SUITESPARSE_SRC_DIR = ''

# For SuiteSparse Versions before to 4.0.0 SuiteSparse_config does not exist
# We can avoid the search and link with this flag
SUITESPARSE_CONFIG = 1

# Set to 1 if compiling with MSVC 14 or later
MSVC=0

# No modifications should be needed below this line.

BLAS_NOUNDERSCORES = int(os.environ.get("KVXOPT_BLAS_NOUNDERSCORES",BLAS_NOUNDERSCORES)) == True
BLAS_LIB = os.environ.get("KVXOPT_BLAS_LIB",BLAS_LIB)
LAPACK_LIB = os.environ.get("KVXOPT_LAPACK_LIB",LAPACK_LIB)
BLAS_LIB_DIR = os.environ.get("KVXOPT_BLAS_LIB_DIR",BLAS_LIB_DIR)
BLAS_EXTRA_LINK_ARGS = os.environ.get("KVXOPT_BLAS_EXTRA_LINK_ARGS",BLAS_EXTRA_LINK_ARGS)
if type(BLAS_LIB) is str: BLAS_LIB = BLAS_LIB.strip().split(';')
if type(LAPACK_LIB) is str: LAPACK_LIB = LAPACK_LIB.strip().split(';')
if type(BLAS_EXTRA_LINK_ARGS) is str: BLAS_EXTRA_LINK_ARGS = BLAS_EXTRA_LINK_ARGS.strip().split(';')
BUILD_GSL = int(os.environ.get("KVXOPT_BUILD_GSL",BUILD_GSL))
GSL_LIB_DIR = os.environ.get("KVXOPT_GSL_LIB_DIR",GSL_LIB_DIR)
GSL_INC_DIR = os.environ.get("KVXOPT_GSL_INC_DIR",GSL_INC_DIR)
BUILD_FFTW = int(os.environ.get("KVXOPT_BUILD_FFTW",BUILD_FFTW))
FFTW_LIB_DIR = os.environ.get("KVXOPT_FFTW_LIB_DIR",FFTW_LIB_DIR)
FFTW_INC_DIR = os.environ.get("KVXOPT_FFTW_INC_DIR",FFTW_INC_DIR)
BUILD_GLPK = int(os.environ.get("KVXOPT_BUILD_GLPK",BUILD_GLPK))
GLPK_LIB_DIR = os.environ.get("KVXOPT_GLPK_LIB_DIR",GLPK_LIB_DIR)
GLPK_INC_DIR = os.environ.get("KVXOPT_GLPK_INC_DIR",GLPK_INC_DIR)
BUILD_OSQP = int(os.environ.get("KVXOPT_BUILD_OSQP",BUILD_OSQP))
OSQP_LIB_DIR = os.environ.get("KVXOPT_OSQP_LIB_DIR",OSQP_LIB_DIR)
OSQP_INC_DIR = os.environ.get("KVXOPT_OSQP_INC_DIR",OSQP_INC_DIR)
BUILD_DSDP = int(os.environ.get("KVXOPT_BUILD_DSDP",BUILD_DSDP))
DSDP_LIB_DIR = os.environ.get("KVXOPT_DSDP_LIB_DIR",DSDP_LIB_DIR)
DSDP_INC_DIR = os.environ.get("KVXOPT_DSDP_INC_DIR",DSDP_INC_DIR)
SUITESPARSE_LIB_DIR = os.environ.get("KVXOPT_SUITESPARSE_LIB_DIR",SUITESPARSE_LIB_DIR)
SUITESPARSE_INC_DIR = os.environ.get("KVXOPT_SUITESPARSE_INC_DIR",SUITESPARSE_INC_DIR)
SUITESPARSE_SRC_DIR = os.environ.get("KVXOPT_SUITESPARSE_SRC_DIR",SUITESPARSE_SRC_DIR)
SUITESPARSE_CONFIG = os.environ.get("KVXOPT_SUITESPARSE_CONFIG",SUITESPARSE_CONFIG) == True
MSVC = int(os.environ.get("KVXOPT_MSVC",MSVC)) == True
INSTALL_REQUIRES = os.environ.get("KVXOPT_INSTALL_REQUIRES",[])
if type(INSTALL_REQUIRES) is str: INSTALL_REQUIRES = INSTALL_REQUIRES.strip().split(';')

RT_LIB = ["rt"] if sys.platform.startswith("linux") else []
M_LIB = ["m"] if not MSVC else []
UMFPACK_EXTRA_COMPILE_ARGS = ["-Wno-unknown-pragmas"] if not MSVC else []

extmods = []


SUITESPARSE_CONF_LIB = ([], ['suitesparseconfig'])[SUITESPARSE_CONFIG]




# Macros
MACROS = []
if BLAS_NOUNDERSCORES: MACROS.append(('BLAS_NO_UNDERSCORE',''))

if platform.architecture() == ('64bit', 'WindowsPE') and not MSVC:
    MACROS += [('MS_WIN64', 1)]


if sys.platform.startswith("win"):
    GSL_MACROS = [('GSL_DLL',''),('WIN32','')]
    GSL_LIBS = ['gsl']
    GSL_EXTRA_LINK_ARGS = []
    FFTW_MACROS = [('FFTW_DLL',''),('FFTW_NO_Complex','')]
else:
    GSL_MACROS = []
    GSL_LIBS = M_LIB + ['gsl'] + BLAS_LIB
    GSL_EXTRA_LINK_ARGS = BLAS_EXTRA_LINK_ARGS
    FFTW_MACROS = []

# optional modules

if BUILD_GSL:
    gsl = Extension('gsl', libraries = GSL_LIBS,
        include_dirs = [ GSL_INC_DIR ],
        library_dirs = [ GSL_LIB_DIR ],
        define_macros = MACROS + GSL_MACROS,
        extra_link_args = GSL_EXTRA_LINK_ARGS,
        sources = ['src/C/gsl.c'] )
    extmods += [gsl];

if BUILD_FFTW:
    fftw = Extension('fftw', libraries = ['fftw3'] + BLAS_LIB,
        include_dirs = [ FFTW_INC_DIR ],
        library_dirs = [ FFTW_LIB_DIR, BLAS_LIB_DIR ],
        define_macros = MACROS + FFTW_MACROS,
        extra_link_args = BLAS_EXTRA_LINK_ARGS,
        sources = ['src/C/fftw.c'] )
    extmods += [fftw];

if BUILD_GLPK:
    glpk = Extension('glpk', libraries = ['glpk'],
        include_dirs = [ GLPK_INC_DIR ],
        library_dirs = [ GLPK_LIB_DIR ],
        define_macros = MACROS,
        sources = ['src/C/glpk.c'] )
    extmods += [glpk];

if BUILD_OSQP:
    osqp = Extension('osqp', libraries = ['osqp'],
        include_dirs = [ OSQP_INC_DIR ],
        library_dirs = [ OSQP_LIB_DIR ],
        define_macros = MACROS + [('DDEBUG', ''), ('PRINTING', '')],
        sources = ['src/C/osqp.c'] )
    extmods += [osqp];

if BUILD_DSDP:
    dsdp = Extension('dsdp', libraries = ['dsdp'] + LAPACK_LIB + BLAS_LIB,
        include_dirs = [ DSDP_INC_DIR ],
        library_dirs = [ DSDP_LIB_DIR, BLAS_LIB_DIR ],
        extra_link_args = BLAS_EXTRA_LINK_ARGS,
        define_macros = MACROS,
        sources = ['src/C/dsdp.c'] )
    extmods += [dsdp];

# Required modules

base = Extension('base', libraries = M_LIB + LAPACK_LIB + BLAS_LIB,
    library_dirs = [ BLAS_LIB_DIR ],
    define_macros = MACROS,
    extra_link_args = BLAS_EXTRA_LINK_ARGS,
    sources = ['src/C/base.c','src/C/dense.c','src/C/sparse.c'])

blas = Extension('blas', libraries = BLAS_LIB,
    library_dirs = [ BLAS_LIB_DIR ],
    define_macros = MACROS,
    extra_link_args = BLAS_EXTRA_LINK_ARGS,
    sources = ['src/C/blas.c'] )

lapack = Extension('lapack', libraries = LAPACK_LIB + BLAS_LIB,
    library_dirs = [ BLAS_LIB_DIR ],
    define_macros = MACROS,
    extra_link_args = BLAS_EXTRA_LINK_ARGS,
    sources = ['src/C/lapack.c'] )

if not SUITESPARSE_SRC_DIR:
    umfpack = Extension('umfpack',
        libraries = ['umfpack','cholmod','amd','colamd'] + SUITESPARSE_CONF_LIB + LAPACK_LIB + BLAS_LIB + RT_LIB,
        include_dirs = [SUITESPARSE_INC_DIR],
        define_macros = MACROS,
        library_dirs = [SUITESPARSE_LIB_DIR, BLAS_LIB_DIR],
        sources = ['src/C/umfpack.c'])
else:
    umfpack = Extension('umfpack',
        include_dirs = [ SUITESPARSE_SRC_DIR + '/UMFPACK/Include',
            SUITESPARSE_SRC_DIR + '/AMD/Include',
            SUITESPARSE_SRC_DIR + '/UMFPACK/Source',
            SUITESPARSE_SRC_DIR + '/AMD/Source',
            SUITESPARSE_SRC_DIR + '/SuiteSparse_config' ],
        library_dirs = [ BLAS_LIB_DIR ],
        define_macros = MACROS + [('NTIMER', '1'), ('NCHOLMOD', '1')],
        libraries = LAPACK_LIB + BLAS_LIB,
        extra_compile_args = UMFPACK_EXTRA_COMPILE_ARGS,
        extra_link_args = BLAS_EXTRA_LINK_ARGS,
        sources = [ 'src/C/umfpack.c',
            SUITESPARSE_SRC_DIR + '/UMFPACK/Source/umfpack_tictoc.c',
            SUITESPARSE_SRC_DIR + '/SuiteSparse_config/SuiteSparse_config.c'] +
            glob('src/C/SuiteSparse_cvxopt_extra/umfpack/*'))

if not SUITESPARSE_SRC_DIR:
    klu = Extension('klu',
    libraries=['klu', 'amd', 'colamd', 'btf',] + SUITESPARSE_CONF_LIB + LAPACK_LIB + BLAS_LIB + RT_LIB,
    include_dirs = [SUITESPARSE_INC_DIR],
    define_macros = MACROS,
    library_dirs = [SUITESPARSE_LIB_DIR, BLAS_LIB_DIR],
    sources = ['src/C/klu.c'])
else:
    klu = Extension('klu',
        include_dirs = [ SUITESPARSE_SRC_DIR + '/KLU/Include',
            SUITESPARSE_SRC_DIR + '/KLU/Source',
            SUITESPARSE_SRC_DIR + '/AMD/Include',
            SUITESPARSE_SRC_DIR + '/AMD/Source',
            SUITESPARSE_SRC_DIR + '/COLAMD/Include',
            SUITESPARSE_SRC_DIR + '/COLAMD/Source',
            SUITESPARSE_SRC_DIR + '/BTF/Include',
            SUITESPARSE_SRC_DIR + '/BTF/Source',
            SUITESPARSE_SRC_DIR + '/SuiteSparse_config' ],
        library_dirs = [ BLAS_LIB_DIR ],
        define_macros = MACROS + [('NTIMER', '1'), ('NCHOLMOD', '1')],
        libraries = LAPACK_LIB + BLAS_LIB,
        extra_link_args = BLAS_EXTRA_LINK_ARGS,
        sources = ['src/C/klu.c' ] +
            [SUITESPARSE_SRC_DIR + '/SuiteSparse_config/SuiteSparse_config.c'] +
            glob('src/C/SuiteSparse_cvxopt_extra/klu/*'))

# Build for int or long?
if sys.maxsize > 2**31: MACROS += [('DLONG',None)]

if not SUITESPARSE_SRC_DIR:
    cholmod = Extension('cholmod',
        libraries = ['cholmod','colamd','amd'] + SUITESPARSE_CONF_LIB + LAPACK_LIB + BLAS_LIB + RT_LIB,
        include_dirs = [SUITESPARSE_INC_DIR],
        define_macros = MACROS,
        library_dirs = [SUITESPARSE_LIB_DIR, BLAS_LIB_DIR],
        sources = [ 'src/C/cholmod.c' ])
else:
    cholmod = Extension('cholmod',
        library_dirs = [ BLAS_LIB_DIR ],
        libraries = LAPACK_LIB + BLAS_LIB,
        include_dirs = [ SUITESPARSE_SRC_DIR + '/CHOLMOD/Include',
            SUITESPARSE_SRC_DIR + '/COLAMD',
            SUITESPARSE_SRC_DIR + '/AMD/Include',
            SUITESPARSE_SRC_DIR + '/COLAMD/Include',
            SUITESPARSE_SRC_DIR + '/SuiteSparse_config' ],
        define_macros = MACROS + [('NPARTITION', '1'), ('NTIMER', '1')],
        extra_link_args = BLAS_EXTRA_LINK_ARGS,
        sources = [ 'src/C/cholmod.c' ] +
            [SUITESPARSE_SRC_DIR + '/AMD/Source/' + s for s in ['amd_postorder.c', 'amd_post_tree.c', 'amd_2.c']] +
            [SUITESPARSE_SRC_DIR + '/COLAMD/Source/colamd.c'] +
            [SUITESPARSE_SRC_DIR + '/SuiteSparse_config/SuiteSparse_config.c'] +
            glob(SUITESPARSE_SRC_DIR + '/CHOLMOD/Core/c*.c') +
            glob(SUITESPARSE_SRC_DIR + '/CHOLMOD/Cholesky/c*.c') +
            [SUITESPARSE_SRC_DIR + '/CHOLMOD/Check/cholmod_check.c'] +
            glob(SUITESPARSE_SRC_DIR + '/CHOLMOD/Supernodal/c*.c') )

if not SUITESPARSE_SRC_DIR:
    amd = Extension('amd',
        libraries = ['amd'] + SUITESPARSE_CONF_LIB + RT_LIB,
        include_dirs = [SUITESPARSE_INC_DIR],
        define_macros = MACROS,
        library_dirs = [SUITESPARSE_LIB_DIR],
        sources = ['src/C/amd.c'])
else:
    amd = Extension('amd',
        include_dirs = [SUITESPARSE_SRC_DIR + '/AMD/Include',
            SUITESPARSE_SRC_DIR + '/SuiteSparse_config' ],
        define_macros = MACROS + [('NTIMER', '1')],
        sources = [ 'src/C/amd.c', SUITESPARSE_SRC_DIR + '/SuiteSparse_config/SuiteSparse_config.c'] +
        glob(SUITESPARSE_SRC_DIR + '/AMD/Source/*.c') )

misc_solvers = Extension('misc_solvers',
    libraries = LAPACK_LIB + BLAS_LIB,
    library_dirs = [ BLAS_LIB_DIR ],
    define_macros = MACROS,
    extra_link_args = BLAS_EXTRA_LINK_ARGS,
    sources = ['src/C/misc_solvers.c'] )

extmods += [base, blas, lapack, umfpack, klu, cholmod, amd, misc_solvers]


setup (name = 'kvxopt',
    description = 'Convex optimization package and Suite Sparse interface',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description = '''
KVXOPT is a fork from CVXOPT wich contains more functions and
wrappers to Suite Sparse library.

CVXOPT is a free software package for convex optimization based on the
Python programming language. It can be used with the interactive Python
interpreter, on the command line by executing Python scripts, or
integrated in other software via Python extension modules. Its main
purpose is to make the development of software for convex optimization
applications straightforward by building on Python's extensive standard
library and on the strengths of Python as a high-level programming
language.
''',
    author = 'M. Andersen, J. Dahl, L. Vandenberghe, and U. Sandoval',
    author_email = 'martin.skovgaard.andersen@gmail.com, dahl.joachim@gmail.com, vandenbe@ee.ucla.edu, sanurielf@gmail.com',
    url = '',
    license = 'GNU GPL version 3',
    ext_package = "kvxopt",
    ext_modules = extmods,
    package_dir = {"kvxopt": "src/python"},
    package_data = {'': ['*.dll', '*LICENSE']},
    packages = ["kvxopt"],
    install_requires = INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        ],
    zip_safe=False
    )
