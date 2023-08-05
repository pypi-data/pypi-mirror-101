import os
from setupext import find_namespace_packages, setup


@setup.add_extensions
def make_extensions():
    from pybind11.setup_helpers import Pybind11Extension
    yield Pybind11Extension(
        "dlsym", ["src/dlsym.cpp"],
        cxx_std=11,
        libraries={"posix": ["dl"], "nt": ["psapi"]}[os.name],
    )


setup(
    name="dlsym",
    description="",
    long_description=open("README.rst", encoding="utf-8").read(),
    long_description_content_type="text/x-rst",
    author="Antony Lee",
    author_email="",
    url="https://github.com/anntzer/dlsym",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: zlib/libpng License",
        "Programming Language :: Python :: 3",
    ],
    cmdclass={},
    py_modules=[],
    packages=find_namespace_packages("lib"),
    package_dir={"": "lib"},
    package_data={},
    python_requires=">=3.6",
    setup_requires=[
        "pybind11>=2.6.0",
        "setuptools_scm>=3.3",  # fallback_version support.
    ],
    use_scm_version=lambda: {
        "version_scheme": "post-release",
        "local_scheme": "node-and-date",
        "fallback_version": "0+unknown",
    },
    install_requires=[
    ],
    entry_points={
        "console_scripts": [],
        "gui_scripts": [],
    },
)
