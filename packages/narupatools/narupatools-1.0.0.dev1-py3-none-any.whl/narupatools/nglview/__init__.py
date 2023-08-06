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

"""
Code for interfacing with NGLView.
"""
import importlib

has_ngl = importlib.util.find_spec("nglview") is not None

if not has_ngl:
    raise ImportError("narupatools.nglview requires nglview to be installed.")

from .show import show_ase, show_narupa  # noqa: E401

__all__ = ["show_ase", "show_narupa"]
