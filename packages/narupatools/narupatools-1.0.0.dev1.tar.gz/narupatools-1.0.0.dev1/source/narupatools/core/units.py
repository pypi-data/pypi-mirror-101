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

"""Core unit conversion system."""
import contextlib
import math
from typing import Any, Generic, Optional, TypeVar, Union, overload

TType = TypeVar('TType')


class Unit:
    """Floating point number that can be considered a 'Unit', and used with the >> conversion type."""

    def __init__(self, value: 'Union[float, int, Unit]'):
        self.value: float = 0.0
        if isinstance(value, Unit):
            self.value = value.value
        else:
            self.value = float(value)

    @overload
    def __mul__(self, other: 'Unit') -> 'Unit':
        ...

    @overload
    def __mul__(self, other: 'Prefix') -> 'UnfinishedUnitOrQuantity':
        ...

    def __mul__(self, other: Any) -> 'Union[Unit, UnfinishedUnitOrQuantity[Unit]]':
        if isinstance(other, Unit):
            return Unit(self.value * other.value)
        if isinstance(other, Prefix):
            return UnfinishedUnitOrQuantity(other, self)
        return NotImplemented

    def __truediv__(self, other: Any) -> 'Unit':
        if isinstance(other, Unit):
            return Unit(self.value / other.value)
        return NotImplemented

    def __rmul__(self, other: TType) -> TType:
        if isinstance(other, (float, int)):
            return other * self.value  # type: ignore[return-value]
        return NotImplemented

    def __rtruediv__(self, other: Any) -> float:
        if isinstance(other, (float, int)):
            return other / self.value
        return NotImplemented

    def __rshift__(self, other: Any) -> float:
        if isinstance(other, Unit):
            return other.value / self.value
        return NotImplemented

    def __pow__(self, power: Any, modulo: Optional[Any] = None) -> 'Unit':
        return Unit(self.value ** power)

    def __repr__(self) -> str:
        return f"Unit({self.value})"

    def __array_ufunc__(self, ufunc: Any, method: Any, *inputs: Any, **kwargs: Any) -> Any:
        # Handle numpy operations by converting to float. Required to prevent numpy arrays from losing dtypes.
        input_list = list(inputs)
        for i in range(len(input_list)):
            if input_list[i] is self:
                input_list[i] = self.value
        return getattr(ufunc, method)(*input_list, **kwargs)


class Prefix:
    """Floating point number that can be considered an SI prefix, and hence multiply a unit."""

    def __init__(self, value: float):
        self.value = value

    @overload
    def __mul__(self, other: Unit) -> Unit:
        ...

    @overload
    def __mul__(self, other: 'Prefix') -> 'Prefix':
        ...

    def __mul__(self, other: Any) -> 'Union[Unit, Prefix]':
        if isinstance(other, Unit):
            return Unit(self.value * other.value)
        if isinstance(other, Prefix):
            return Prefix(other.value * self.value)
        return NotImplemented

    def __rmul__(self, other: Any) -> 'UnfinishedUnitOrQuantity':
        return UnfinishedUnitOrQuantity(self, other)

    def __array_ufunc__(self, ufunc: Any, method: Any, *inputs: Any, **kwargs: Any) -> Any:
        # Handle numpy operations by converting to float. Required to prevent numpy arrays from losing dtypes.
        input_list = list(inputs)
        for i in range(len(input_list)):
            if input_list[i] is self:
                input_list[i] = self.value
        return getattr(ufunc, method)(*input_list, **kwargs)


class UnfinishedUnitOrQuantity(Generic[TType]):
    """Represents a partially assembled quantity obtained by multiplying values, units and prefixes."""

    def __init__(self, prefix: Prefix, prepend: TType):
        self.prefix = prefix
        self.prepend = prepend

    @overload
    def __mul__(self, other: Unit) -> TType:
        ...

    @overload
    def __mul__(self, other: Prefix) -> 'UnfinishedUnitOrQuantity[TType]':
        ...

    def __mul__(self, other: Any) -> 'Union[TType, UnfinishedUnitOrQuantity[TType]]':
        if isinstance(other, Unit):
            return self.prepend * (self.prefix * other)
        if isinstance(other, Prefix):
            return UnfinishedUnitOrQuantity(self.prefix * other, self.prepend)
        return NotImplemented


yotta = Prefix(1e24)
zetta = Prefix(1e21)
exa = Prefix(1e18)
peta = Prefix(1e15)
tera = Prefix(1e12)
giga = Prefix(1e9)
mega = Prefix(1e6)
kilo = Prefix(1e3)
hecto = Prefix(1e2)
deca = Prefix(10)
deci = Prefix(1e-1)
centi = Prefix(1e-2)
milli = Prefix(1e-3)
micro = Prefix(1e-6)
nano = Prefix(1e-9)
pico = Prefix(1e-12)
femto = Prefix(1e-15)
atto = Prefix(1e-18)
zepto = Prefix(1e-21)
yocto = Prefix(1e-24)

second = Unit(1e12)
r"""The second (:math:`\text{s}`), the SI unit of time."""

meter = Unit(1e9)
r"""The meter (:math:`\text{m}`), the SI unit of length."""

dalton = Unit(1)
r"""The dalton (:math:`\text{Da}`) or 'unified atomic mass' (:math:`\text{u}`) unit of mass."""

amu = dalton
r"""The atomic mass unit (:math:`\text{amu}`) unit of mass."""

gram = Unit(6.02214076e23)
r"""The gram (:math:`\text{g}`), the SI unit of mass."""

elementary_charge = Unit(1)
r"""The elementary charge (:math:`\text{e}`) as a unit of charge."""

coulomb = Unit(6.241509074e18)
r"""The coulomb (:math:`\text{C}`), the SI unit of charge."""

kelvin = Unit(1)
r"""The kelvin (:math:`\text{K}`), the SI unit of absolute temperature."""

radian = Unit(1)
r"""The radian (:math:`\text{rad}`), the natural unit of angle."""

degree = Unit(math.pi / 180.0)
r"""The degree (:math:`^{\circ}`) unit of angle."""

joule = Unit(kilo * gram * meter * meter / (second * second))
r"""The joule (:math:`\text{J}`), the SI unit of energy defined as :math:`1 \text{J}
= 1 \text{kg} \text{m}^2 \text{s}^{-2}`."""

mole = Unit(6.02214076e23)
r"""The mole (:math:`\text{mol}`) unit of quantity, equal to Avogadro's constant."""

angstrom = Unit(1e-10 * meter)
r"""The angstrom (:math:`\text{\AA}`) unit of length."""

electronvolt = Unit(1.602176634e-19 * joule)
r"""The electronvolt (:math:`\text{eV}`) unit of energy."""

calorie = Unit(4.184 * joule)
r"""The (gram) calorie (:math:`\text{cal}`) unit of energy."""

newton = Unit(kilo * gram * meter / (second * second))
r"""The newton (:math:`\text{N}`), the SI unit of force defined as :math:`1 \text{N}
= 1 \text{kg} \text{m} \text{s}^{-2}`."""

pascal = Unit(newton / (meter * meter))
r"""The pascal (:math:`\text{Pa}`), the SI unit of pressure defined as :math:`1 \text{N}
= 1 \text{kg} \text{m}^{-1} \text{s}^{-2}`."""

bar = Unit(1e5 * pascal)
r"""The bar (:math:`\text{bar}`) unit of pressure."""

atmosphere = Unit(1.01325e5 * pascal)
r"""The atmosphere (:math:`\text{atm}`) unit of pressure."""

bohr = Unit(5.29177210903e-11 * meter)
r"""The Bohr radius (:math:`\text{a_0}`) unit of length."""

hartree = Unit(4.3597447222071e-18 * joule)
r"""The Hartree (:math:`\text{Ha}`) unit of energy."""

statcoulomb = Unit(3.33564095198152e-10 * coulomb)
r"""The statcoulomb (:math:`\text{statC}`) unit of charge."""

volt = Unit(joule / coulomb)
r"""The volt (:math:`\text{V}`) unit of electric field."""

statvolt = Unit(299.792458 * volt)
r"""The statvolt (:math:`\text{statV}`) unit of electric field."""

esu = Unit(statcoulomb)
r"""The electrostatic unit of charge (:math:`\text{esu}`) unit of charge"""

dyne = Unit(1e-5 * newton)
r"""The dyne (:math:`\text{dyn}`) unit of force."""

debye = Unit(1e-18 * statcoulomb * centi * meter)
r"""The debye (:math:`\text{D}`) unit of pressure."""

poise = Unit(0.1 * pascal * second)
r"""The poise (:math:`\text{P}`) unit of dynamic viscosity."""

atomic_time_unit = Unit(1.03275e-15 * second)
r"""The atomic time unit of time."""

amp = Unit(coulomb / second)
r"""The ampere (:math:`\text{A}`) unit of current."""

erg = Unit(1e-7 * joule)
r"""The erg (:math:`\text{erg}`) unit of energy."""


class UnitConversion:
    """Conversion between two distinct unit systems."""

    def __init__(self, a: 'UnitSystem', b: 'UnitSystem'):
        self._from = a
        self._to = b

    def __getattr__(self, name: str) -> Unit:
        return getattr(self._from, name) / getattr(self._to, name)  # type: ignore


class UnitSystem:
    """
    System of units which can be converted between each other.

    Accessing an attribute such as .length or .time gives the corresponding value in units compatible with Narupa.
    """

    def _add_if_missing(self, key: str, unit: Unit) -> None:
        if key not in self._units:
            self._units[key] = unit

    def __init__(self, **kwargs: Union[float, Unit]):
        self._units = {}
        for name, value in kwargs.items():
            self._units[name] = Unit(value)
        with contextlib.suppress(AttributeError):
            self._add_if_missing('velocity', Unit(self.length / self.time))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('force', Unit(self.mass * self.length / (self.time * self.time)))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('energy', Unit(self.force * self.length))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('torque', Unit(self.force * self.length))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('dipole_moment', Unit(self.charge * self.length))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('electric_field', Unit(self.energy / self.charge / self.length))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('pressure', Unit(self.force / (self.length * self.length)))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('dynamic_viscosity', Unit(self.pressure * self.time))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('density', Unit(self.mass / (self.length ** 3)))
        with contextlib.suppress(AttributeError):
            self._add_if_missing('density2d', Unit(self.mass / (self.length ** 2)))

    def __rshift__(self, other: 'UnitSystem') -> 'UnitConversion':
        return UnitConversion(self, other)

    def __lshift__(self, other: 'UnitSystem') -> 'UnitConversion':
        return UnitConversion(other, self)

    @property
    def length(self) -> Unit:
        """Length unit in nanometers."""
        return self._units['length']

    @property
    def time(self) -> Unit:
        """Time unit in picoseconds."""
        return self._units['time']

    @property
    def mass(self) -> Unit:
        """Mass unit in a.m.u."""
        return self._units['mass']

    @property
    def charge(self) -> Unit:
        """Charge unit in elementary charge."""
        return self._units['charge']

    @property
    def temperature(self) -> Unit:
        """Absolute temperature unit in kelvin."""
        return self._units['temperature']

    @property
    def angle(self) -> Unit:
        """Angle unit in radians."""
        return self._units['angle']

    @property
    def velocity(self) -> Unit:
        """Velocity unit in nanometers per picosecond."""
        return self._units['velocity']

    @property
    def force(self) -> Unit:
        """Force unit in kilojoules per mole per nanometer."""
        return self._units['force']

    @property
    def energy(self) -> Unit:
        """Energy unit in kilojoules per mole."""
        return self._units['energy']

    @property
    def torque(self) -> Unit:
        """Torque unit in kilojoules per mole."""
        return self._units['torque']

    @property
    def dipole_moment(self) -> Unit:
        """Dipole moment in elementary charge nano meters."""
        return self._units['dipole_moment']

    @property
    def electric_field(self) -> Unit:
        """Electric field in kilojoules per mole per elemetary charge per nanometer."""
        return self._units['electric_field']

    @property
    def pressure(self) -> Unit:
        """Pressure unit in kilojoules per mole per nanometers cubed."""
        return self._units['pressure']

    @property
    def dynamic_viscosity(self) -> Unit:
        """Dynamic viscosity unit in kilojoules picosecond per mole per nanometers cubed"""
        return self._units['dynamic_viscosity']

    @property
    def density(self) -> Unit:
        """Density unit in a.m.u. per cubic nanometer."""
        return self._units['density']

    @property
    def density2d(self) -> Unit:
        """2D density unit in a.m.u. per square nanometer."""
        return self._units['density2d']


UnitsNarupa = UnitSystem(length=nano * meter,
                         time=pico * second,
                         mass=amu,
                         charge=elementary_charge,
                         temperature=kelvin,
                         angle=radian)
"""Unit system used by Narupa/narupatools."""
