"""Maps ticks helpers."""

from matplotlib.ticker import Formatter, FuncFormatter


class UnitFormatter(Formatter):
    """Format numbers with a unit.

    Parameters
    ----------
    unit: str, optional
        A string that will be appended to the label. It may be
        ``None`` or empty to indicate that no unit should be used. LaTeX
        special characters are escaped in ``unit`` whenever latex mode is
        enabled, unless `is_latex` is ``True``.

    sep: str, optional
        Separator used between the value and the unit.
        Default is a `space` but it can be remove with empty value.

    """

    def __init__(self, unit='', sep=' '):
        self.unit = unit
        self.sep = sep

    def __call__(self, x, pos=None):
        """Format the tick as a number with the appropriate scaling and a unit."""
        s = f'{x:,g}{self.sep}{self.unit}'
        if self.sep and s.endswith(self.sep):
            s = s[:-len(self.sep)]
        return self.fix_minus(s)


km_ticks = UnitFormatter('km')
km_s_ticks = UnitFormatter('km/s')
deg_ticks = UnitFormatter('°', sep='')
hr_ticks = UnitFormatter('h')


@FuncFormatter
def lat_ticks(lat, pos=None):  # pylint: disable=unused-argument
    """Latitude ticks formatter."""
    if lat == 90:
        return 'N.P.'

    if lat == 0:
        return 'Eq.'

    if lat == -90:
        return 'S.P.'

    if lat < 0:
        return f'{-lat}°S'

    return f'{lat}°N'


@FuncFormatter
def lon_e_ticks(lon_e, pos=None):  # pylint: disable=unused-argument
    """East longitude ticks formatter."""
    if lon_e % 180 == 0:
        return f'{lon_e % 360}°'

    return f'{lon_e % 360}°E'


@FuncFormatter
def lon_w_ticks(lon_w, pos=None):  # pylint: disable=unused-argument
    """West longitude ticks formatter."""
    if lon_w % 180 == 0:
        return f'{lon_w % 360}°'

    return f'{lon_w % 360}°W'
