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
#
# Originally part of the narupa-openmm package.
# Copyright (c) Intangible Realities Lab, University Of Bristol. All rights reserved.
# Modified under the terms of the GPL.

"""
Conversion functions between OpenMM objects and Narupa objects.
"""
import itertools
from typing import Iterable, Optional, Sequence, Type, TypeVar, Union

import numpy as np
from infinite_sets import InfiniteSet
from narupa.trajectory.frame_data import FrameData
from simtk.openmm.app import Element, Simulation, Topology
from simtk.openmm.openmm import Context, State

from narupatools.core.units import UnitsNarupa
from narupatools.frame import BondCount, BondPairs, BoxVectors, ChainCount, ChainNames, ParticleCount, \
    ParticleElements, ParticleForces, ParticleNames, ParticlePositions, ParticleResidues, ParticleVelocities, \
    PotentialEnergy, ResidueChains, ResidueCount, ResidueIds, ResidueNames
from narupatools.frame.converter import FrameConverter
from narupatools.frame.utils import atomic_numbers_to_symbols
from narupatools.openmm.units import UnitsOpenMM

DEFAULT_OPENMM_STATE_PROPERTIES = frozenset((ParticlePositions.key, BoxVectors.key))

DEFAULT_OPENMM_TOPOLOGY_PROPERTIES = frozenset((
    ResidueNames.key, ResidueChains.key, ResidueCount.key, ParticleCount.key, ChainNames.key, ChainCount.key,
    ParticleNames.key, ParticleElements.key, ParticleResidues.key, BondPairs.key, BondCount.key, BoxVectors.key))

DEFAULT_OPENMM_SIMULATION_PROPERTIES = frozenset(
    DEFAULT_OPENMM_TOPOLOGY_PROPERTIES | DEFAULT_OPENMM_TOPOLOGY_PROPERTIES)

OpenMMToNarupa = UnitsOpenMM >> UnitsNarupa

_TType = TypeVar("_TType")


class OpenMMConverter(FrameConverter):
    """Frame converter for the OpenMM package."""

    @classmethod
    def convert_to_frame(cls,  # noqa:D102
                         object: _TType,
                         *,
                         fields: InfiniteSet[str],
                         existing: Optional[FrameData]) -> FrameData:
        if isinstance(object, Context):
            return openmm_context_to_frame(object, fields=fields, frame=existing)
        if isinstance(object, State):
            return openmm_state_to_frame(object, fields=fields, frame=existing)
        if isinstance(object, Topology):
            return openmm_topology_to_frame(object, fields=fields, frame=existing)
        if isinstance(object, Simulation):
            return openmm_simulation_to_frame(object, fields=fields, frame=existing)
        raise NotImplementedError()

    @classmethod
    def convert_from_frame(cls,  # noqa:D102
                           frame: FrameData,
                           type: Union[Type[_TType], _TType],
                           *,
                           fields: InfiniteSet[str]) -> _TType:
        if type == Topology:
            return frame_to_openmm_topology(frame)  # type: ignore[return-value]
        raise NotImplementedError()


def frame_to_openmm_topology(frame: FrameData) -> Topology:
    """
    Convert a Narupa FrameData to an OpenMM topology.

    :param frame: FrameData to convert.
    :return: OpenMM topology populated from the provided FrameData.
    """

    topology = Topology()

    elements = ParticleElements.get(frame)
    residues = ParticleResidues.get_with_default(frame, itertools.repeat(0))
    resnames = ResidueNames.get_with_default(frame, itertools.repeat("Xxx"))
    names = ParticleNames.get_with_default(frame, atomic_numbers_to_symbols(elements))
    resids = ResidueIds.get_with_default(frame, itertools.repeat(None))
    segs = ResidueChains.get_with_default(frame, itertools.repeat(0))
    segnames = ChainNames.get_with_default(frame, itertools.repeat(None))
    segcount = ChainCount.get_with_default(frame, 1)
    rescount = ResidueCount.get_with_default(frame, 1)
    bonds: Iterable[Sequence[int]] = BondPairs.get_with_default(frame, [])
    box = BoxVectors.get_with_default(frame, None)

    omm_segs = []
    for segname, _ in zip(segnames, range(segcount)):
        omm_segs.append(topology.addChain(id=segname))

    omm_res = []
    for resname, resid, seg, _ in zip(resnames, resids, segs, range(rescount)):
        omm_res.append(topology.addResidue(name=resname, id=resid, chain=omm_segs[seg]))

    omm_atoms = []
    for residue, name, element in zip(residues, names, elements):
        omm_atoms.append(topology.addAtom(name=name,
                                          element=Element.getByAtomicNumber(element),
                                          residue=omm_res[residue]))

    for bond in bonds:
        topology.addBond(atom1=omm_atoms[bond[0]], atom2=omm_atoms[bond[1]])

    if box is not None:
        topology.setPeriodicBoxVectors(box)

    return topology


def openmm_simulation_to_frame(simulation: Simulation, *,
                               fields: InfiniteSet[str] = DEFAULT_OPENMM_SIMULATION_PROPERTIES,
                               frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM simulation to a Narupa FrameData.

    :param simulation: OpenMM simulation to convert.
    :param properties: Properties to read from frame.
    :param frame: Prexisting FrameData to populate.
    :return: FrameData with requested fields populated from an OpenMM simulation.
    """

    if frame is None:
        frame = FrameData()

    openmm_topology_to_frame(simulation.topology, fields=fields, frame=frame)
    openmm_context_to_frame(simulation.context, fields=fields, frame=frame)

    return frame


def openmm_context_to_frame(context: Context, *, fields: InfiniteSet[str] = DEFAULT_OPENMM_STATE_PROPERTIES,
                            frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM context to a Narupa FrameData.

    By converting the context instead of the state, a state can be generated which only has the data that is asked for
    in properties.

    :param context: OpenMM context to convert.
    :param properties: Properties to read from frame.
    :param frame: Prexisting FrameData to populate.
    :return: FrameData with requested fields populated from an OpenMM context.
    """

    if frame is None:
        frame = FrameData()

    needPositions = ParticlePositions.key in fields
    needForces = ParticleForces.key in fields
    needVelocities = ParticleVelocities.key in fields
    needEnergy = PotentialEnergy.key in fields

    state = context.getState(getPositions=needPositions, getForces=needForces,
                             getEnergy=needEnergy, getVelocities=needVelocities)

    return openmm_state_to_frame(state, fields=fields, frame=frame)


def openmm_state_to_frame(state: State, *, fields: InfiniteSet[str] = DEFAULT_OPENMM_STATE_PROPERTIES,
                          frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM state object to a Narupa FrameData

    :param state: OpenMM state to convert.
    :param properties: A list of properties to include.
    :param frame_data: Prexisting FrameData to populate.
    :return: FrameData populated with the requested properties that could be obtained from the state object.
    """
    if frame is None:
        frame = FrameData()

    if ParticlePositions.key in fields:
        ParticlePositions.set(frame, state.getPositions(asNumpy=True)._value * OpenMMToNarupa.length)
    if ParticleForces.key in fields:
        ParticleForces.set(frame, state.getForces(asNumpy=True)._value * OpenMMToNarupa.force)
    if ParticleVelocities.key in fields:
        ParticleVelocities.set(frame, state.getVelocities(asNumpy=True)._value * OpenMMToNarupa.velocity)

    if PotentialEnergy.key in fields:
        PotentialEnergy.set(frame, state.getPotentialEnergy()._value * OpenMMToNarupa.energy)

    if BoxVectors.key in fields:
        BoxVectors.set(frame, np.array(state.getPeriodicBoxVectors()._value, dtype=float) * OpenMMToNarupa.length)
    return frame


def openmm_topology_to_frame(topology: Topology, *, fields: InfiniteSet[str] = DEFAULT_OPENMM_TOPOLOGY_PROPERTIES,
                             frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an OpenMM topology object to a Narupa FrameData

    :param topology: OpenMM topology to convert.
    :param properties: List of properties to include.
    :param frame_data: Prexisting FrameData to populate.
    :return: FrameData populated with the requested properties that could be obtained from the topology object.
    """
    if frame is None:
        frame = FrameData()

    if ParticleCount.key in fields:
        ParticleCount.set(frame, topology.getNumAtoms())

    _get_openmm_topology_residue_info(topology, fields, frame)

    if ChainNames.key in fields:
        ChainNames.set(frame, [chain.id for chain in topology.chains()])
    if ChainCount.key in fields:
        ChainCount.set(frame, topology.getNumChains())

    _get_openmm_topology_atom_info(topology, fields, frame)

    _get_openmm_topology_bonds(topology, fields, frame)

    if BoxVectors.key in fields:
        box = topology.getPeriodicBoxVectors()
        if box is not None:
            BoxVectors.set(frame, np.array(box._value, dtype=float) * OpenMMToNarupa.length)

    return frame


def _get_openmm_topology_bonds(topology: Topology, fields: InfiniteSet[str], frame: FrameData) -> None:
    if BondPairs.key in fields:
        bonds = []
        for bond in topology.bonds():
            bonds.append((bond[0].index, bond[1].index))
        BondPairs.set(frame, bonds)
    if BondCount.key in fields:
        BondCount.set(frame, topology.getNumBonds())


def _get_openmm_topology_atom_info(topology: Topology, fields: InfiniteSet[str], frame: FrameData) -> None:
    if ParticleNames.key in fields or ParticleElements.key in fields or ParticleResidues.key in fields:

        n = topology.getNumAtoms()
        atom_names = np.empty(n, dtype=object)
        elements = np.empty(n, dtype=int)
        residue_indices = np.empty(n, dtype=int)

        for i, atom in enumerate(topology.atoms()):
            atom_names[i] = atom.name
            elements[i] = atom.element.atomic_number
            residue_indices[i] = atom.residue.index

        if ParticleNames.key in fields:
            ParticleNames.set(frame, atom_names)
        if ParticleElements.key in fields:
            ParticleElements.set(frame, elements)
        if ParticleResidues.key in fields:
            ParticleResidues.set(frame, residue_indices)


def _get_openmm_topology_residue_info(topology: Topology, fields: InfiniteSet[str], frame: FrameData) -> None:
    if ResidueNames.key in fields:
        ResidueNames.set(frame, [residue.name for residue in topology.residues()])
    if ResidueIds.key in fields:
        ResidueIds.set(frame, [residue.id for residue in topology.residues()])
    if ResidueChains.key in fields:
        ResidueChains.set(frame, [residue.chain.index for residue in topology.residues()])
    if ResidueCount.key in fields:
        ResidueCount.set(frame, topology.getNumResidues())
