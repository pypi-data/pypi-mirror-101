# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from collections import defaultdict
from typing import Dict, List, Set

from portmod.atom import QualifiedAtom
from portmod.functools import prefix_aware_cache
from portmod.globals import env
from portmod.parsers.list import CommentedLine, read_list
from portmod.repo.profiles import profile_parents


@prefix_aware_cache
def get_masked() -> Dict[str, Dict[QualifiedAtom, List[str]]]:
    """
    Returns details about masked packages

    returns:
        A mapping of package Category-Package-Name strings to their comment and atom
        (noting that the atom can contain version specifiers, and the mapping is
        provided to facilitate efficient checks).
    """
    masked: Dict[str, Dict[QualifiedAtom, List[str]]] = defaultdict(dict)

    for path in (
        profile_parents()
        + [os.path.join(repo.location, "profiles") for repo in env.prefix().REPOS]
        + [env.prefix().PORTMOD_CONFIG_DIR]
    ):
        if os.path.exists(os.path.join(path, "package.mask")):
            for line in read_list(os.path.join(path, "package.mask")):
                atom = QualifiedAtom(line)
                if isinstance(line, CommentedLine):
                    masked[atom.CPN][atom] = line.comment
                else:
                    masked[atom.CPN][atom] = []
    return masked


@prefix_aware_cache
def get_unmasked() -> Dict[str, Set[QualifiedAtom]]:
    """
    Returns a dictionary mapping Category-Package-Name strings to
    the precice atom which is unmasked
    """
    unmasked: Dict[str, Set[QualifiedAtom]] = defaultdict(set)

    path = env.prefix().PORTMOD_CONFIG_DIR
    if os.path.exists(os.path.join(path, "package.unmask")):
        for line in read_list(os.path.join(path, "package.unmask")):
            atom = QualifiedAtom(line)
            unmasked[atom.CPN].add(atom)
    return unmasked
