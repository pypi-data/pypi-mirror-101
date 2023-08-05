import ctypes
from ctypes import CFUNCTYPE, POINTER, c_char_p, c_double, c_int
import math
import os
from pathlib import Path
import sys

import dlsym
import pytest


def test_atan2():
    atan2 = CFUNCTYPE(c_double, c_double, c_double)(
        dlsym.dlsym("atan2"))
    assert atan2 and atan2(1, 2) == math.atan2(1, 2)


def test_tcl():
    pytest.importorskip("tkinter")  # Python calls Tcl_FindExecutable for us.
    getnameofexecutable = CFUNCTYPE(c_char_p)(
        dlsym.dlsym("Tcl_GetNameOfExecutable"))
    # On Windows, separators must be normalized.
    assert Path(os.fsdecode(getnameofexecutable())) == Path(sys.executable)


def test_blas():
    pytest.importorskip("numpy")
    dasum = CFUNCTYPE(c_double, c_int, POINTER(c_double), c_int)(
        dlsym.dlsym("cblas_dasum"))
    buf = (c_double * 10)(*range(10))
    assert dasum and dasum(10, buf, 1) == 45


def test_fftw():
    pytest.importorskip("pyfftw")
    alignment_of = CFUNCTYPE(c_int, POINTER(c_double))(
        dlsym.dlsym("fftw_alignment_of"))
    buf = (c_double * 10)(*range(10))
    a0 = alignment_of(buf)
    a1 = alignment_of(
        ctypes.cast(ctypes.addressof(buf) + ctypes.sizeof(c_double),
                    POINTER(c_double)))
    assert (a1 - a0) % ctypes.sizeof(c_double) == 0
