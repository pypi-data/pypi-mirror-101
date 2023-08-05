|GitHub|

.. |GitHub|
   image:: https://img.shields.io/badge/github-anntzer%2Fdlsym-brightgreen
   :target: https://github.com/anntzer/dlsym

dlsym -- A cross-platform symbol locator
========================================

``dlsym`` allows Python C extension modules to use symbols present in already
loaded C libraries, without having to actually link these libraries.  As a
simple example, using pybind11_:

.. code-block:: cpp

   double (* my_atan2)(double, double);
   my_atan2 = reinterpret_cast<decltype(my_atan2)>(
       py::module::import("dlsym").attr("dlsym")("atan2").cast<uintptr_t>());

.. _pybind11: https://pybind11.readthedocs.io/

Obviously, linking against ``libm`` to get access to ``atan2`` is not
particularly difficult, but this approach also allows one to use e.g.
``numpy``-provided BLAS/LAPACK functions which are available after importing
``numpy`` (regardless of whether the underlying implementation is OpenBLAS,
MKL, or something else), ``fftw`` functions after importing ``pyfftw``, or
``Tcl/Tk`` functions after importing ``tkinter`` (see tests for examples).

The main goal here is to simplify the compilation of such extension modules on
machines where the C libraries may not be present by default, but where they
can be "requested" by declaring an ``install_requires`` on the corresponding
Python package.

Note that the path to the shared library is not actually passed as an argument
to ``dlsym`` (unlike the POSIX ``dlsym(3)``.  This is because the symbol search
on Windows has to enumerate all loaded modules anyways, as one cannot just
pass a module that transitively loads the symbol.  On POSIX, we thus follow
the same strategy for consistency (but enumerating all extension modules in
``sys.modules`` instead).

The path of the library where the symbol is actually defined is logged at the
INFO level.

I learned this trick from Matthew Brett's original implementation for loading
``tkinter`` into ``matplotlib``.
