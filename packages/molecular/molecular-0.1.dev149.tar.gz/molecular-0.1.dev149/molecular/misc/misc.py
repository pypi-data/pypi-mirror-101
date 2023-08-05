
import numpy as np
from typelike import ArrayLike


# Assert that an array is incremental
def assert_incremental(a, increment=1):
    """
    Assert that something like an array has entries that increment by a specific value.

    Parameters
    ----------
    a : ArrayLike
        Array to check if entries increment by specific value.
    increment : int
        Increment value.

    Raises
    ------
    AssertionError
        If `a` does not have entries that increment by `increment`
    """

    assert is_incremental(a, increment=increment)


# Test if an array is incremental
def is_incremental(a, increment=1):
    return (np.diff(a) == increment).all()


# Pairwise Cartesian generator
def pairwise_cartesian(a):
    """
    Return the Cartesian product of `a` as a generator. However, only unique pairs will be returned.

    Parameters
    ----------
    a : array-like

    Returns
    -------
    Pairwise Cartesian product
        generator
    """

    for i in range(len(a)):
        for j in range(i+1, len(a)):
            yield a[i], a[j]


# Convenience zfill function
def zfill(a, width=None):
    if width is None:
        return a
    elif hasattr(a, '__getitem__'):
        return np.char.zfill(list(map(str, a)), width)
    else:
        return str(a).zfill(width)
