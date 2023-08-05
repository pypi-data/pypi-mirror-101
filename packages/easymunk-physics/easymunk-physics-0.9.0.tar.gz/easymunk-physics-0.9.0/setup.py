from pathlib import Path
import re
from setuptools import setup, find_packages  # type: ignore

version_re = re.compile(r"""(?<![\w_])version\s+=\s+['"]([^'"]+)['"]""")


def read_version():
    src = (PACKAGE_DIR / "_version.py").read_text()
    (res,) = version_re.findall(src)
    return res


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Games/Entertainment",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: pygame",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

PACKAGE_DIR = Path("easymunk")
long_description = Path("README.rst").read_text()
version = read_version()

setup(
    name="easymunk-physics",
    url="http://fabiommendes.github.io/easymunk/",
    author="Fábio Mendes",
    author_email="fabiomacedomendes@gmail.com",
    version=version,
    description="Easymunk is a easy-to-use pythonic 2d physics library",
    long_description=long_description,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license="MIT License",
    classifiers=classifiers,
    command_options={
        "build_sphinx": {
            "build_dir": ("setup.py", "docs"),
            "source_dir": ("setup.py", "docs/src"),
        }
    },
    python_requires=">=3.8",
    # Require >1.14.0 since that (and older) has problem with returning structs
    # from functions.
    setup_requires=["cffi > 1.14.0"],
    install_requires=["cffi > 1.14.0", "sidekick"],
    # For now, we use pymunk to supply the C module
    # cffi_modules=["easymunk/extension_build.py:ffibuilder"],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "sphinx",
            "aafigure",
            "wheel",
            "matplotlib",
            "hypothesis",
            "readme_renderer",
            "sphinx-autodoc-typehints",
            "flake8",
            "mypy",
        ],
        "backends": [
            "pyglet",
            "pygame",
            "pytest",
            "pyxel",
            "streamlit",
        ],
    },
)
