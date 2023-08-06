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
Describes the base class for anything that supports get_frame.
"""

from abc import ABCMeta, abstractmethod

from infinite_sets import InfiniteSet
from narupa.trajectory import FrameData


class FrameSource(metaclass=ABCMeta):
    """Base class for object which can create a FrameData."""

    @abstractmethod
    def get_frame(self, fields: InfiniteSet[str]) -> FrameData:
        """
        Create a FrameData representation, with the given fields present if available.
        :param fields: Collection of fields that should be added to FrameData if available.
        """
        pass
