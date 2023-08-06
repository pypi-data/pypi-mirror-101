"""Masked trajectory module."""

from functools import wraps

import numpy as np

from ..misc import Segment


def trajectory_property(func):
    """Parent trajectory property decorator."""
    @property
    @wraps(func)
    def original_property(_self):
        traj = _self.traj
        prop = func.__name__

        if not hasattr(traj, prop):
            raise AttributeError(
                f'The original trajectory does not have a `{prop}` attribute.')

        return getattr(traj, prop)
    return original_property


def masked_trajectory_property(func):
    """Masked parent trajectory property decorator."""
    @property
    @wraps(func)
    def masked_property(_self):
        traj = _self.traj
        prop = func.__name__

        if not hasattr(traj, prop):
            raise AttributeError(
                f'The original trajectory does not have a `{prop}` attribute.')

        dtype, nan = (float, np.nan) if prop not in ['utc'] else \
            (np.datetime64, np.datetime64('NaT'))

        values = np.array(getattr(traj, prop), dtype=dtype)
        values[..., _self.mask] = nan

        return values

    return masked_property


class MaskedTrajectory:  # pylint: disable=too-many-public-methods
    """Masked trajectroy object.

    Paramters
    ---------
    traj:
        Original trajectory.
    mask: np.ndarray
        Bool list of the points to mask.

    """
    def __init__(self, traj, mask):
        self.traj = traj
        self.mask = mask
        self.seg = Segment(np.invert(mask))

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}> '
            f'Observer: {self.observer} | '
            f'Target: {self.target}'
            f'\n - First UTC start time: {self.start}'
            f'\n - Last UTC stop time: {self.stop}'
            f'\n - Nb of pts: {len(self):,d} (+{self.nb_masked:,d} masked)'
            f'\n - Nb of segments: {self.nb_segments}'
        )

    def __len__(self):
        """Number of point in the trajectory."""
        return len(self.traj) - self.nb_masked

    def __and__(self, other):
        """And ``&`` operator."""
        return self.traj.mask(
            self.traj.intersect(other) | self.mask
        )

    def __xor__(self, other):
        """Hat ``^`` operator."""
        return self.traj.mask(
            self.traj.intersect(other, outside=True) | self.mask
        )

    @property
    def nb_masked(self):
        """Number of point masked."""
        return np.sum(self.mask)

    @property
    def nb_segments(self):
        """Number of segment(s)."""
        return len(self.seg)

    @property
    def starts(self):
        """UTC start time segments."""
        return self.utc[self.seg.istarts]

    @property
    def stops(self):
        """UTC stop time segments."""
        return self.utc[self.seg.istops]

    @property
    def start(self):
        """UTC start time of the initial segment."""
        return self.starts[0] if len(self) != 0 else np.datetime64('NaT')

    @property
    def stop(self):
        """UTC stop time of the last segment."""
        return self.stops[-1] if len(self) != 0 else np.datetime64('NaT')

    @property
    def windows(self):
        """Segmented windows (UTC start and stop times)."""
        return np.vstack([self.starts, self.stops]).T

    @trajectory_property
    def observer(self):
        """Observer SPICE reference for the trajectory."""

    @trajectory_property
    def target(self):
        """Target SPICE reference for the trajectory."""

    @masked_trajectory_property
    def ets(self):
        """Masked ephemeris times."""

    @masked_trajectory_property
    def utc(self):
        """Masked UTC times."""

    @masked_trajectory_property
    def lonlat(self):
        """Masked sub-observer ground track east longitudes and latitudes (degree)."""

    @masked_trajectory_property
    def local_time(self):
        """Masked sub-observer local time (decimal hours)."""

    @masked_trajectory_property
    def inc(self):
        """Masked sub-observer incidence angle (degree)."""

    @masked_trajectory_property
    def emi(self):
        """Masked sub-observer emission angle (degree)."""

    @masked_trajectory_property
    def phase(self):
        """Masked sub-observer phase angle (degree)."""

    @masked_trajectory_property
    def day(self):
        """Masked day side."""

    @masked_trajectory_property
    def night(self):
        """Masked night side."""

    @masked_trajectory_property
    def dist(self):
        """Masked spacecraft distance to target body center (km)."""

    @masked_trajectory_property
    def alt(self):
        """Masked spacecraft altitude to the sub-observer point (km)."""

    @masked_trajectory_property
    def sun_lonlat(self):
        """Masked sub-solar ground track coordinates (degree)."""

    @masked_trajectory_property
    def solar_zenith_angle(self):
        """Masked sub-observer solar zenith angle (degree)."""

    @masked_trajectory_property
    def solar_longitude(self):
        """Masked target seasonal solar longitude (degree)."""

    @masked_trajectory_property
    def true_anomaly(self):
        """Masked target orbital true anomaly (degree)."""

    @masked_trajectory_property
    def groundtrack_velocity(self):
        """Masked groundtrack velocity (km/s)."""
