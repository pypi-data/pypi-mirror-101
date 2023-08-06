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
# Originally part of the narupa-ase package.
# Copyright (c) Intangible Realities Lab, University Of Bristol. All rights reserved.
# Modified under the terms of the GPL.

"""
Conversion functions for converting ASE objects to Narupa objects.
"""

import contextlib
from contextlib import suppress
from typing import Any, Dict, Optional, Type, TypeVar, Union

from ase.atoms import Atoms
from ase.calculators.calculator import PropertyNotImplementedError
from infinite_sets import InfiniteSet, everything
from narupa.trajectory.frame_data import FrameData

from narupatools.ase.calculators.constant_calculator import ConstantCalculator
from narupatools.ase.units import UnitsASE
from narupatools.core.units import UnitsNarupa
from narupatools.frame import BoxVectors, KineticEnergy, ParticleCharges, ParticleCount, ParticleElements, \
    ParticleForces, ParticleMasses, ParticleNames, ParticlePositions, ParticleResidues, ParticleVelocities, \
    PotentialEnergy, ResidueCount, ResidueNames
from narupatools.frame.converter import FrameConverter
from narupatools.mdanalysis.units import UnitsMDAnalysis

ASEToNarupa = UnitsASE >> UnitsNarupa
NarupaToASE = UnitsNarupa >> UnitsASE

MDAnalysisToASE = UnitsMDAnalysis >> UnitsASE

ASE_PROPERTIES = frozenset((
    ParticlePositions.key, ParticleElements.key, BoxVectors.key, ParticleCount.key, ResidueNames.key, ParticleNames.key,
    ParticleResidues.key, ResidueCount.key))

ALL_PROPERTIES = everything()

_TType = TypeVar("_TType")


class ASEConverter(FrameConverter):
    """Converters for the ASE package."""

    @classmethod
    def convert_to_frame(cls,  # noqa: D102
                         object: _TType,
                         *,
                         fields: InfiniteSet[str],
                         existing: Optional[FrameData]) -> FrameData:
        if isinstance(object, Atoms):
            return ase_atoms_to_frame(object, fields=fields)
        raise NotImplementedError()

    @classmethod
    def convert_from_frame(cls,  # noqa: D102
                           frame: FrameData,
                           type: Union[Type[_TType], _TType],
                           *,
                           fields: InfiniteSet[str]) -> _TType:
        if type == Atoms:
            return frame_to_ase_atoms(frame=frame, fields=fields)  # type: ignore[return-value]
        raise NotImplementedError()


def frame_to_ase_atoms(frame: FrameData, *, fields: InfiniteSet[str] = everything()) -> Atoms:
    """
    Convert a Narupa FrameData to an ASE atoms object.

    :param frame: Narupa FrameData to convert.
    :param fields: Set of fields to convert.
    :return: An ASE atoms objects with masses, velocities, elements, unit cell and charges read from the frame.
    """
    kwargs: Dict[str, Any] = {}
    if ParticlePositions.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['positions'] = ParticlePositions.get(frame) * NarupaToASE.length
    if ParticleMasses.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['masses'] = ParticleMasses.get(frame) * NarupaToASE.mass
    if ParticleVelocities.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['velocities'] = ParticleVelocities.get(frame) * NarupaToASE.velocity
    if ParticleElements.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['symbols'] = ParticleElements.get(frame)
    if BoxVectors.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['cell'] = BoxVectors.get(frame) * NarupaToASE.length
    if ParticleCharges.key in fields:
        with contextlib.suppress(KeyError):
            kwargs['charges'] = ParticleCharges.get(frame) * NarupaToASE.charge

    calc_kwargs: Dict[str, Any] = {}

    if ParticleForces.key in fields:
        with contextlib.suppress(KeyError):
            calc_kwargs['forces'] = ParticleForces.get(frame) * NarupaToASE.force
    if PotentialEnergy.key in fields:
        with contextlib.suppress(KeyError):
            calc_kwargs['energy'] = PotentialEnergy.get(frame) * NarupaToASE.energy
    if ParticleCharges.key in fields:
        with contextlib.suppress(KeyError):
            calc_kwargs['charges'] = ParticleCharges.get(frame) * NarupaToASE.charge

    calculator = ConstantCalculator(**calc_kwargs)

    atoms = Atoms(**kwargs)
    atoms.set_calculator(calculator)
    return atoms


def ase_atoms_to_frame(atoms: Atoms, *, fields: InfiniteSet[str] = ASE_PROPERTIES,
                       frame: Optional[FrameData] = None) -> FrameData:
    """
    Convert an ASE Atoms object to a Narupa FrameData.

    :param atoms: ASE Atoms object to convert.
    :param fields: A collection of keys that should be added to the frame if available.
    :param frame: An optional preexisting FrameData to populate.
    :return: A FrameData populated with information available in the ASE atoms object whose keys are present in
        the properties parameter.
    """
    if frame is None:
        frame = FrameData()

    _add_ase_atoms_particles_to_frame(atoms, fields, frame)
    _add_ase_atoms_residues_to_frame(atoms, fields, frame)
    _add_ase_atoms_calculated_properties_to_frame(atoms, fields, frame)

    if BoxVectors.key in fields:
        # todo: is this copy necessary?
        BoxVectors.set(frame, atoms.get_cell().copy() * ASEToNarupa.length)

    if KineticEnergy.key in fields:
        KineticEnergy.set(frame, atoms.get_kinetic_energy() * ASEToNarupa.energy)

    return frame


def _add_ase_atoms_particles_to_frame(atoms: Atoms, fields: InfiniteSet[str], frame: FrameData) -> None:
    if ParticlePositions.key in fields:
        ParticlePositions.set(frame, atoms.get_positions() * ASEToNarupa.length)

    if ParticleCount.key in fields:
        ParticleCount.set(frame, len(atoms))

    if ParticleElements.key in fields:
        elements = []
        for atom in atoms:
            elements.append(atom.number)

        ParticleElements.set(frame, elements)

    if ParticleMasses.key in fields:
        ParticleMasses.set(frame, atoms.get_masses())

    if ParticleVelocities.key in fields:
        ParticleVelocities.set(frame, atoms.get_velocities() * ASEToNarupa.velocity)

    if ParticleNames.key in fields and 'atomtypes' in atoms.arrays:
        ParticleNames.set(frame, atoms.arrays['atomtypes'])


def _add_ase_atoms_calculated_properties_to_frame(atoms: Atoms, fields: InfiniteSet[str], frame: FrameData) -> None:
    if ParticleCharges.key in fields:
        calc_charges = False
        if atoms.calc is not None:
            with contextlib.suppress(PropertyNotImplementedError):
                ParticleCharges.set(frame, atoms.get_charges())
                calc_charges = True
        if not calc_charges:
            ParticleCharges.set(frame, atoms.get_initial_charges())

    if ParticleForces.key in fields and atoms.calc is not None:
        with contextlib.suppress(PropertyNotImplementedError):
            ParticleForces.set(frame, atoms.get_forces() * ASEToNarupa.force)

    if PotentialEnergy.key in fields and atoms.calc is not None:
        with suppress(PropertyNotImplementedError):
            PotentialEnergy.set(frame, atoms.get_potential_energy() * ASEToNarupa.energy)


def _add_ase_atoms_residues_to_frame(atoms: Atoms, fields: InfiniteSet[str], frame: FrameData) -> None:
    if (ResidueNames.key in fields or ResidueCount.key in fields or ParticleResidues.key in fields) \
            and 'residuenumbers' in atoms.arrays:
        segid_to_index: Dict[Any, int] = {}
        res_to_first_particle_index = []
        index = 0
        for atom_index, segid in enumerate(atoms.arrays['residuenumbers']):
            if segid not in segid_to_index:
                segid_to_index[segid] = index
                res_to_first_particle_index.append(atom_index)
                index += 1

        if ParticleResidues.key in fields:
            ParticleResidues.set(frame, [segid_to_index[segid] for segid in atoms.arrays['residuenumbers']])

        if ResidueNames.key in fields and 'residuenames' in atoms.arrays:
            ResidueNames.set(frame, [str(atoms.arrays['residuenames'][atom_index]).strip() for atom_index in
                                     res_to_first_particle_index])

        if ResidueCount.key in fields and 'residuenames' in atoms.arrays:
            ResidueCount.set(frame, len(res_to_first_particle_index))
