#!/usr/bin/env python3

import iio
import numpy as np
import timeit

from fpc import filter_xyz, filter_xyz_bis


image = iio.read('test_image.tif')  # iio use 3rd dim for color channels
image = image.squeeze().astype('float32')
h, w = image.shape

xyz_array = np.zeros((h, w, 3), dtype='float32')
xyz_array[:, :, 0] = np.broadcast_to(np.arange(w, dtype='float32'), (h, w))
xyz_array[:, :, 1] = np.broadcast_to(np.transpose(
                     np.arange(h, dtype='float32')[np.newaxis], (1, 0)), (h, w))
xyz_array[:, :, 2] = 100 + image * 50

r = 4.0  # filtering radius, in meters
n = 10  # number of points (under which a pixel is rejected)
img_gsd = 1


# filter_xyz(xyz_array, r, n, img_gsd)
filter_xyz_bis(xyz_array, r, n, img_gsd)


output = xyz_array[:, :, 2].squeeze()
easting = xyz_array[:, :, 0].squeeze()
northing = xyz_array[:, :, 1].squeeze()

iio.write('test_out.tif', (output - 100) / 50 )
iio.write('test_easting.tif', easting)
iio.write('test_northing.tif', northing)

# profiling conclusion:
# filter_xyz_bis where the NAN assignement is done with the c function is not
# faster, maybe even slightly slower that filter_xyz (from s2p)
