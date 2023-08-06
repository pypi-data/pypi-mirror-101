"""Projections module.

Projection are based on PROJ project:

    * https://proj.org/

"""

from .equi import Equirectangular
from .equi_gc import Equirectangular as EquirectangularGC
from .ticks import UnitFormatter


__all__ = [
    'Equirectangular',
    'EquirectangularGC',
    'UnitFormatter',
]
