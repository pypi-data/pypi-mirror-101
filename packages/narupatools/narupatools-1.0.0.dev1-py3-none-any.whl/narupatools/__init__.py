# This file is part of narupatools (https://gitlab.com/alexjbinnie/narupatools).
# Copyright (c) University of Bristol. All rights reserved.
#
# narupatools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# narupatools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with narupatools.  If not, see <http://www.gnu.org/licenses/>.

"""Narupatools is a package containing utilities to make working with Narupa easier."""
import importlib

import narupatools.ase  # noqa: F401
import narupatools.mdanalysis  # noqa: F401
import narupatools.mdtraj  # noqa: F401
import narupatools.openmm  # noqa: F401

if importlib.util.find_spec("lammps") is not None:
    import narupatools.lammps  # noqa: F401

from ._version import __version__  # noqa

__author__ = 'Alex Jamieson-Binnie'
