"""SPICE reference module."""

import numpy as np

import spiceypy as sp
from spiceypy.utils.exceptions import SpiceKERNELVARNOTFOUND


class SPICERef:
    """SPICE reference helper.

    Parameters
    ----------
    name: str
        Reference name


    Raises
    ------
    ValueError
        If this reference is not know in the kernel pool.

    """

    is_IAU = False

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self} (ID: {int(self)})'

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return str(self) == other or int(self) == other

    @property
    def id(self):
        """SPICE reference ID."""
        return self.__id

    @property
    def name(self):
        """SPICE reference name."""
        return self.__name

    @name.setter
    def name(self, name):
        """SPICE object name setter."""
        self.__name = str(name).upper()

        try:
            self.__id = sp.bods2c(self.name)
        except sp.stypes.NotFoundError:
            raise ValueError(f'Unknown reference: `{self.name}`')

        # Check if the reference have a IAU counterpart
        self.is_IAU = sp.namfrm(self.__iau) != 0

    @property
    def __iau(self):
        """Theoretical associated IAU frame."""
        return f'IAU_{self.name}'

    @property
    def iau_frame(self):
        """IAU body fixed frame."""
        if not self.is_IAU:
            raise TypeError(f'This reference doesn\'t `{self.__iau}` exist.')
        return self.__iau

    @property
    def parent(self):
        """Parent body."""
        code = str(int(self))
        if len(code) == 3 and code[0] != '-':
            parent = 'SUN' if code[-2:] == '99' else sp.bodc2n(int(code[0] + '99'))
            return SPICERef(parent)

        raise AttributeError(f'this body `{self}` has no parent.')

    @property
    def radii(self):
        """Body radii, if available (km)."""
        try:
            return sp.bodvrd(str(self), 'RADII', 3)[1]
        except SpiceKERNELVARNOTFOUND:
            raise KeyError(
                f'This body `{self}` does not have a RADII attribute.') from None

    @property
    def radius(self):
        """Body mean radius, if available (km)."""
        return np.cbrt(np.product(self.radii))

    @property
    def r(self):
        """Body mean radius alias."""
        return self.radius

    @property
    def re(self):
        """Body equatorial radius, if available (km)."""
        return self.radii[0]

    @property
    def rp(self):
        """Body polar radius, if available (km)."""
        return self.radii[2]

    @property
    def f(self):
        """Body flattening coefficient, if available (km)."""
        re, _, rp = self.radii
        return (re - rp) / re

    @property
    def mu(self):
        """Gravitational parameter (GM, km³/sec²)."""
        try:
            return sp.bodvrd(str(self), 'GM', 1)[1]
        except SpiceKERNELVARNOTFOUND:
            raise KeyError(
                f'This body `{self}` does not have a GM attribute.') from None
