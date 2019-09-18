import ctypes
from ctypes import c_int, c_float, c_double, byref, POINTER
from numpy.ctypeslib import ndpointer
import numpy as np
import os

here = os.path.dirname(os.path.abspath(__file__))
# lib_path = os.path.join(os.path.dirname(here), 'filt-3D-point-cloud.so')
lib_path = os.path.join(here, 'filt-3D-point-cloud.so')
lib = ctypes.CDLL(lib_path)

def count_3d_neighbors(xyz, r, p):
    """
    Count 3D neighbors of a gridded set of 3D points.

    Args:
        xyz (array): 3D array of shape (h, w, 3) where each pixel contains the
            UTM easting, northing, and altitude of a 3D point.
        r (float): filtering radius, in meters
        p (int): the filering window has size 2p + 1, in pixels

    Returns:
        array of shape (h, w) with the count of the number of 3D points located
        less than r meters from the current 3D point
    """
    h, w, d = xyz.shape
    assert(d == 3)

    # define the argument types of the count_3d_neighbors function from disp_to_h.so
    lib.count_3d_neighbors.argtypes = (ndpointer(dtype=c_int, shape=(h, w)),
                                       ndpointer(dtype=c_float, shape=(h, w, 3)),
                                       c_int, c_int, c_float, c_int)

    # call the count_3d_neighbors function from disp_to_h.so
    out = np.zeros((h, w), dtype='int32')
    lib.count_3d_neighbors(out, np.ascontiguousarray(xyz), w, h, r, p)

    return out


def remove_isolated_3d_points(xyz, r, p, n, q=1):
    """ Remove isolated pixels or group of pixels in a gridded set of 3D points.

    Args:
        xyz (array): 3D array of shape (h, w, 3) where each pixel contains the
            UTM easting, northing, and altitude of a 3D point.
        r (float): filtering radius, in meters
        p (int): the filering window has size 2p + 1, in pixels
    """
    h, w, d = xyz.shape
    assert d == 3, 'expecting a 3-channels image with shape (h, w, 3)'

    lib.remove_isolated_3d_points.argtypes = (
        ndpointer(dtype=c_float, shape=(h, w, 3)),
        c_int, c_int, c_float, c_int, c_int, c_int)

    lib.remove_isolated_3d_points(np.ascontiguousarray(xyz), w, h, r, p, n, q)


def filter_xyz(xyz, r, n, img_gsd):
    """
    Discard (in place) points that have less than n points closer than r meters.

    Args:
        xyz (array): 3D array of shape (h, w, 3) where each pixel contains the
            UTM easting, northing, and altitude of a 3D point.
        r (float): filtering radius, in meters
        n (int): filtering threshold, in number of points
        img_gsd (float): ground sampling distance, in meters / pix
    """
    p = np.ceil(r / img_gsd).astype(int)
    count = count_3d_neighbors(xyz, r, p)
    xyz[count < n] = np.nan


def filter_xyz_bis(xyz, r, n, img_gsd):
    """ The new version of filter_xyz
    """
    p = np.ceil(r / img_gsd).astype(int)
    remove_isolated_3d_points(xyz, r, p, n)


