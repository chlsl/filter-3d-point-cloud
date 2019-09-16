#!/usr/bin/env python3

import iio
import numpy as np
# from s2p import triangulation
from fpc import filter_xyz

image = iio.read('test_image.tif')  # iio use 3rd dim for color channels
image = image.squeeze().astype('float32')
h, w = image.shape

xyz_array = np.zeros((h, w, 3), dtype='float32')
xyz_array[:, :, 0] = np.broadcast_to(np.arange(w, dtype='float32'), (h, w))
xyz_array[:, :, 1] = np.broadcast_to(np.transpose(
                     np.arange(h, dtype='float32')[np.newaxis], (1, 0)), (h, w))
xyz_array[:, :, 2] = 100 + image * 50

# xyz_array = np.array(
#         [np.broadcast_to(np.arange(image.shape[1], dtype=np.float32), image.shape[0:2]),
#          np.broadcast_to(np.transpose(
#              np.arange(image.shape[0], dtype=np.float32)[np.newaxis], (1, 0)), image.shape[0:2]),
#          image*255]
#         ).transpose((1, 2, 0))
# xyz_array = xyz_array.astype('float32')

r = 3.0  # filtering radius, in meters
n = 2  # number of points (under which a pixel is rejected)
img_gsd = 1

# triangulation.filter_xyz(xyz_array, r, n, img_gsd)
filter_xyz(xyz_array, r, n, img_gsd)

output = xyz_array[:, :, 2].squeeze()
easting = xyz_array[:, :, 0].squeeze()
northing = xyz_array[:, :, 1].squeeze()

# iio.write('test_out.tif', xyz_array)
iio.write('test_out.tif', (output - 100) / 50 )
iio.write('test_easting.tif', easting)
iio.write('test_northing.tif', northing)

