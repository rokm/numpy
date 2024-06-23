"""This hook should collect all binary files and any hidden modules that numpy
needs.

Our (some-what inadequate) docs for writing PyInstaller hooks are kept here:
https://pyinstaller.readthedocs.io/en/stable/hooks.html

"""
from PyInstaller.utils.hooks import (
    collect_dynamic_libs,
    get_installer,
    is_module_satisfies,
    logger
)

# Collect all DLLs inside numpy's installation folder, dump them into built
# app's root.
binaries = collect_dynamic_libs("numpy", ".")

# If using Anaconda-packaged numpy, collect shared libraries using
# conda-specific utility function.
try:
    installer = get_installer("numpy")
except Exception:
    logger.warning("hook-numpy: failed to determine installer!", exc_info=True)
    installer = None

if installer == "conda":
    # Assume running the NumPy from Conda-forge and collect it's DLLs from the
    # communal Conda bin directory. DLLs from NumPy's dependencies must also be
    # collected to capture MKL, OpenBlas, OpenMP, etc.
    from PyInstaller.utils.hooks import conda_support
    datas = conda_support.collect_dynamic_libs("numpy", dependencies=True)

# Submodules PyInstaller cannot detect.  `_dtype_ctypes` is only imported
# from C and `_multiarray_tests` is used in tests (which are not packed).
hiddenimports = ['numpy._core._dtype_ctypes', 'numpy._core._multiarray_tests']

# Remove testing and building code and packages that are referenced throughout
# NumPy but are not really dependencies.
excludedimports = [
    "scipy",
    "pytest",
]
