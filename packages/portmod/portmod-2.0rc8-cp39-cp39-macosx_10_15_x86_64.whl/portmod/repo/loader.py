# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for directly loading pybuild files.
These functions should not be called directly.
See portmod.loader for functions to load pybuilds safely using a sandbox.
"""

import ast
import glob
import importlib
import importlib.util
import os
import sys
from copy import deepcopy
from functools import lru_cache
from logging import warning
from types import SimpleNamespace
from typing import Any, Callable, Dict, Generator, Optional, cast

from RestrictedPython import (
    RestrictingNodeTransformer,
    compile_restricted_exec,
    limited_builtins,
    safe_globals,
)
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import (
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
    safer_getattr,
)

from portmod.atom import Atom, FQAtom, QualifiedAtom, VAtom, atom_sat
from portmod.functools import install_cache
from portmod.globals import env
from portmod.l10n import l10n
from portmod.lock import vdb_lock
from portmod.parsers.manifest import Manifest
from portmod.pybuild import File, FullInstalledPybuild, FullPybuild, InstallDir
from portmod.repo import Repo
from portmod.repo.metadata import get_categories
from portmod.util import get_max_version

from . import get_repo, get_repo_name
from .metadata import get_masters
from .updates import get_moved

WHITELISTED_IMPORTS = {
    "filecmp",
    "os",
    "sys",
    "shutil",
    "os.path",
    "chardet",
    "pybuild",
    "pybuild.info",
    "pybuild.winreg",
    "re",
    "csv",
    "json",
    "typing",
    "fnmatch",
    "collections",
}


@lru_cache()
def _import_common(
    name: str,
    installed: bool,
    load_function: Callable,
    repo: Optional[str] = None,
) -> SimpleNamespace:
    """
    args:
        name: The import name as an absolute import path
        installed: Whether or not the package calling this is an installed package
        load_function: The function taking a file path and a keyword argument installed,
            indicating the installed status of the file to be loaded, to be used to load
            the common module

    returns:
        The Module as a SimpleNamespace
    """
    if len(name.split(".")) > 2:
        raise Exception(f"Invalid package {name}")
    _, module_name = name.split(".")
    base_atom = Atom(f"common/{module_name}")
    if installed:
        path = find_installed_path(base_atom)

    if installed and path:
        result = load_function(path, installed=True, repo=None)
    else:
        versions = {}
        for file in _iterate_pybuilds(base_atom, repo_name=repo):
            atom, _ = os.path.splitext(file)
            versions[VAtom("common/" + os.path.basename(atom)).PVR] = file

        max_version = get_max_version(versions.keys())
        if not max_version:
            raise Exception(f"Could not find package {name}")

        result = load_function(versions[max_version], installed=False, repo=repo)

    return SimpleNamespace(
        **{key: value for key, value in result.items() if not key.startswith("_")}
    )


def _import(installed: bool, repo: Optional[str] = None):
    def import_fn(name, globs, loc, fromlist, level):
        if name.startswith("common."):
            return _import_common(name, installed, __load_module, repo)
        if name not in WHITELISTED_IMPORTS:
            raise RuntimeError(f"Importing from {name} is not allowed")
        return __import__(name, globs, loc, fromlist, level)

    return import_fn


# Default implementation to handle invalid pybuilds
class Package:
    def __init__(self):
        raise Exception("Package is not defined")


def default_write_guard(ob):
    """Noop write guard"""
    return ob


def safer_hasattr(obj, name):
    """
    Version of hasattr implemented using safet_getattr

    This doesn't really provide any extra security, but does mean that
    str.format, and attributes beginning with underscores, which are
    blocked by safer_getattr, return False rather than True
    """
    try:
        safer_getattr(obj, name)
    except (NotImplementedError, AttributeError):
        return False
    return True


def default_apply(func, *args, **kwargs):
    return func(*args, **kwargs)


MINIMAL_GLOBALS: Dict[str, Any] = safe_globals
SAFE_GLOBALS: Dict[str, Any] = MINIMAL_GLOBALS.copy()
SAFE_GLOBALS["__builtins__"] = MINIMAL_GLOBALS["__builtins__"].copy()
SAFE_GLOBALS.update({"Package": Package})
SAFE_GLOBALS["__builtins__"].update(
    {
        "FileNotFoundError": FileNotFoundError,
        "__metaclass__": type,
        "_apply_": default_apply,
        "_getattr_": safer_getattr,
        "_getitem_": default_guarded_getitem,
        "_getiter_": default_guarded_getiter,
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_unpack_sequence_": guarded_unpack_sequence,
        "_write_": default_write_guard,
        "all": all,
        "any": any,
        "dict": dict,
        "enumerate": enumerate,
        "filter": filter,
        "frozenset": frozenset,
        "getattr": safer_getattr,
        "hasattr": safer_hasattr,
        "iter": iter,
        "map": map,
        "max": max,
        "min": min,
        "next": next,
        "reversed": reversed,
        "set": set,
        "sorted": sorted,
        "sum": sum,
        "super": super,
    }
)
SAFE_GLOBALS["__builtins__"].update(limited_builtins)

SANDBOX_GLOBALS: Dict[str, Any] = SAFE_GLOBALS.copy()
SANDBOX_GLOBALS["__builtins__"] = SAFE_GLOBALS["__builtins__"].copy()


class PrintWrapper:
    def __init__(self, _getattr_=None):
        self.txt = []
        self._getattr_ = _getattr_

    def write(self, text):
        self.txt.append(text)

    def __call__(self):
        return "".join(self.txt)

    def _call_print(self, *objects, **kwargs):
        if kwargs.get("file", None) is None:
            kwargs["file"] = sys.stdout
        else:
            self._getattr_(kwargs["file"], "write")
        print(*objects, **kwargs)


# print and open are only allowed within the sandbox
SANDBOX_GLOBALS["__builtins__"].update({"_print_": PrintWrapper, "open": open})


class Policy(RestrictingNodeTransformer):
    def visit_JoinedStr(self, node):
        return self.node_contents_visit(node)

    def visit_FormattedValue(self, node):
        return self.node_contents_visit(node)

    def visit_AnnAssign(self, node):
        return self.node_contents_visit(node)

    def visit_AugAssign(self, node):
        return self.node_contents_visit(node)

    def visit_ImportFrom(self, node):
        if (
            node.module in WHITELISTED_IMPORTS
            or node.module.startswith("pybuild")
            and node.level == 0
        ):
            try:
                module = importlib.import_module(node.module)
                for name in node.names:
                    if isinstance(module.__dict__.get(name.name), type(importlib)):
                        self.error(
                            node, "Importing modules from other modules is forbidden"
                        )
            except ModuleNotFoundError:
                pass

        return RestrictingNodeTransformer.visit_ImportFrom(self, node)

    def visit_FunctionDef(self, node):
        node = RestrictingNodeTransformer.visit_FunctionDef(self, node)
        if node.name == "__init__":
            newnode = ast.parse("super().__init__()").body[0]
            newnode.lineno = node.lineno
            newnode.col_offset = node.col_offset
            node.body.insert(0, newnode)
        return node


def restricted_load(code, filepath: str, _globals: Dict[str, Any]):
    if sys.platform == "win32":
        code = code.replace("\\", "\\\\")
    byte_code, errors, warnings, names = compile_restricted_exec(
        code, filename=filepath, policy=Policy
    )
    if errors:
        raise SyntaxError(errors)
    seen: Dict[str, str] = {}
    for message in [seen.setdefault(x, x) for x in warnings if x not in seen]:
        if not message.endswith("Prints, but never reads 'printed' variable."):
            warning(f"In file {filepath}: {message}")
    exec(byte_code, _globals, _globals)


@install_cache
def get_atom_from_path(path: str) -> FQAtom:
    repopath, filename = os.path.split(os.path.abspath(os.path.normpath(path)))
    atom, _ = os.path.splitext(filename)
    repopath, _ = os.path.split(repopath)
    repopath, C = os.path.split(repopath)
    try:
        repo_name = get_repo_name(repopath)
    except FileNotFoundError as e:
        path = os.path.join(os.path.dirname(path), "REPO")
        if os.path.exists(path):
            with open(path, "r") as file:
                repo_name = file.read().strip() + "::installed"
        else:
            raise e
    return FQAtom(f"{C}/{atom}::{repo_name}")


def __load_module(
    path: str, *, installed=False, repo: Optional[str] = None
) -> Dict[str, Any]:
    filename, _ = os.path.splitext(os.path.basename(path))

    with open(path, "r", encoding="utf-8") as file:
        code = file.read()
        tmp_globals = SANDBOX_GLOBALS.copy()
        tmp_globals["__builtins__"]["__import__"] = _import(
            installed=installed, repo=repo
        )
        tmp_globals["__name__"] = filename
        restricted_load(code, path, tmp_globals)

    return tmp_globals


def __load_file_common(
    path: str, module: Dict[str, Any], installed: bool, repo: Optional[str]
):
    module["Package"].__pybuild__ = path
    pkg = module["Package"]()
    pkg.FILE = os.path.abspath(path)
    pkg.INSTALLED = False

    if not installed:
        # determine common dependencies
        def find_common_imports(file: str):
            depends = []
            with open(file, "r", encoding="utf-8") as fp:
                tree = ast.parse(fp.read())

            def find_imports(tree: ast.AST):
                if isinstance(tree, ast.Module):
                    for statement in tree.body:
                        if isinstance(statement, ast.Import):
                            for alias in statement.names:
                                if alias.name.startswith("common."):
                                    depends.append(alias.name.replace(".", "/"))
                        elif isinstance(statement, ast.ImportFrom):
                            if statement.module and statement.module.startswith(
                                "common."
                            ):
                                depends.append(statement.module.replace(".", "/"))

            # Globals
            find_imports(tree)
            # TODO: Inline imports in functions?
            return depends

        pkg.RDEPEND = " ".join([pkg.RDEPEND] + find_common_imports(pkg.FILE))
    return pkg


def __load_file(path: str, *, installed=False) -> FullPybuild:
    """
    Loads a pybuild file

    :param path: Path of the pybuild file
    """
    repo = get_repo_name(path) if not installed else None
    module = __load_module(path, installed=installed, repo=repo)
    pkg = __load_file_common(path, module, installed, repo)
    return cast(FullPybuild, pkg)


def __safe_load_file(path: str, *, installed=False) -> FullPybuild:
    """
    Loads a pybuild file

    :param path: Path of the pybuild file
    """
    repo = get_repo_name(path) if not installed else None
    module = __safe_load_module(path, installed, repo)
    pkg = __load_file_common(path, module, installed, repo)
    pkg.ATOM = get_atom_from_path(path)
    pkg.REPO = pkg.ATOM.R
    if installed:
        __load_installed_common(pkg, path)
    return cast(FullPybuild, pkg)


def __load_installed(file: str) -> FullInstalledPybuild:
    """
    Loads an installed pybuild

    :param file: Path of the pybuild file
    """
    mod = cast(FullInstalledPybuild, __load_file(file, installed=True))
    __load_installed_common(mod, file)
    return mod


@vdb_lock()
def __load_installed_common(mod, file: str):
    """Shared code for loading installed pybuilds"""
    mod.INSTALLED = True
    parent = os.path.dirname(file)

    def read_file(name: str) -> Optional[str]:
        if os.path.exists(os.path.join(parent, name)):
            with open(os.path.join(parent, name), "r") as repo_file:
                return repo_file.read().strip()
        return None

    repo = read_file("REPO")
    if not repo:
        raise Exception(
            f"Internal Error: Installed package in file {file}"
            "has no repository identifier"
        )
    mod.REPO = repo
    mod.INSTALLED_USE = set((read_file("USE") or "").split())
    mod.RDEPEND = read_file("RDEPEND") or mod.RDEPEND
    mod.INSTALLED_REBUILD_FILES = None
    path = os.path.join(parent, "REBUILD_FILES")
    if os.path.exists(path):
        try:
            mod.INSTALLED_REBUILD_FILES = Manifest(path)
        except ValueError:
            warning(f"Failed to load {path}")


def _iterate_installed() -> Generator[str, None, None]:
    repo = env.prefix().INSTALLED_DB

    for path in glob.glob(os.path.join(repo, "*", "*", "*.pybuild")):
        yield path


def find_installed_path(atom: Atom) -> Optional[str]:
    repo_path = env.prefix().INSTALLED_DB

    # Handle renames:
    # Check all possible renames for this atom (all repos), and they are only valid if
    # the package comes from the repo matching the rename entry
    for repo in env.REPOS:
        moved = get_moved(repo)
        if atom.CPN in moved:
            moved_atom = QualifiedAtom(moved[atom.CPN])
            path = os.path.join(repo_path, moved_atom.C, moved_atom.PN)
            if os.path.exists(path):
                with open(os.path.join(path, "REPO"), "r") as file:
                    if repo.name == file.read().strip():
                        atom = moved_atom
                        break

    if atom.C:
        path = os.path.join(repo_path, atom.C, atom.PN)
        if os.path.exists(path):
            results = glob.glob(os.path.join(path, "*.pybuild"))
            assert len(results) == 1
            return results[0]
    else:
        for dirname in glob.glob(os.path.join(repo_path, "*")):
            path = os.path.join(repo_path, dirname, atom.PN)
            if os.path.exists(path):
                results = glob.glob(os.path.join(path, "*.pybuild"))
                assert len(results) == 1
                return results[0]
    return None


def _iterate_pybuilds(
    atom: Optional[Atom] = None,
    repo_name: Optional[str] = None,
    only_repo_root: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Iterates over pybuilds.

    If no repository is given, checks all available.
    If a repository name is given, checks that repository and its masters

    if only_repo_root is specified, only checks the repository at the given location
    """
    path = None
    repos = []
    if env.PREFIX_NAME:
        repos = env.prefix().REPOS
    else:
        repos = env.REPOS

    if repo_name is not None:
        repo = get_repo(repo_name)
        repos = [repo]
        for master in get_masters(repo.location):
            yield from _iterate_pybuilds(atom, master.name)
    elif only_repo_root:
        repos = [Repo(location=only_repo_root, name=get_repo_name(only_repo_root))]

    def valid_atom(desired_atom: Atom, other: Atom):
        if isinstance(desired_atom, FQAtom):
            return desired_atom == other
        else:
            return atom_sat(other, desired_atom)

    def try_move_atom(moved: Dict[str, str], atom: QualifiedAtom, repo):
        true_atom = atom
        if atom.CPN in moved:
            true_atom = QualifiedAtom(moved[atom.CPN])
            if atom.PVR:
                true_atom = QualifiedAtom(f"{true_atom}-{atom.PVR}")
        return true_atom

    for repo in repos:
        if not os.path.exists(repo.location):
            warning(
                l10n(
                    "repo-does-not-exist-warning",
                    name=repo.name,
                    path=repo.location,
                    command="omwmerge --sync",
                )
            )

        if atom:
            moved = get_moved(repo)
            if atom.C:
                true_atom = try_move_atom(moved, cast(QualifiedAtom, atom), repo)
                path = os.path.join(repo.location, true_atom.C, true_atom.PN)
                if path is not None and os.path.exists(path):
                    for file in glob.glob(os.path.join(path, "*.pybuild")):
                        if valid_atom(true_atom, get_atom_from_path(file)):
                            yield file
            else:
                for category in get_categories(repo.location):
                    true_atom = try_move_atom(
                        moved, QualifiedAtom(category + "/" + atom), repo
                    )
                    path = os.path.join(repo.location, category, true_atom.PN)

                    if path is not None and os.path.exists(path):
                        for file in glob.glob(os.path.join(path, "*.pybuild")):
                            if valid_atom(true_atom, get_atom_from_path(file)):
                                yield file
        else:
            for file in glob.glob(os.path.join(repo.location, "*", "*", "*.pybuild")):
                yield file


def pkg_exists(atom: Atom, *, repo_name: Optional[str] = None) -> bool:
    """Returns true if a package with the given atom can be found in the given repository"""
    return next(_iterate_pybuilds(atom, repo_name), None) is not None


def __safe_load_module(path: str, installed: bool, repo: Optional[str]):
    try:
        atom: Optional[FQAtom] = get_atom_from_path(path)
    except Exception:
        atom = None

    def get_info():
        assert atom
        return {
            "CATEGORY": atom.C,
            "P": atom.P,
            "PF": atom.PF,
            "PN": atom.PN,
            "PV": atom.PV,
            "PR": atom.PR,
            "PVR": atom.PVR,
            "__name__": "pybuild.info",
        }

    def get_pybuild():
        # File/InstallDir/Pybuild1 objects are instead passed as functions
        # to prevent modification of class attributes.
        # the instances are safe as long as underscored attributes are inaccessible

        def file_func(*args, **kwargs):
            return File(*args, **kwargs)

        def install_dir_func(*args, **kwargs):
            return InstallDir(*args, **kwargs)

        # create simplified version of Pybuild to use for inheritance.
        # It has default values for all the pyubild fields.
        # We don't use FullPybuild directly to prevent its fields being modified
        # This class is generated within a function, and thus will not be the same
        # for any two packages.
        class Pybuild1(FullPybuild):
            """Generated Pybuild1 for use in non-sandboxed loader"""

        return {
            "File": file_func,
            "InstallDir": install_dir_func,
            "Pybuild1": Pybuild1,
            "DOWNLOAD_DIR": env.DOWNLOAD_DIR,
            "version_gt": None,
            "find_file": None,
            "use_reduce": None,
            "patch_dir": None,
            "get_masters": None,
            "apply_patch": None,
            "__name__": "pybuild",
        }

    def get_typing():
        import typing

        result = {}

        for attr, value in typing.__dict__.items():
            if not attr.startswith("_") and not isinstance(value, type(typing)):
                result[attr] = deepcopy(value)

        return result

    def _import(name, _globs, _loc, _fromlist, _level):
        if name.startswith("common."):
            return deepcopy(_import_common(name, installed, __safe_load_module, repo))
        if name == "pybuild":
            return SimpleNamespace(**get_pybuild())
        if name == "pybuild.info":
            return SimpleNamespace(**get_info())
        if name == "typing":
            return SimpleNamespace(**get_typing())
        if _fromlist:
            return SimpleNamespace(**{item: None for item in _fromlist})
        else:

            class NoAttr:
                def __getattr__(self, attr):
                    # Necessary so that the object can be copied
                    # Note that RestrictedPython prevents use of such attributes through ast parsing
                    if attr.startswith("_"):
                        return super().__getattr__(attr)  # type: ignore  # pylint: disable=no-member
                    raise RuntimeError(
                        f"Cannot use {name}.{attr}: Complex code in the global scope is not allowed!"
                    )

            return NoAttr()

    filename, _ = os.path.splitext(os.path.basename(path))

    with open(path, "r", encoding="utf-8") as file:
        code = file.read()
        tmp_globals = deepcopy(SAFE_GLOBALS)
        tmp_globals["__builtins__"]["__import__"] = _import
        tmp_globals["__name__"] = filename
        restricted_load(code, path, tmp_globals)
        for _global in tmp_globals.values():
            # Note: we can't use hasattr here, as we want to set the attribute for this classmethod
            if isinstance(_global, type) and "__file__" not in _global.__dict__:
                try:
                    setattr(_global, "__file__", path)
                except:  # noqa
                    ...

    return tmp_globals
