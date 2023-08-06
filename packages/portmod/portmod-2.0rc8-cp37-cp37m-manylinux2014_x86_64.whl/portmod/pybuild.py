# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Pybuild classes

Pybuilds are divided into two types:

1. The Pybuild class, which is used internally by portmod and includes several helper functions
2. The FullPybuild class, which is what packages inherit from and is accessible when loading

A third class, the BasePybuild, includes common code shared between Pybuild and FullPybuild
There is also an InstalledPybuild variant of the Pybuild, and a FullInstalledPybuild
variant of the FullPybuild which include information about the installed package.

Due to the Unsandboxed loader having full access to the FullPybuild, this class must
not implement any (non-private) functions which access the filesystem. Such functions
either belong in Pybuild, or Pybuild1 (the subclass of FullPybuild which is used by the
Sandboxed loader).
"""

import json
import lzma
import os
import urllib
import urllib.parse
from functools import lru_cache
from pathlib import Path
from typing import (
    AbstractSet,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    cast,
)

from portmod.atom import Atom, FQAtom, QualifiedAtom
from portmod.colour import green
from portmod.globals import env
from portmod.parsers.manifest import Manifest
from portmod.parsers.usestr import check_required_use, use_reduce
from portmod.repo import get_repo_name, get_repo_root
from portmod.source import Source, SourceManifest, get_archive_basename


class File:
    """Represents important installed files and their metadata"""

    def __init__(
        self,
        NAME: str,
        REQUIRED_USE: str = "",
        OVERRIDES: Union[str, List[str]] = [],
        **kwargs,
    ):
        """
        File objects also support a REQUIRED_USE variable, for , and an OVERRIDES variable for overriding other plugins in the load order.
        """
        self.__keys__: Set[str] = set()
        self.NAME: str = NAME
        """Name of the file relative to the root of the InstallDir"""
        self.REQUIRED_USE: str = REQUIRED_USE
        """
        Requirements for installing this file

        The default empty string is always satisfied.
        See Pybuild1.REQUIRED_USE for details on the syntax.
        """
        self.OVERRIDES: Union[str, List[str]] = OVERRIDES
        """
        A list of files which this overrides when sorting (if applicable).

        Can either be in the form of a string containing use-conditionals (note that
        this does not support files that contain spaces) or a list of files to override.
        Note that these overridden files are not considered masters and do not need to
        be present.

        For archives it determines the order in which the fallback archives will be
        searched during VFS lookups.
        """
        if REQUIRED_USE:
            self._add_kwarg("REQUIRED_USE", REQUIRED_USE)
        if OVERRIDES:
            self._add_kwarg("OVERRIDES", OVERRIDES)

        for key in kwargs:
            self._add_kwarg(key, kwargs[key])

    def _add_kwarg(self, key, value):
        self.__dict__[key] = value
        self.__keys__.add(key)

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'File("{self.NAME}"' + separator + ", ".join(kvps) + ")"

    def _to_cache(self):
        cache = {"NAME": self.NAME}
        for key in self.__keys__:
            cache[key] = getattr(self, key)

        cache["__type__"] = "File"
        return cache


class InstallDir:
    """
    Represents a directory in the Virtual File System

    Note that arbitrary arguments can be passed to the constructor, as
    repositories may make use of custom information.
    See the repository-level documentation for such information.
    """

    def __init__(
        self,
        PATH: str,
        REQUIRED_USE: str = "",
        PATCHDIR: str = ".",
        S: Optional[str] = None,
        WHITELIST: Optional[List[str]] = None,
        BLACKLIST: Optional[List[str]] = None,
        RENAME: Optional[str] = None,
        DATA_OVERRIDES: str = "",
        ARCHIVES: List[File] = [],
        **kwargs,
    ):
        self.PATH: str = PATH
        """
        The path to the data directory that this InstallDir represents
        relative to the root of the archive it is contained within.
        """
        self.REQUIRED_USE: str = REQUIRED_USE
        """
        A list of use flags with the same format as the package's
        REQUIRED_USE variable which enable the InstallDir if satisfied.
        Defaults to an empty string that is always satisfied.
        """
        self.PATCHDIR: str = PATCHDIR
        """
        The destination path of the InstallDir within the package's directory.

        Defaults to ".", i.e. the root of the mod directory. If multiple InstallDirs
        share the same PATCHDIR they will be installed into the same directory in the
        order that they are defined in the INSTALL_DIRS list.
        Each unique PATCHDIR has its own entry in the VFS, and its own sorting rules
        """
        self.S: Optional[str] = S
        """
        The source directory corresponding to this InstallDir.

        Similar function to S for the entire pybuild, this determines which directory
        contains this InstallDir, and generally corresponds to the name of the source
        archive, minus extensions. This is required for packages that contain more
        than one source, but is automatically detected for those with only one source
        if it is not specified, and will first take the value of Pybuild1.S, then the
        source's file name without extension if the former was not defined.
        """
        self.WHITELIST: Optional[List[str]] = WHITELIST
        """
        If present, only installs files matching the patterns in this list.
        fnmatch-style globbing patterns (e.g. * and [a-z]) can be used
        """
        self.BLACKLIST: Optional[List[str]] = BLACKLIST
        """
        If present, does not install files matching the patterns in this list.
        fnmatch-style globbing patterns (e.g. * and [a-z]) can be used
        """
        self.RENAME: Optional[str] = RENAME
        """
        Destination path of this directory within the final directory.

        E.g.::

            InstallDir("foo/bar", PATCHDIR=".", RENAME="bar")

        Will install the contents of ``foo/bar`` (in the source) into the directory
        ``bar`` inside the package's installation directory (and also the VFS).
        """
        self.DATA_OVERRIDES: str = DATA_OVERRIDES
        """
        A list of packages that this InstallDir should override in the VFS

        This only has a different effect from Pybuild1.DATA_OVERRIDES if multiple PATCHDIRs
        are set, as it can define overrides for individual PATCHDIRS, while
        Pybuild1.DATA_OVERRIDES affects all PATCHDIRs.
        See Pybuild1.DATA_OVERRIDES for details of the syntax.
        """
        self.ARCHIVES: List[File] = ARCHIVES
        """
        A list of File objects representing VFS archives.

        These will be searched, in order, during VFS file lookups if the file is not
        present in the package directories.
        """
        self.__keys__: Set[str] = set()
        if ARCHIVES:
            self._add_kwarg("ARCHIVES", ARCHIVES)
        if PATCHDIR != ".":
            self._add_kwarg("PATCHDIR", PATCHDIR)
        for arg in [
            "DATA_OVERRIDES",
            "RENAME",
            "BLACKLIST",
            "WHITELIST",
            "S",
            "REQUIRED_USE",
        ]:
            if getattr(self, arg):
                self._add_kwarg(arg, getattr(self, arg))
        for key in kwargs:
            self._add_kwarg(key, kwargs[key])

    def _add_kwarg(self, key, value):
        if isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict) and item.get("__type__") == "File":
                    file = dict(item)
                    file.pop("__type__", None)
                    new_value.append(File(**file))
                else:
                    new_value.append(item)
            value = new_value

        self.__dict__[key] = value
        self.__keys__.add(key)

    def get_files(self):
        """Generator function yielding file subattributes of the installdir"""
        for key in self.__dict__:
            if isinstance(getattr(self, key), list):
                for item in getattr(self, key):
                    if isinstance(item, File):
                        yield item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'InstallDir("{self.PATH}"' + separator + ", ".join(kvps) + ")"

    def _to_cache(self):
        cache = {"PATH": self.PATH}
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, list):
                new = []
                for item in value:
                    if isinstance(item, File):
                        new.append(item._to_cache())
                    else:
                        new.append(item)
                value = new
            cache[key] = value

        return cache


class BasePybuild:
    """
    Interface describing the Pybuild Type
    Only describes elements that are cached.
    This class cannot be used to install/uninstall mods
    """

    __file__ = __file__

    ATOM: FQAtom
    RDEPEND: str = ""
    DEPEND: str = ""
    SRC_URI: str = ""
    P: Atom
    PF: Atom
    PN: Atom
    CATEGORY: str
    PV: str
    PR: str
    PVR: str
    CPN: QualifiedAtom
    CP: QualifiedAtom
    REQUIRED_USE: str = ""
    RESTRICT: str = ""
    PROPERTIES: str = ""
    IUSE_EFFECTIVE: Set[str] = set()
    IUSE: Set[str] = set()
    TEXTURE_SIZES: str = ""
    DESC: str = ""
    NAME: str = ""
    HOMEPAGE: str = ""
    LICENSE: str = ""
    KEYWORDS: str = ""
    REBUILD_FILES: List[str] = []
    TIER: str = "a"
    FILE: str
    REPO: str
    INSTALLED: bool = False
    INSTALL_DIRS: List[InstallDir] = []
    DATA_OVERRIDES = ""
    S: Optional[str] = None  # Primary directory during prepare and install operations:w
    PATCHES: str = ""
    # Phase functions defined by the pybuild (or superclasses other than Pybuild1)
    # Used to determine if a function should be run, as certain functions don't have any default
    # behaviour
    FUNCTIONS: List[str] = []
    # Only set in phase functions
    USE: Set[str]

    def get_use(self) -> Set[str]:
        """Returns the enabled use flags for the package"""
        return self.USE

    def get_dir_path(self, install_dir: InstallDir) -> str:
        """Returns the installed path of the given InstallDir"""
        path = os.path.normpath(
            os.path.join(
                env.prefix().PACKAGE_DIR, self.CATEGORY, self.PN, install_dir.PATCHDIR
            )
        )
        if os.path.islink(path):
            return os.readlink(path)
        else:
            return path

    def get_file_path(self, install_dir: InstallDir, esp: File) -> str:
        return os.path.join(self.get_dir_path(install_dir), esp.NAME)

    def get_directories(self) -> Generator[InstallDir, None, None]:
        """
        Returns all enabled InstallDir objects in INSTALL_DIRS
        """
        for install_dir in self.INSTALL_DIRS:
            if check_required_use(
                install_dir.REQUIRED_USE, self.get_use(), self.valid_use
            ):
                yield install_dir

    def get_files(self, typ: str) -> Generator[Tuple[InstallDir, File], None, None]:
        """
        Returns all enabled files and their directories
        """
        for install_dir in self.get_directories():
            if hasattr(install_dir, typ):
                for file in getattr(install_dir, typ):
                    if check_required_use(
                        file.REQUIRED_USE, self.get_use(), self.valid_use
                    ):
                        yield install_dir, file

    def valid_use(self, use: str) -> bool:
        """Returns true if the given flag is a valid use flag for this mod"""
        return use in self.IUSE_EFFECTIVE


class Pybuild(BasePybuild):
    """Interface used internally to define helper functions on pybuilds"""

    def __init__(
        self, atom: FQAtom, cache: Optional[Dict] = None, *, FILE: str, **kwargs
    ):
        # Note: mypy doesn't like how we coerce INSTALL_DIRS
        if cache:
            self.__dict__ = cache
            self.INSTALL_DIRS = [
                InstallDir(**cast(Dict, idir)) for idir in self.INSTALL_DIRS
            ]
        for keyword, value in kwargs.items():
            setattr(self, keyword, value)
        self.ATOM = atom
        self.P = Atom(atom.P)
        self.PF = Atom(atom.PF)
        self.PN = Atom(atom.PN)
        self.CATEGORY = atom.C
        self.PV = atom.PV
        self.PR = atom.PR or "r0"
        self.PVR = atom.PVR
        self.CPN = QualifiedAtom(atom.CPN)
        self.CP = QualifiedAtom(atom.CP)
        self.__ENV = None
        self.INSTALLED = False
        self.FILE = FILE
        self.REPO_PATH = get_repo_root(self.FILE)
        if not self.REPO and self.REPO_PATH:
            self.REPO = get_repo_name(self.REPO_PATH)

    def __str__(self):
        return self.ATOM

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.FILE + ")"

    def get_manifest(self):
        """Returns the manifest object for the mod's sources"""
        if os.path.exists(manifest_path(self.FILE)):
            self._manifest = get_manifest(self.FILE)

        if hasattr(self, "_manifest"):
            return self._manifest

        return get_manifest(self.FILE)

    def _get_sources(
        self,
        uselist: AbstractSet[str] = frozenset(),
        masklist: AbstractSet[str] = frozenset(),
        matchnone=False,
        matchall=False,
    ) -> List[Source]:
        """
        Returns a list of sources that are enabled using the given configuration
        """
        sourcestr = self.SRC_URI
        sources = use_reduce(
            sourcestr,
            uselist,
            masklist,
            is_valid_flag=self.valid_use,
            is_src_uri=True,
            flat=True,
            matchnone=matchnone,
            matchall=matchall,
        )
        return parse_arrow(sources)

    def get_default_sources(self) -> List[SourceManifest]:
        """
        Returns a list of sources that are enabled
        with the current use configuration
        """
        return self.get_sources(self.get_use())

    def get_sources(
        self,
        uselist: AbstractSet[str] = frozenset(),
        masklist: AbstractSet[str] = frozenset(),
        matchnone=False,
        matchall=False,
    ) -> List[SourceManifest]:
        """
        Returns a list of sources that are enabled using the given configuration
        """
        sources = self._get_sources(uselist, masklist, matchnone, matchall)
        manifest = self.get_manifest()

        manifested_sources: List[SourceManifest] = []

        for source in sources:
            if manifest.get(source.name) is not None:
                m = manifest.get(source.name)
                manifested_sources.append(SourceManifest(source, m.hashes, m.size))
            else:
                raise Exception(f"Source {source.name}  is missing from the manifest!")

        return manifested_sources

    def get_use(self) -> Set[str]:
        """Returns the enabled use flags for the package"""
        from .config.use import get_use

        return get_use(self)[0]

    def parse_string(self, string, matchall=False):
        from .config.use import get_use

        if not matchall:
            (enabled, disabled) = get_use(self)
        else:
            (enabled, disabled) = (set(), set())

        return use_reduce(
            self.RESTRICT,
            enabled,
            disabled,
            is_valid_flag=self.valid_use,
            flat=True,
            matchall=matchall,
        )

    def get_restrict(self, *, matchall=False):
        """Returns parsed tokens in RESTRICT using current use flags"""
        # If we don't have a prefix there is no user configuration
        if not env.PREFIX_NAME:
            matchall = True
        return self.parse_string(self.RESTRICT, matchall=matchall)

    def get_properties(self, *, matchall=False):
        """Returns parsed tokens in PROPERTIES using current use flags"""
        return self.parse_string(self.PROPERTIES, matchall=matchall)

    def get_default_source_basename(self) -> Optional[str]:
        tmp_source = next(iter(self.get_default_sources()), None)
        if tmp_source:
            return get_archive_basename(tmp_source.name)
        return None

    def validate(self):
        """QA Checks pybuild structure"""
        from portmod.repo.loader import pkg_exists
        from portmod.repo.metadata import (
            check_use_expand_flag,
            get_global_use,
            get_package_metadata,
            get_use_expand,
            license_exists,
        )

        if not isinstance(self.RDEPEND, str):
            raise TypeError("RDEPEND must be a string")

        if not isinstance(self.DEPEND, str):
            raise TypeError("DEPEND must be a string")

        if not isinstance(self.SRC_URI, str):
            raise TypeError("SRC_URI must be a string")

        if not isinstance(self.DATA_OVERRIDES, str):
            raise TypeError("DATA_OVERRIDES must be a string")

        if not isinstance(self.LICENSE, str):
            raise TypeError(
                "LICENSE must be a string containing a space separated list of licenses"
            )

        if not isinstance(self.RESTRICT, str):
            raise TypeError(
                "RESTRICT must be a string containing a space separated list"
            )

        if not isinstance(self.PROPERTIES, str):
            raise TypeError(
                "PROPERTIES must be a string containing a space separated list"
            )

        IUSE_STRIP = set([use.lstrip("+") for use in self.IUSE])
        errors = []

        try:
            rdeps = use_reduce(self.RDEPEND, token_class=Atom, matchall=True, flat=True)
        except Exception as e:
            errors.append(f"Failed to parse RDEPEND: {e}")

        try:
            deps = use_reduce(self.DEPEND, token_class=Atom, matchall=True, flat=True)
        except Exception as e:
            errors.append(f"Failed to parse DEPEND: {e}")

        try:
            overrides = use_reduce(
                self.DATA_OVERRIDES, token_class=Atom, matchall=True, flat=True
            )
        except Exception as e:
            errors.append(f"Failed to parse DATA_OVERRIDES: {e}")

        for atom in rdeps + deps:
            if isinstance(atom, Atom) and not pkg_exists(atom, repo_name=self.REPO):
                errors.append(f"Dependency {atom} could not be found!")

        for atom in overrides:
            if isinstance(atom, Atom) and not pkg_exists(atom, repo_name=self.REPO):
                errors.append(f"Data Override {atom} could not be found!")

        try:
            use_reduce(self.PATCHES, matchall=True)
        except Exception as e:
            errors.append(f"Failed to parse PATCHES: {e}")

        for install in self.INSTALL_DIRS:
            if not isinstance(install, InstallDir):
                errors.append(
                    'InstallDir "{}" must have type InstallDir'.format(install.PATH)
                )
                continue
            for file in install.get_files():
                if not isinstance(file, File):
                    errors.append('File "{}" must have type File'.format(file))
                    continue

                try:
                    check_required_use(file.REQUIRED_USE, set(), self.valid_use)
                except Exception as e:
                    errors.append("Error processing file {}: {}".format(file.NAME, e))

            try:
                check_required_use(install.REQUIRED_USE, set(), self.valid_use)
            except Exception as e:
                errors.append("Error processing dir {}: {}".format(install.PATH, e))

            if install.WHITELIST is not None and type(install.WHITELIST) is not list:
                errors.append("WHITELIST {} must be a list".format(install.WHITELIST))
            elif install.WHITELIST is not None:
                for string in install.WHITELIST:
                    if type(string) is not str:
                        errors.append(
                            "{} in InstallDir WHITELIST is not a string".format(string)
                        )

            if install.BLACKLIST is not None and type(install.BLACKLIST) is not list:
                errors.append("BLACKLIST {} must be a list".format(install.BLACKLIST))
            elif install.BLACKLIST is not None:
                for string in install.BLACKLIST:
                    if type(string) is not str:
                        errors.append(
                            "{} in InstallDir BLACKLIST is not a string".format(string)
                        )

            if install.WHITELIST is not None and install.BLACKLIST is not None:
                errors.append("WHITELIST and BLACKLIST are mutually exclusive")

        global_use = get_global_use(self.REPO_PATH)
        metadata = get_package_metadata(self)

        for use in IUSE_STRIP:
            if global_use.get(use) is None and (
                metadata is None
                or metadata.use is None
                or metadata.use.get(use) is None
            ):
                valid = False
                # If the flag contains an underscore, it may be a USE_EXPAND flag
                if "_" in use:
                    for use_expand in get_use_expand(self.REPO_PATH):
                        length = len(use_expand) + 1  # Add one for underscore
                        if use.startswith(use_expand.lower()) and check_use_expand_flag(
                            self.REPO_PATH, use_expand, use[length:]
                        ):
                            valid = True
                            break

                if not valid:
                    errors.append(
                        'Use flag "{}" must be either a global use flag '
                        "or declared in metadata.yaml".format(use)
                    )

        for value in self.get_restrict(matchall=True):
            if value not in {"fetch", "mirror"}:
                errors.append(f"Unsupported restrict flag {value}")

        if not self.NAME or "FILLME" in self.NAME or len(self.NAME) == 0:
            errors.append("Please fill in the NAME field")
        if not self.DESC or "FILLME" in self.DESC or len(self.DESC) == 0:
            errors.append("Please fill in the DESC field")
        if not isinstance(self.HOMEPAGE, str) or "FILLME" in self.HOMEPAGE:
            errors.append("Please fill in the HOMEPAGE field")

        for license in use_reduce(self.LICENSE, flat=True, matchall=True):
            if license != "||" and not license_exists(self.REPO_PATH, license):
                errors.append(
                    "LICENSE {} does not exit! Please make sure that it named "
                    "correctly, or if it is a new License that it is added to "
                    "the licenses directory of the repository".format(license)
                )

        if not isinstance(self.PATCHES, str):
            errors.append("PATCHES must be a string")

        all_sources = self._get_sources(matchall=True)

        for install in self.INSTALL_DIRS:
            if isinstance(install, InstallDir):
                if len(all_sources) > 0 and install.S is None:
                    if len(all_sources) != 1:
                        raise Exception(
                            "InstallDir does not declare a source name but source "
                            "cannot be set automatically"
                        )
            else:
                raise TypeError(
                    "InstallDir {} should be of type InstallDir".format(install)
                )

        manifest = self.get_manifest()
        for source in self._get_sources(matchall=True):
            if manifest.get(source.name) is None:
                errors.append(f'Source "{source.name}" is not listed in the Manifest')

        if len(errors) > 0:
            raise Exception(
                "Pybuild {} contains the following errors:\n{}".format(
                    green(self.FILE), "\n".join(errors)
                )
            )


# Class used for typing pybuilds, allowing more flexibility with
# the implementations. Implementations of this class (e.g. Pybuild1)
# should derive it, but build file Mod classes should derive one of
# the implementations. This should be used as the type for any function that
# handles Pybuild objects.
#
# This provides a mechanism for modifying the Pybuild format, as we can
# make changes to this interface, and update the implementations to conform
# to it while keeping their file structure the same, performing conversions
# of the data inside the init function.
class FullPybuild(BasePybuild):
    """Interface describing the Pybuild Type"""

    __file__ = __file__
    TIER: str
    REPO_PATH: Optional[str]
    __pybuild__: str

    # Variables defined during the install/removal process
    A: List[Source]  # List of enabled sources
    D: str  # Destination directory where the mod is to be installed
    FILESDIR: str  # Path of the directory containing additional repository files
    ROOT: str  # Path of the installed directory of the mod
    T: str  # Path of temp directory
    UNFETCHED: List[Source]  # List of sources that need to be fetched
    USE: Set[str]  # Enabled use flags
    WORKDIR: str  # Path of the working directory

    # Note: declared as a string, but converted into a set during __init__
    IUSE = ""  # type: ignore
    KEYWORDS = ""

    def __init__(self):
        self.FILE = self.__class__.__pybuild__

        category = Path(self.FILE).resolve().parent.parent.name
        # Note: type will be fixed later by the loader and will become an FQAtom
        self.ATOM = Atom(  # type: ignore
            "{}/{}".format(category, os.path.basename(self.FILE)[: -len(".pybuild")])
        )

        self.REPO_PATH = str(Path(self.FILE).resolve().parent.parent.parent)
        repo_name_path = os.path.join(self.REPO_PATH, "profiles", "repo_name")
        if os.path.exists(repo_name_path):
            with open(repo_name_path, "r") as repo_file:
                self.REPO = repo_file.readlines()[0].rstrip()
            self.ATOM = FQAtom("{}::{}".format(self.ATOM, self.REPO))

        self.P = Atom(self.ATOM.P)
        self.PN = Atom(self.ATOM.PN)
        self.PV = self.ATOM.PV
        self.PF = Atom(self.ATOM.PF)
        self.PR = self.ATOM.PR or "r0"
        self.CATEGORY = self.ATOM.C
        self.R = self.ATOM.R
        self.CP = QualifiedAtom(self.ATOM.CP)
        self.CPN = QualifiedAtom(self.ATOM.CPN)
        self.PVR = self.ATOM.PVR

        self.IUSE_EFFECTIVE = set()

        if type(self.IUSE) is str:
            self.IUSE = set(self.IUSE.split())  # type: ignore # pylint: disable=no-member
            self.IUSE_EFFECTIVE |= set([use.lstrip("+") for use in self.IUSE])
        else:
            raise TypeError("IUSE must be a space-separated list of use flags")

        if type(self.KEYWORDS) is str:
            self.KEYWORDS = set(self.KEYWORDS.split())  # type: ignore # pylint: disable=no-member
        else:
            raise TypeError("KEYWORDS must be a space-separated list of keywords")

        if type(self.TIER) is int:
            self.TIER = str(self.TIER)
        elif type(self.TIER) is not str:
            raise TypeError("TIER must be a integer or string containing 0-9 or z")

        if type(self.TEXTURE_SIZES) is str:
            texture_sizes = use_reduce(self.TEXTURE_SIZES, matchall=True)
            self.IUSE_EFFECTIVE |= set(
                ["texture_size_{}".format(size) for size in texture_sizes]
            )
        else:
            raise TypeError(
                "TEXTURE_SIZES must be a string containing a space separated list of "
                "texture sizes"
            )

    def pkg_nofetch(self):
        """
        Function to give user instructions on how to fetch a mod
        which cannot be fetched automatically
        """

    def pkg_pretend(self):
        """
        May be used to carry out sanity checks early on in the install process

        Note that the default does nothing, and it will not even be executed unless defined.
        """

    def src_unpack(self):
        """Function used to unpack mod sources"""

    def src_prepare(self):
        """Function used to apply patches and configuration"""

    def src_install(self):
        """Function used to create the final install directory"""

    def pkg_prerm(self):
        """
        Function called immediately before mod removal

        Note that the default does nothing, and it will not even be executed unless defined.
        """

    def pkg_postinst(self):
        """
        Function called immediately after mod installation

        Note that the default does nothing, and it will not even be executed unless defined.
        """

    @lru_cache()
    def get_installed_env(self):
        """Returns a dictionary containing installed object values"""

    @staticmethod
    def execute(
        command: str, pipe_output: bool = False, pipe_error: bool = False
    ) -> Optional[str]:
        """Function pybuild files can use to execute native commands"""

    def _to_cache(self) -> Dict:
        from pybuild import Pybuild1

        cache = {}
        for key in [
            "RDEPEND",
            "DEPEND",
            "SRC_URI",
            "REQUIRED_USE",
            "RESTRICT",
            "PROPERTIES",
            "IUSE_EFFECTIVE",
            "IUSE",
            "TEXTURE_SIZES",
            "DESC",
            "NAME",
            "HOMEPAGE",
            "LICENSE",
            "KEYWORDS",
            "REBUILD_FILES",
            "TIER",
            "FILE",
            "REPO",
            "DATA_OVERRIDES",
            "S",
            "PATCHES",
        ]:
            cache[key] = getattr(self, key)

        cache["INSTALL_DIRS"] = [idir._to_cache() for idir in self.INSTALL_DIRS]
        phase_functions = [
            "src_unpack",
            "src_install",
            "src_prepare",
            "pkg_nofetch",
            "pkg_pretend",
            "pkg_postinst",
            "pkg_prerm",
        ]
        cache["FUNCTIONS"] = [
            func
            for func in phase_functions
            if hasattr(self.__class__, func)
            and getattr(self.__class__, func) != getattr(Pybuild1, func)
        ]
        return cache


class InstalledPybuild(Pybuild):
    """Interface describing the type of installed Pybuilds"""

    INSTALLED_USE: Set[str] = set()
    INSTALLED_REBUILD_FILES: Optional[Manifest] = None

    def __init__(
        self, atom: FQAtom, cache: Optional[Dict] = None, *, FILE: str, **kwargs
    ):
        super().__init__(atom, cache=cache, FILE=FILE, **kwargs)
        self.INSTALLED_USE = set(self.INSTALLED_USE)
        self.INSTALLED = True
        if self.INSTALLED_REBUILD_FILES:
            self.INSTALLED_REBUILD_FILES = Manifest.from_json(
                self.INSTALLED_REBUILD_FILES
            )

    def get_use(self):
        return self.INSTALLED_USE

    @lru_cache()
    def get_installed_env(self):
        """Returns a dictionary containing installed object values"""
        return get_installed_env(self)


class FullInstalledPybuild(InstalledPybuild, FullPybuild):
    """Interface describing the type of installed Pybuilds"""

    INSTALLED_USE: Set[str]

    def _to_cache(self) -> Dict:
        cache = FullPybuild._to_cache(self)
        cache["INSTALLED_USE"] = self.INSTALLED_USE
        cache["INSTALLED_REBUILD_FILES"] = None
        if self.INSTALLED_REBUILD_FILES:
            cache["INSTALLED_REBUILD_FILES"] = self.INSTALLED_REBUILD_FILES.to_json()
        return cache


def parse_arrow(sourcelist: Iterable[str]) -> List[Source]:
    """
    Turns a list of urls using arrow notation into a list of
    Source objects
    """
    result: List[Source] = []
    arrow = False
    for value in sourcelist:
        if arrow:
            result[-1] = Source(result[-1].url, value)
            arrow = False
        elif value == "->":
            arrow = True
        else:
            url = urllib.parse.urlparse(value)
            result.append(Source(value, os.path.basename(url.path)))
    return result


def manifest_path(file):
    return os.path.join(os.path.dirname(file), "Manifest")


# Loads the manifest for the given file, i.e. the Manifest file in the same directory
#    and turns it into a map of filenames to (shasum, size) pairs
def get_manifest(file):
    m_path = manifest_path(file)

    return Manifest(m_path)


def get_installed_env(pkg: BasePybuild):
    if not pkg.INSTALLED:
        raise Exception("Trying to get environment for mod that is not installed")

    path = os.path.join(os.path.dirname(pkg.FILE), "environment.xz")
    if os.path.exists(path):
        environment = lzma.LZMAFile(path)
        try:
            return json.load(environment)
        except EOFError as e:
            raise RuntimeError(f"Failed to read {path}") from e

    return {}
