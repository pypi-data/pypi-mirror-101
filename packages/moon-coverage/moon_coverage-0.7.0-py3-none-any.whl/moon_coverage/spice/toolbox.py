"""SPICE toolbox helper module."""

import numpy as np

import spiceypy as sp

from .references import SPICERef
from .times import et


def is_iter(value):
    """Check if a value is iterable."""
    return isinstance(value, (list, tuple, np.ndarray))


def deg(rad):
    """Convert radian angle in degrees."""
    return np.multiply(rad, sp.dpr())


def rlonlat(pt):
    """Convert point location in planetocentric coordinates.

    Parameters
    ----------
    pt: tuple
        Input XYZ cartesian coordinates.

    Returns
    -------
    float
        Point radius (in km).
    float
        East planetocentric longitude (in degree).
    float
        North planetocentric latitude (in degree).

    Note
    ----
    - If the X and Y components of `pt` are both zero, the longitude is set to zero.
    - If `pt` is the zero vector, longitude and latitude are both set to zero.

    See Also
    --------
    spiceypy.reclat

    """
    big = np.max(np.abs(pt), axis=0)

    if np.ndim(pt) < 2:
        if big == 0:
            return 0, 0, 0

        xyz = np.divide(pt, big)
    else:
        xyz = np.zeros_like(pt)
        np.divide(pt, big, where=big > 0, out=xyz, casting='unsafe')

    radius = big * np.sqrt(np.sum(np.power(xyz, 2), axis=0))
    lat_rad = np.arctan2(xyz[2], np.sqrt(np.sum(np.power(xyz[:2], 2), axis=0)))

    lon_e_rad = np.zeros_like(radius)
    np.arctan2(xyz[1], xyz[0], out=lon_e_rad)

    return radius, deg(lon_e_rad) % 360, deg(lat_rad)


def sub_obs_pt(time, observer, target, abcorr='NONE', method='NEAR POINT/ELLIPSOID'):
    """Sub-observer point calculation.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
    observer: str
        Observer name.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Computation method to be used.
        Possible values:
            - 'NEAR POINT/ELLIPSOID' (default)
            - 'INTERCEPT/ELLIPSOID'
            - 'NADIR/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'
            - 'INTERCEPT/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'

        (See NAIF :func:`subpnt` for more details).

    Returns
    -------
    (float, float, float) or np.ndarray
        Sub-observer XYZ coordinates in the target body fixed frame
        (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    spiceypy.subpnt

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time):
        return np.transpose([
            sub_obs_pt(t, observer, target, abcorr=abcorr, method=method)
            for t in time
        ])

    xyz, _, _ = sp.subpnt(method, str(target), time, target.iau_frame,
                          abcorr, str(observer))

    return xyz


def obs_state(time, observer, target, abcorr='NONE'):
    """Observer position and velocity relative to the target.

    The position vector starts from the target body to the observer:

        target ------> observer
                (km)

    The velocity vector correspond to the observer motion (in km/s).

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    observer: str
        Observer name.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    (float, float, float) or np.ndarray
        Observer XYZ position and velocity coordinates in
        the target body fixed frame (expressed in km and km/s).

        If a list of time were provided, the results will be stored
        in a (6, N) array.

    Warning
    -------
    If a aberration correction is applied, you must use the `reception` case
    (departing from the target location at `ET - LT`).

    See Also
    --------
    spiceypy.spkezr

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time):
        return np.transpose([
            obs_state(t, observer, target, abcorr=abcorr)
            for t in time
        ])

    state, _ = sp.spkezr(str(target), time, target.iau_frame,
                         abcorr, str(observer))
    return np.negative(state)


def local_time(time, lon, target, lon_type='PLANETOCENTRIC'):
    """Local solar time.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
    lon: float or list or tuple
        Longitude of surface point (degree).
    target: str
        Target body name.
    lon_type: str, optional
        Form of longitude supplied by the variable :py:attr:`lon`.
        Possible values:
            - `PLANETOCENTRIC` (default)
            - `PLANETOGRAPHIC`

        (See NAIF :func:`et2lst` for more details).

    Returns
    -------
    float or np.ndarray
        Local solar time (expressed in decimal hours).

        If a list of :py:attr:`time` or :py:attr:`lon`
        were provided, the results will be stored
        in an array.


    Raises
    ------
    ValueError
        If the :py:attr:`time` and :py:attr:`lon` are both
        arrays but their size don't match.

    See Also
    --------
    spiceypy.et2lst

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time) and is_iter(lon):
        if len(time) != len(lon):
            raise ValueError(
                'The ephemeris times and longitudes must have the same size: '
                f'{len(time)} vs {len(lon)}'
            )

        return np.transpose([
            local_time(t, l, target, lon_type) for t, l in zip(time, lon)
        ])

    if is_iter(time):
        return local_time(time, [lon] * len(time), target, lon_type)

    if is_iter(lon):
        return local_time([time] * len(lon), lon, target, lon_type)

    h, m, s, *_ = sp.et2lst(time, int(target), np.radians(lon), lon_type)

    return h + m / 60 + s / 3600


def illum_angles(time, observer, target, pt, abcorr='NONE', method='ELLIPSOID'):
    """Illumination angles.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
    observer: str
        Observer name.
    target: str
        Target body name.
    pt: np.ndarray
        Surface point (XYZ coordinates).
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Form of longitude supplied by the variable :py:attr:`lon`.
        Possible values:
            - `ELLIPSOID` (default)
            - `DSK/UNPRIORITIZED[/SURFACES = <surface list>]`

        (See NAIF :func:`ilumin` for more details).

    Returns
    -------
    float or np.ndarray
        Solar incidence, emission and phase angles at the surface point (degrees).

        If a list of time were provided, the results will be stored in a (3, N) array.

    Raises
    ------
    ValueError
        If the :py:attr:`time` and :py:attr:`lon` are both
        arrays but their size don't match.

    See Also
    --------
    spiceypy.ilumin

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time) and np.ndim(pt) > 1:
        if len(time) != np.shape(pt)[1]:
            raise ValueError(
                'The ephemeris times and surface point must have the same size: '
                f'{len(time)} vs {len(pt)}'
            )

        return np.transpose([
            illum_angles(t, observer, target, _pt, abcorr=abcorr, method=method)
            for t, _pt in zip(time, np.transpose(pt))
        ])

    if is_iter(time):
        return illum_angles(time, observer, target, np.transpose([pt] * len(time)),
                            abcorr=abcorr, method=method)

    if np.ndim(pt) > 1:
        return illum_angles([time] * np.shape(pt)[1], observer, target,
                            pt, abcorr=abcorr, method=method)

    *_, p, i, e = sp.ilumin(method, str(target), time,
                            target.iau_frame, abcorr, str(observer), pt)

    return np.degrees([i, e, p])


def sun_pos(time, target, abcorr='NONE'):
    """Sun position relative to the target.

    The vector starts from the target body to the Sun:

        target ------> Sun
                (km)

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    (float, float, float) or np.ndarray
        Sun XYZ coordinates in the target body fixed frame
        (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    spiceypy.spkpos

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time):
        return np.transpose([
            sun_pos(t, target, abcorr=abcorr)
            for t in time
        ])

    xyz, _ = sp.spkpos('SUN', time, target.iau_frame, abcorr, str(target))

    return xyz


def solar_longitude(time, target, abcorr='NONE'):
    """Seasonal solar longitude (degrees).

    Compute the angle from the vernal equinox of the main parent
    body.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    float or np.ndarray
        Solar longitude angle(s) (degrees).

        If a list of :py:attr:`time` were provided,
        the results will be stored in an array.

    Note
    ----
    It the target parent is not the SUN the target will be change
    for its own parent.

    See Also
    --------
    spiceypy.lspcn

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if target.parent != 'SUN':
        solar_longitude(time, target.parent, abcorr=abcorr)

    if is_iter(time):
        return np.transpose([
            solar_longitude(t, target, abcorr=abcorr)
            for t in time
        ])

    solar_lon = sp.lspcn(target, time, abcorr)

    return np.degrees(solar_lon)


def true_anomaly(time, target, abcorr='NONE', frame='ECLIPJ2000'):
    """Target orbital true anomaly (degrees).

    The angular position of the target in its orbit
    compare to its periapsis.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')
    frame: str, optional
        Inertial frame to compute the state vector
        (default: `ECLIPJ2000`).

    Returns
    -------
    float or np.ndarray
        True anomaly angle (degrees).

        If a list of :py:attr:`time` were provided,
        the results will be stored in an array.

    See Also
    --------
    spiceypy.spkezr
    spiceypy.oscltx

    """
    if isinstance(time, str):
        time = et(time)

    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if is_iter(time):
        return np.transpose([
            true_anomaly(t, target, abcorr=abcorr, frame=frame)
            for t in time
        ])

    state, _ = sp.spkezr(str(target.parent), time, frame, abcorr, str(target))
    nu = sp.oscltx(np.negative(state), time, target.parent.mu)[8]

    return np.degrees(nu)


def groundtrack_velocity(target, state):
    """Ground track velocity (km/s).

    Speed motion of the sub-observer point along the groundtrack.

    Caution
    -------
    This speed does not correspond to the norm of the rejection
    of the velocity vector of the observer in the target fixed frame.

    Warning
    -------
    This formula is only valid for a spheroid elongated along the
    axis of rotation (``c``). It is not correct for a generic ellipsoid.

    Parameters
    ----------
    target: str
        Target body name.
    state: str
        Target -> observer state position and velocity vectors.

    Returns
    -------
    float or np.ndarray
        Ground track velocity (km/s).

        If a list of :py:attr:`state` is provided,
        the results will be stored in an array.

    Raises
    ------
    ValueError
        If the :py:attr:`state` arrays doesn't have the good shape.

    Note
    ----
    The tangential speed is obtained as product of the local radius of the
    observed body with the tangential angular speed:

        latitudinal
        component
            ^   x
            |  /
            | / <- tangential component
            |/
            o----> longitudinal component

                (the cos is to compensate the 'shrinking' of
                 longitude incerasing the latitude)

    See Also
    --------
    spiceypy.recgeo
    spiceypy.dgeodr
    spiceypy.mxv

    """
    if not isinstance(target, SPICERef):
        target = SPICERef(target)

    if np.ndim(state) > 1:
        return np.transpose([
            groundtrack_velocity(target, s) for s in np.transpose(state)
        ])

    if np.shape(state)[0] != 6:
        raise ValueError('Invalid `state` shape.')

    xyz, v = state[:3], state[3:]

    re, _, rp = target.radii  # target equatorial and polar radii
    f = (re - rp) / re        # target flattening factor

    # Local radius
    _, lat, _ = sp.recgeo(xyz, re, f)
    r = re * rp / (np.sqrt((re**2 * np.sin(lat)**2) + (rp**2 * np.cos(lat)**2)))

    # Geodetic speed
    jacobi = sp.dgeodr(*xyz, re, f)
    vlon, vlat, vr = sp.mxv(jacobi, v)  # Longitudinal, latitudinal and radial components

    # Groundtrack speed
    gt_speed = np.sqrt(r**2 * ((vlon * np.cos(lat))**2 + vlat**2) + vr**2)

    return gt_speed
