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
Methods for dealing with systems of particles, such as center of mass and angular momentum.

Methods here are not specific with units - as long as arguments are provided in consistent units, then
the calculated result will be correct.
"""

from typing import Optional

import numpy as np

from .matrix import zero_matrix
from .typing import Matrix3x3, ScalarArray, ScalarArrayLike, Vector3, Vector3Array, Vector3ArrayLike, Vector3Like
from .vector import left_vector_triple_product_matrix, sqr_magnitude, zero_vector


def center_of_mass(*, masses: ScalarArrayLike, positions: Vector3ArrayLike) -> Vector3:
    r"""
    Calculate the center of mass :math:`R` of a collection of particles, defined as the mass weighted average position:

    .. math:: R = \frac{\sum_i m_i r_i}{\sum_i m_i}

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`r_i` of each particle.
    :return: Center of mass of the particles, in the same units as positions was provided in.
    """
    positions: Vector3Array = np.asfarray(positions)
    masses: ScalarArray = np.asfarray(masses)

    count = len(positions)
    if len(masses) != count:
        raise ValueError(f"Mismatch between number of positions ({len(positions)}) "
                         f"and number of masses ({len(masses)})")

    total_center = zero_vector()
    for i in range(0, count):
        total_center += masses[i] * positions[i]
    return total_center / sum(masses)  # type: ignore


def center_of_mass_velocity(*, masses: ScalarArrayLike, velocities: Vector3ArrayLike) -> Vector3:
    r"""
    Calculate the velocity :math:`V_R` of the center of mass of a collection of particles, defined as the mass weighted
    average velocity:

    .. math:: V_R = \frac{\sum_i m_i v_i}{\sum_i v_i}

    :param masses: List of masses :math:`m_i` of each particle.
    :param velocities: List of velocities :math:`v_i` of each particle.
    :return: Velocity of the center of mass of the particles, in units of [distance] / [time].
    """
    # Reuse center of mass calculation, as its the same with positions exchanged for velocities
    return center_of_mass(masses=masses, positions=velocities)


def center_of_mass_acceleration(*, masses: ScalarArrayLike, accelerations: Vector3ArrayLike) -> Vector3:
    r"""
    Calculate the acceleration :math:`A_R` of the center of mass of a collection of particles, defined as the mass
    weighted average acceleration:

    .. math:: A_R = \frac{\sum_i m_i a_i}{\sum_i a_i}

    :param masses: List of masses :math:`m_i` of each particle.
    :param accelerations: List of accelerations :math:`a_i` of each particle.
    :return: Acceleration of the center of mass of the particles, in units of [distance] / [time] ** 2.
    """
    # Reuse center of mass calculation, as its the same with positions exchanged for accelerations
    return center_of_mass(masses=masses, positions=accelerations)


def spin_angular_momentum(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array) -> Vector3:
    r"""
    Calculate the spin angular momentum :math:`L` of a collection of particles about their center of mass, defined as:

    .. math:: L = \sum_i m_i r_i \times v_i

    where :math:`r_i` and :math:`v_i` are the particles' position and velocity relative to the center of mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :return: Spin angular momentum :math:`L` in units of [mass] * [distance] squared / [time].
    """
    com = center_of_mass(masses=masses, positions=positions)
    com_velocity = center_of_mass_velocity(masses=masses, velocities=velocities)
    angular_momentum = np.array([0.0, 0.0, 0.0], dtype=float)
    for i in range(0, len(masses)):
        angular_momentum += masses[i] * np.cross(positions[i] - com, velocities[i] - com_velocity)
    return angular_momentum


def orbital_angular_momentum(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array,
                             origin: Optional[Vector3Like] = None) -> Vector3:
    r"""
    Calculate the orbital angular momentum :math:`L` of a collection of particles about an origin :math:`c`, defined as:

    .. math:: L = M (R - c) \times V

    where :math:`M`, :math:`R` and :math:`V` are the total mass, center of mass and the velocity of the center of mass
    respectively.

    The origin defaults to the origin (0, 0, 0).

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :param origin: Origin about where to calculate the orbital angular momentum.
    :return: Orbital angular momentum :math:`L` in units of [mass] * [distance] squared / [time].
    """
    if origin is None:
        origin = zero_vector()
    else:
        origin = np.asfarray(origin)
    com = center_of_mass(masses=masses, positions=positions)
    com_velocity = center_of_mass_velocity(masses=masses, velocities=velocities)
    total_mass = np.sum(np.asfarray(masses))
    return total_mass * np.cross(com - origin, com_velocity)  # type: ignore


def moment_of_inertia_tensor(*, masses: ScalarArray, positions: Vector3Array,
                             origin: Optional[Vector3Like] = None) -> Matrix3x3:
    r"""
    Calculate the moment of inertia tensor :math:`I` of a collection of particles with respect to an origin :math:`c`.
    This matrix fulfills the identity:

    .. math:: I v = \sum_i m_i r_i \times (v \times r_i)

    for all vectors :math:`v`. Here, :math:`r_i` is the position of the i-th particle relative to the center of mass.

    By default, the origin is taken to be the center of mass.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param origin: Optional origin to calculate the moment of inertia around. Defaults to the center of mass.
    :return: Moment of inertia tensor :math:`I` with respect to the center of mass, in units of [mass] * [distance]
             squared
    """
    if origin is None:
        origin = center_of_mass(masses=masses, positions=positions)
    else:
        origin = np.asfarray(origin)
    tensor = zero_matrix()
    for i in range(0, len(masses)):
        tensor -= masses[i] * left_vector_triple_product_matrix(positions[i] - origin, positions[i] - origin)
    return tensor


def angular_velocity(*, masses: ScalarArray, positions: Vector3Array, velocities: Vector3Array) -> Vector3:
    r"""
    Calculate the angular velocity :math:`\omega` of a collection of particles with respect to their center of mass by
    calculating the angular momentum about the center of mass, and inverting the inertia tensor to obtain
    :math:`\omega`:

    .. math:: \omega = I^{-1} L

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param velocities: List of velocities :math:`V_i` of each particle.
    :return: Angular velocity :math:`\omega` in units of radians / [time].
    """
    L = spin_angular_momentum(masses=masses, positions=positions, velocities=velocities)
    inertia = moment_of_inertia_tensor(masses=masses, positions=positions)
    return np.matmul(np.linalg.inv(inertia), L)  # type: ignore


def distribute_angular_velocity(*, masses: Optional[ScalarArrayLike] = None, positions: Vector3ArrayLike,
                                angular_velocity: Vector3Like, origin: Optional[Vector3Like] = None) -> Vector3Array:
    r"""
    Calculate the velocities that should be assigned to each particle in a collection of particles to correspond to a
    given angular velocity :math:`\omega` about an origin :math:`c`, defined by:

    .. math:: v_i = \omega \times (r_i - c)

    The origin :math:`c` defaults to the center of mass of the particles.

    :param masses: List of masses :math:`m_i` of each particle.
    :param positions: List of positions :math:`R_i` of each particle.
    :param angular_velocity: Angular velocity :math:`\omega` to assign to the system.
    :return: Velocities :math:`V_i` in units of [distance] / [time].
    """
    if origin is None:
        if masses is None:
            raise ValueError("Either an origin or masses must be provided.")
        origin = center_of_mass(masses=masses, positions=positions)
    else:
        origin = np.asfarray(origin)
    velocities = [np.cross(angular_velocity, position - origin) for position in positions]  # type: ignore[operator]
    return np.asfarray(velocities)  # type: ignore [no-any-return]


def kinetic_energy(*, masses: ScalarArrayLike, velocities: Vector3ArrayLike) -> float:
    r"""
    Calculate the total kinetic energy of a set of particles, given by

    .. math:: K = \frac{1}{2} \sum_i m_i v_i^2

    :param masses: List of masses :math:`m_i` of each particle.
    :param velocities: List of velocities :math:`v_i` of each particle.
    :return: Kinetic energy :math:`K` in units of [distance] / [time].
    """
    return sum(0.5 * mass * sqr_magnitude(velocity) for mass, velocity in zip(masses, velocities))
