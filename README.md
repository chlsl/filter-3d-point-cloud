Small filter to remove outliers in 3D point clouds.
Most functions of this repository are bare copies of functions written by Carlo
de Franchis et al. for [s2p](https://github.com/cmla/s2p), extracted from s2p so
as to easily test the 3D point cloud filtering part.

Contrarily to the initial function in s2p that has an erosion effect, the method
implemented here preserve all the inliers.

