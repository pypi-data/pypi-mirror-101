#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#if !_WIN32
#include <dlfcn.h>
#else
#define NOMINMAX
#define UNICODE
#define _UNICODE
#include <Windows.h>
#define PSAPI_VERSION 1
#include <Psapi.h>
#endif

namespace {

namespace py = pybind11;
using namespace pybind11::literals;

uintptr_t py_dlsym(std::string symbol)
{
  auto addr = uintptr_t{};
  auto path = py::str{"<unknown path>"};
#if !_WIN32
  auto modules = py::module::import("sys").attr("modules").cast<py::dict>();
  auto suffixes =
    py::tuple(py::module::import("importlib.machinery").attr("EXTENSION_SUFFIXES"));
  for (auto& kv: modules) {
    auto file = py::getattr(kv.second, "__file__", py::cast(""));
    if (file.is_none() || !file.attr("endswith")(suffixes).cast<bool>()) {
      continue;
    }
    if (auto handle = dlopen(file.cast<std::string>().c_str(), RTLD_LAZY)) {
      addr = reinterpret_cast<uintptr_t>(dlsym(handle, symbol.c_str()));
      dlclose(handle);
    }
    if (addr) {
      auto dlinfo = Dl_info{};
      if (dladdr(reinterpret_cast<void*>(addr), &dlinfo)) {
        path = dlinfo.dli_fname;
      }
      break;
    }
  }
#else
  auto process = GetCurrentProcess();
  auto n_bytes = DWORD{};
  if (!EnumProcessModules(process, nullptr, 0, &n_bytes)) {
    PyErr_SetFromWindowsErr(0);
    throw py::error_already_set{};
  }
  auto n_modules = n_bytes / sizeof(HMODULE);
  auto modules = std::unique_ptr<HMODULE[]>{new HMODULE[n_modules]};
  if (!EnumProcessModules(process, modules.get(), n_bytes, &n_bytes)) {
    PyErr_SetFromWindowsErr(0);
    throw py::error_already_set{};
  }
  for (auto i = 0; i < n_modules; ++i) {
    if (addr = reinterpret_cast<uintptr_t>(GetProcAddress(modules[i], symbol.c_str()))) {
      wchar_t wpath[MAX_PATH];
      if (GetModuleFileNameEx(process, modules[i], wpath, MAX_PATH)) {
        path = py::reinterpret_steal<py::str>(PyUnicode_FromWideChar(wpath, -1));
      }
      break;
    }
  }
#endif
  if (addr) {
    py::module::import("logging").attr("getLogger")("dlsym").attr("info")(
      "Loaded %s from %s", symbol, path);
  }
  return addr;
}

}

PYBIND11_MODULE(dlsym, m) {
  m.doc() = R"__doc__(
Function loader.
)__doc__";

  m.def("dlsym", py_dlsym, "symbol"_a, R"__doc__(
Locate *symbol* from the currently loaded libraries.

On POSIX, *symbol* is searched through the currently loaded extension
modules.  On Windows, *symbol* is searched through the DLLs enumerated by
EnumProcessModules.

Parameters
----------
symbol : str
    The searched symbol.

Returns
-------
int
    The address of the symbol, if it can be found; 0 otherwise.

Examples
--------
.. code-block:: cpp

    double (* my_atan2)(double, double);
    my_atan2 = reinterpret_cast<decltype(my_atan2)>(
        py::module::import("dlsym").attr("dlsym")("atan2").cast<uintptr_t>());

.. code-block:: python

    from ctypes import *
    my_atan2 = CFUNCTYPE(c_double, c_double, c_double)(dlsym.dlsym("atan2"))
)__doc__");
}
