# =============================================================================
# Imports
# =============================================================================

# Standard
from distutils.command.clean import clean as Clean
from pkg_resources import parse_version
from platform import python_version
from os import unlink, walk
from os.path import abspath, exists, join, splitext
import shutil
import sys
import traceback
import os

# Local application
import sklr


# =============================================================================
# Constants
# =============================================================================

# Name and version
DISTNAME = "scikit-lr"
VERSION = sklr.__version__

# Description
DESCRIPTION = "A set of Python modules for Label Ranking problems."
with open("README.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

# Maintainer
MAINTAINER = "Juan Carlos Alfaro Jiménez"
MAINTAINER_EMAIL = "JuanCarlos.Alfaro@uclm.es"

# URLs
URL = "https://github.com/alfaro96/scikit-lr"
DOWNLOAD_URL = "https://pypi.org/project/scikit-lr/#files"
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/alfaro96/scikit-lr/issues",
    "Source Code": "https://github.com/alfaro96/scikit-lr",
    "Docker": "https://github.com/alfaro96/docker-scikit-lr"
}

# License
LICENSE = "MIT"

# Classifiers
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Unix",
    "Programming Language :: C",
    "Programming Language :: C++",
    "Programming Language :: Cython",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Scientific/Engineering :: Artificial Intelligence"
]

# Minimum version of the required packages
NUMPY_MIN_VERSION = "1.17.3"
SCIPY_MIN_VERSION = "1.3.2"
INSTALL_REQUIRES = [
    "numpy>={}".format(NUMPY_MIN_VERSION),
    "scipy>={}".format(SCIPY_MIN_VERSION),
]


# =============================================================================
# Classes
# =============================================================================

# =============================================================================
# Clean command
# =============================================================================
class CleanCommand(Clean):
    """Custom clean command to remove build artifacts."""

    def run(self):
        """Execute the custom clean command."""
        # Call to the run method of the parent
        # to clean common files and directories
        Clean.run(self)

        # Locate the current working directory
        # to clean the directories and files on it
        cwd = abspath(os.path.dirname(__file__))

        # Remove the .c and .cpp files if the current working directory is
        # not a distribution (that is, the "PKG-INFO" file does not exist),
        # since the source files are needed by the package in release mode
        remove_c_files = not exists(join(cwd, "PKG-INFO"))

        # Remove the build directory
        if exists("build"):
            shutil.rmtree("build")

        # Remove the .pytest_cache directory
        if exists(".pytest_cache"):
            shutil.rmtree(".pytest_cache")

        # Look for the directories and files
        # to remove under the sklr module
        for (dirpath, dirnames, filenames) in walk("sklr"):
            # Look for the files to remove
            for filename in filenames:
                # Get the current extension of the file
                filename_ext = splitext(filename)[1]
                # Check whether this file corresponding to .c or .cpp
                # taking into account whether they must be removed
                if filename_ext in {".c", ".cpp"} and remove_c_files:
                    # Only remove the .c and .cpp files that have been
                    # generated by Cython, that is, if they exists, in
                    # the same directory, a .pyx file with the same name
                    pyx_filename = str.replace(filename, filename_ext, ".pyx")
                    # If this .pyx file exists, then, remove
                    # the corresponding .c or .cpp one
                    if exists(join(dirpath, pyx_filename)):
                        unlink(join(dirpath, filename))
            # Look for the directories to remove
            for dirname in dirnames:
                # Remove the __pycache__ and .pytest_cache directories
                if dirname in {"__pycache__", ".pytest_cache"}:
                    shutil.rmtree(join(dirpath, dirname))


# Custom actions that can be carried
# out when calling to this setup file
# (defined custom clean command)
CMDCLASS = {"clean": CleanCommand}

# Optional setuptools features
# (require that it is imported)
SETUPTOOLS_EXTRA_COMMANDS = {
    "alias", "bdist_egg", "bdist_wheel",
    "develop", "dist_info", "easy_install",
    "egg_info", "install_egg_info", "rotate",
    "saveopts", "setopt", "test", "upload_docs"
}

# Import setuptools if at least one of
# the extra commands have been required
if SETUPTOOLS_EXTRA_COMMANDS.intersection(sys.argv):
    # Import
    import setuptools
    # Optimize
    EXTRA_SETUPTOOLS_ARGS = {
        "zip_false": False,
        "include_package_data": True,
        "extras_require": {
            "all_deps": INSTALL_REQUIRES
        }
    }

# Set the extra arguments as an empty set
# as far as the setuptools are not required
EXTRA_SETUPTOOLS_ARGS = {}


# =============================================================================
# Methods
# =============================================================================

def get_numpy_version():
    """Return a string containing the NumPy
    version (empty string if not installed)."""
    # Try to import NumPy and if it is not
    # found, show an error message to the user
    try:
        # Import
        import numpy as np
        # Get the version
        numpy_version = np.__version__
    except ImportError:
        # Show the error message
        traceback.print_exc()
        # Set the version to an empty string
        numpy_version = ""

    # Return the installed
    # version of NumPy
    return numpy_version


def configuration(parent_package="", top_path=None):
    """Configure the scikit-lr package."""
    # Before building the extensions, remove .MANIFEST.
    # Otherwise it may not be properly updated when
    # the contents of directories change
    if exists("MANIFEST"):
        unlink("MANIFEST")

    # Locally import the distribution utils of NumPy
    # to avoid that an import error is shown before
    # checking whether it is installed in the system
    from numpy.distutils.misc_util import Configuration

    # Create the configuration file of the scikit-lr package
    config = Configuration(None, parent_package, top_path)

    # Remove useless messages
    # from the configuration file
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True)

    # Add to the configuration file the
    # subpackage with the sklr module
    config.add_subpackage("sklr")

    # Return the configuration file
    # of the scikit-lr package
    return config


def setup_package():
    """Setup the scikit-lr package."""
    # Setup the metadata of the scikit-lr package
    # (all information has been previously defined)
    metadata = dict(
        name=DISTNAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        url=URL,
        download_url=DOWNLOAD_URL,
        project_urls=PROJECT_URLS,
        license=LICENSE,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        cmdclass=CMDCLASS,
        **EXTRA_SETUPTOOLS_ARGS)

    # For some actions like installing from pip, NumPy is not
    # required. Therefore, setuptools are employed in such cases
    if (len(sys.argv) == 1 or
            len(sys.argv) >= 2 and ("--help" in sys.argv[1:] or
                                    sys.argv[1] in (
                                        "--help-commands",
                                        "egg_info",
                                        "--version",
                                        "clean"))):
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup
    # Otherwise, NumPy is required. Therefore, its
    # setup configuration method must be imported
    else:
        # Ensure that the Python version installed in the system
        # is greater than or equal the minimum required version
        if sys.version_info < (3, 6):
            raise RuntimeError("scikit-lr requires Python 3.6 or later. "
                               "The current Python version is {} "
                               "installed in {}."
                               .format(python_version(), sys.executable))
        # Get the NumPy version
        # installed in the system
        numpy_version = get_numpy_version()
        # If NumPy is not installed, show an import error to
        # the user with the minimum required version of NumPy
        if not numpy_version:
            raise ImportError("NumPy is not installed. "
                              "At least version {} is required."
                              .format(NUMPY_MIN_VERSION))
        # Otherwise, if the installed version is not the minimum required one,
        # inform to the user about the got and the minimum required version
        elif parse_version(numpy_version) < parse_version(NUMPY_MIN_VERSION):
            raise ImportError("Your installation of NumPy is not "
                              "the required. Got {} but requires >={}."
                              .format(numpy_version, NUMPY_MIN_VERSION))
        # Import the setup method from NumPy
        # to install the scikit-lr package
        from numpy.distutils.core import setup
        # Setup the metadata of the configuration
        metadata["configuration"] = configuration

    # Setup the scikit-lr package
    # with the gathered metadata
    setup(**metadata)


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    setup_package()
