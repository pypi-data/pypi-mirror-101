# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Depclean tests
"""

import os
import sys

import pytest

from portmod.atom import Atom
from portmod.loader import load_installed_pkg
from portmod.merge import configure, deselect

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_depclean(setup):
    """
    Tests that deselected mods are then depcleaned
    """
    configure(["test/test-1.0", "test/test2-1.0"], no_confirm=True)
    assert load_installed_pkg(Atom("test/test2"))
    deselect(["test/test2"], no_confirm=True)
    configure([], no_confirm=True, depclean=True)
    assert not load_installed_pkg(Atom("test/test2"))

    assert load_installed_pkg(Atom("test/test"))
    deselect(["test/test"], no_confirm=True)
    configure([], no_confirm=True, depclean=True)
    # Note: test/test is a system mod, so it cannot be removed


@pytest.mark.xfail(
    sys.platform == "win32" and "APPVEYOR" in os.environ,
    reason="For some reason a file is being accessed by another process",
    raises=PermissionError,
)
def test_noarg_depclean(setup):
    """
    Tests that deselected mods are then depcleaned
    """
    configure(["test/test6-1.0"], no_confirm=True)
    configure(["test/test6-1.0"], no_confirm=True, delete=True)
    assert load_installed_pkg(Atom("test/test3"))
    configure([], no_confirm=True, depclean=True)
    assert not load_installed_pkg(Atom("test/test3"))
