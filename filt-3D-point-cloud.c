
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


