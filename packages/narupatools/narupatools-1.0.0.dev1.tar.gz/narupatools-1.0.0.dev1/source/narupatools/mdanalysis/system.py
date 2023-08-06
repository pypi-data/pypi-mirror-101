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

"""Wrapper around an MDAnalysis universe."""

from MDAnalysis import Universe
from infinite_sets import InfiniteSet
from narupa.trajectory import FrameData

from narupatools.frame.frame_source import FrameSource
from narupatools.mdanalysis import mdanalysis_universe_to_frame


class MDAnalysisSystem(FrameSource):
    """Wrapper around an MDAnalysis universe to allow it to be broadcast on a Narupa session."""

    def __init__(self, universe: Universe):
        self._universe = universe

    def get_frame(self, fields: InfiniteSet[str]) -> FrameData:  # noqa: D102
        return mdanalysis_universe_to_frame(self._universe)
