import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#includefiles = ['gifsicle.exe', 'noimage.bin', 'CMN_binViewer_readme.txt']
includefiles = ['data.txt']
#exclude_libs = ['_ssl', 'pyreadline', 'doctest', 'locale','optparse', 'pickle', 'calendar', 'matplotlib', "BaseHTTPServer", "SocketServer", "dateutil", "email", "httplib", "itertools", "mpl_toolkits", "numpy.f2py", "pydoc_data", "random", "urllib", "urllib2", "xml", "zipfile", "zipimport", "scipy.sparse.linalg.eigen.arpack", "scipy.sparse._sparsetools"]
exclude_libs = []
build_exe_options = {"packages": ["scipy.special._ufuncs_cxx", "scipy.sparse", "scipy.stats", "scipy.integrate", "matplotlib.backends.backend_tkagg"], 'include_files':includefiles, "excludes":exclude_libs, "include_msvcr":True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

setup(  name = "GaussFit",
        version = "0.1",
        options = {"build_exe": build_exe_options},
        executables = [Executable("GaussFit.py", base=base)])