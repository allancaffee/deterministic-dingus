# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>, Allan Caffee <allan.caffee@gmail.com>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of “git describe”, modified to conform to the versioning
# scheme that setuptools uses.  If “git describe” returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the RELEASE-VERSION file.
#
# To use this script, simply import it your setup.py file, and use the
# results of get_git_version() as your package version:
#
# from version import *
#
# setup(
#     version=get_git_version(),
#     .
#     .
#     .
# )
#
# This will automatically update the RELEASE-VERSION file, if
# necessary.  Note that the RELEASE-VERSION file should *not* be
# checked into git; please add it to your top-level .gitignore file.
#
# You'll probably want to distribute the RELEASE-VERSION file in your
# sdist tarballs; to do this, just create a MANIFEST.in file that
# contains the following line:
#
#   include RELEASE-VERSION

__all__ = ("get_git_version")

from subprocess import Popen, PIPE
from os.path import isdir


def call_git_describe():

    # If the current directory doesn't have a .git directory than we may be
    # inside of somebody else's git repos.  This can happen if someone installs
    # our package from their project directory (e.g. with virtualenv).
    if not isdir('.git'):
        return None

    try:
        # Work around an apparent bug in git:
        # http://comments.gmane.org/gmane.comp.version-control.git/178169
        p = Popen(['git', 'status'], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        p.stdout.close()

        command = ['git', 'describe', '--abbrev=4', '--tags', '--dirty', '--match=v*']
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readline().strip()
        return line.lstrip('v')

    except:
        return None


def read_release_version():
    """Read the version from the file ``RELEASE-VERSION``"""
    try:
        with open("RELEASE-VERSION", "r") as f:
            version = f.readlines()[0]
            return version.strip()
    except:
        return None


def write_release_version(version):
    """Write `version` to the file ``RELEASE-VERSION``"""
    with open("RELEASE-VERSION", "w") as f:
        f.write("%s\n" % version)


def get_git_version():
    # Read in the version that's currently in RELEASE-VERSION.

    release_version = read_release_version()

    # First try to get the current version using “git describe”.

    version = call_git_describe()

    # If that doesn't work, fall back on the value that's in
    # RELEASE-VERSION.

    if not version:
        version = release_version

    # If we still don't have anything, that's an error.

    if version is None:
        raise ValueError("Cannot find the version number!")

    # If the current version is different from what's in the
    # RELEASE-VERSION file, update the file to be current.

    if version and release_version != version:
        write_release_version(version)

    # Finally, return the current version.

    return version


if __name__ == "__main__":
    print get_git_version()
