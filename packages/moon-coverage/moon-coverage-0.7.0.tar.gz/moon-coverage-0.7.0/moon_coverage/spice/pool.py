"""SPICE kernel pool module."""

import numpy as np

import spiceypy as sp

from .references import SPICERef
from .times import tdb, utc
from ..misc import logger


log_spice_pool, debug_spice_pool = logger('SPICE Pool')


class MetaSPICEPool(type):
    """Meta SPICE kernel pool object."""
    # pylint: disable=no-value-for-parameter, unsupported-membership-test

    def __repr__(cls):
        n = int(cls)
        if n == 0:
            desc = 'EMPTY'
        else:
            desc = f'{n} kernel'
            desc += 's'
            desc += ' loaded:\n - '
            desc += '\n - '.join(cls.kernels)

        return f'<{cls.__name__}> {desc}'

    def __int__(cls):
        return cls.count()

    def __len__(cls):
        return cls.count()

    def __hash__(cls):
        return cls.get_pool_hash()

    def __eq__(cls, other):
        if isinstance(other, str):
            return cls == [other]

        if isinstance(other, list):
            return cls == tuple(other)

        return hash(cls) == hash(other)

    def __iter__(cls):
        return iter(cls.kernels)

    def __contains__(cls, el):
        return cls.contains(el)

    def __add__(cls, el):
        return cls.add(el)

    def __sub__(cls, el):
        return cls.remove(el)

    @staticmethod
    def count() -> int:
        """Count the number of kernels in the pool."""
        return int(sp.ktotal('ALL'))

    def get_pool(cls):
        """Get SPICE kernel pool files."""
        return tuple(
            sp.kdata(i, 'ALL')[0] for i in range(cls.count())
        )

    def get_pool_hash(cls):
        """Get SPICE pool content hash."""
        return hash(cls.get_pool())

    @property
    def kernels(cls):
        """Return the lis of kernels loaded in the pool."""
        return cls.get_pool()

    def contains(cls, kernel):
        """Check if the kernel is in the pool."""
        return kernel in cls.kernels

    def add(cls, kernel, purge=False):
        """Add a kernel to the pool."""
        if purge:
            cls.purge()

        if kernel in cls:
            raise ValueError(f'Kernel `{kernel}` is already in the pool.')

        log_spice_pool.debug('Add %s', kernel)
        sp.furnsh(kernel)

    def remove(cls, kernel):
        """Remove the kernel from the pool if present."""
        if kernel not in cls:
            raise ValueError(f'Kernel `{kernel}` is not in the pool.')

        log_spice_pool.debug('Remove %s', kernel)
        sp.unload(kernel)

    @staticmethod
    def purge():
        """Purge the pool from all its content."""
        log_spice_pool.info('Empty the pool')
        sp.kclear()

    def windows(cls, *refs, fmt='UTC'):
        """Get kernels windows on a collection of bodies in the pool.

        Parameters
        ----------
        refs: str, int or SPICERef
            Body(ies) reference(s).
        fmt: str, optional
            Output format:
                - ``UTC`` (default)
                - ``TDB``
                - ``ET``

        Returns
        -------
        [[float,float], …]
            Start and stop times windows in the requested format.

        Raises
        ------
        KeyError
            If the requested reference does not have a specific coverage
            range in the pool.

        """
        refs = {int(ref): ref for ref in map(SPICERef, refs)}

        windows = []
        for i in range(cls.count()):
            kernel, ext, *_ = sp.kdata(i, 'ALL')

            if ext == 'CK':
                ids = set(sp.ckobj(kernel))
                cov = cls._ck_cov

            elif ext == 'PCK':
                ids = sp.cell_int(1000)
                sp.pckfrm(kernel, ids)
                ids = set(ids)
                cov = cls._pck_cov

            elif ext == 'SPK':
                ids = set(sp.spkobj(kernel))
                cov = cls._spk_cov

            else:
                ids = set()
                cov = None

            for ref in ids & set(refs):
                log_spice_pool.debug('Found `%s` in %s', refs[ref], kernel)

                windows.extend(cov(kernel, ref))

        if not windows:
            values = list(refs.values())
            err = 'The windows for '
            err += f'{values[0]} was' if len(values) == 1 else f'{values} were'
            err += ' not found.'
            raise KeyError(err)

        if fmt.upper() == 'UTC':
            windows = np.array([utc(w) for w in windows], dtype=np.datetime64)

        elif fmt.upper() == 'TDB':
            windows = np.array([tdb(w) for w in windows], dtype='<U27')

        elif fmt.upper() != 'ET':
            raise TypeError(
                f'Output format unknown: `{fmt}`, only [`UTC`|`TDB`|`ET`] are accepted.')

        return windows

    @staticmethod
    def _ck_cov(ck, ref: int):
        """Get CK coverage for given body."""
        cover = sp.ckcov(ck, ref, False, 'SEGMENT', 0.0, 'TDB')
        ets = [
            [cover[i * 2], cover[i * 2 + 1]] for i in range(sp.wncard(cover))
        ]

        log_spice_pool.debug('ET windows: %r', ets)
        return ets

    @staticmethod
    def _pck_cov(pck, ref: int):
        """Get PCK coverage for given body."""
        cover = sp.cell_double(2000)
        sp.pckcov(pck, ref, cover)
        ets = list(cover)

        log_spice_pool.debug('ET coverage: %r', ets)
        return [ets]

    @staticmethod
    def _spk_cov(spk, ref: int):
        """Get SPK coverage for given body."""
        ets = list(sp.spkcov(spk, ref))

        log_spice_pool.debug('ET coverage: %r', ets)
        return [ets]

    def coverage(cls, *refs, fmt='UTC'):
        """Get coverage for a collection of bodies in the pool.

        Parameters
        ----------
        refs: str, int or SPICERef
            Body(ies) reference(s).
        fmt: str, optional
            Output format:
                - ``UTC`` (default)
                - ``TDB``
                - ``ET``

        Returns
        -------
        [str, str] or [float, float]
            Start and stop times coveraged for the requested format.

        Note
        ----
        If multiple values are available, only the ``max(start)``
        and ``min(stop)`` are kept.

        Raises
        ------
        TypeError
            If the output format is invalid.
        ValueError
            If the start time is after the stop time

        """
        starts, ends = np.transpose(cls.windows(*refs, fmt='ET'))

        start, stop = np.max(starts), np.min(ends)

        if start > stop:
            raise ValueError(
                f'MAX start time ({tdb(start)}) is after MIN stop time ({tdb(stop)}).')

        if fmt.upper() == 'UTC':
            start, stop = utc(start, stop)

        elif fmt.upper() == 'TDB':
            start, stop = tdb(start, stop)

        elif fmt.upper() != 'ET':
            raise TypeError(
                f'Output format unknown: `{fmt}`, only [`UTC`|`TDB`|`ET`] are accepted.')

        return start, stop


class SPICEPool(metaclass=MetaSPICEPool):
    """SPICE kernel pool object."""
