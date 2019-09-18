/* Copyright (C) 2019, Charles Hessel
 * Copyright (C) 2015, Carlo de Franchis <carlo.de-franchis@cmla.ens-cachan.fr>
 * Copyright (C) 2015, Gabriele Facciolo <facciolo@cmla.ens-cachan.fr>
 * Copyright (C) 2015, Enric Meinhardt <enric.meinhardt@cmla.ens-cachan.fr>
 *
 * The two functions:
 *   1) squared_distance_between_3d_points
 *   2) count_3d_neighbors
 * are from s2p (see https://github.com/cmla/s2p).
 * The following ones are by me.
 */


#include <stdlib.h>
#include <stdbool.h>
#include <math.h>


float squared_distance_between_3d_points(float a[3], float b[3])
{
    float x = (a[0] - b[0]);
    float y = (a[1] - b[1]);
    float z = (a[2] - b[2]);
    return x*x + y*y + z*z;
}


void count_3d_neighbors(int *count, float *xyz, int nx, int ny, float r, int p)
{
    // count the 3d neighbors of each point
    for (int y = 0; y < ny; y++)
    for (int x = 0; x < nx; x++) {
        int pos = x + nx * y;
        float *v = xyz + pos * 3;
        int c = 0;
        int i0 = y > p ? -p : -y;
        int i1 = y < ny - p ? p : ny - y - 1;
        int j0 = x > p ? -p : -x;
        int j1 = x < nx - p ? p : nx - x - 1;
        for (int i = i0; i <= i1; i++)
        for (int j = j0; j <= j1; j++) {
            float *u = xyz + (x + j + nx * (y + i)) * 3;
            float d = squared_distance_between_3d_points(u, v);
            if (d < r*r) {
                c++;
            }
        }
        count[pos] = c;
    }
}

void remove_isolated_3d_points(
    float* xyz,  // input (and output) image, dim = (h, w, 3)
    int nx,      // width w
    int ny,      // height h
    float r,     // filtering radius, in meters
    int p,       // filtering window (square of width is 2p+1 pix)
    int n,       // minimal number of neighbors to be an inlier
    int q)       // neighborhood for the saving step (square of width 2q+1)
{
    int *count = (int*) malloc(nx * ny * sizeof(int));
    bool *rejected = (bool*) malloc(nx * ny * sizeof(bool));

    // count the 3d neighbors of each point
    count_3d_neighbors(count, xyz, nx, ny, r, p);

    // brutally reject any point with less than n neighbors
    for (int i = 0; i < ny * nx; i++)
        rejected[i] = count[i] < n;

    // show mercy; save points with at least one close and non-rejected neighbor
    bool need_more_iterations = true;
    while (need_more_iterations) {
        need_more_iterations = false;
        // scan the image and stop at rejected points
        for (int y = 0; y < ny; y++)
        for (int x = 0; x < nx; x++)
        if (rejected[x + y * nx])
        // explore the neighborhood (square of width 2q+1)
        for (int yy = y - q; yy < y + q + 1; yy++) {
            if (yy < 0) continue; else if (yy > ny-1) break;
            for (int xx = x - q; xx < x + q + 1; xx++) {
                if (xx < 0) continue; else if (xx > nx-1) break;
                // is the current rejected point's neighbor non-rejected?
                if (!rejected[xx + yy * nx])
                // is this connected neighbor close (in 3d)?
                if (squared_distance_between_3d_points(xyz + (x + y * nx) * 3,
                                                       xyz + (xx + yy * nx) * 3)
                    < r*r) {
                    rejected[x + y * nx] = false;  // save the point
                    yy = xx = ny + nx + 2*q + 2;  // break loops on yy and xx
                    need_more_iterations = true;  // this point may save others!
                }
            }
        }
    }

    // set to NAN the rejected pixels
    for (int i = 0; i < ny * nx; i++)
        if (rejected[i])
            for (int c = 0; c < 3; c++)
                xyz[c + i * 3] = NAN;

    free(rejected);
    free(count);
}

