"""
Calculate latitude and longitude grids data.

Notes
-----
See GOES-R Product User Guide (PUG) Volume 5 (L2 products) Section 4.2.8
for details & example of calculations.

Functions
---------
calculate_latlon_noaa
    Calculate latitude and longitude grids using NOAA's algorithm.
"""

from netCDF4 import Dataset  # pylint: disable=no-name-in-module
from numpy import (
    arctan,
    cos,
    float32,
    float64,
    meshgrid,
    pi,
    power,
    sin,
    sqrt,
)

from .array import ArrayFloat32
from .grid_helper import calculate_pixel_edges, make_common_mask


def calculate_latlon_grid_noaa(
    record: Dataset, corners: bool
) -> tuple[ArrayFloat32, ArrayFloat32]:
    """
    Calculate latitude and longitude grids using NOAA's algorithm.

    Calculate latitude and longitude from GOES ABI fixed grid projection
    data. GOES ABI fixed grid projection is a map projection relative to
    the GOES satellite.

    Units: latitude in °N (°S < 0), longitude in °E (°W < 0)

    Parameters
    ----------
    record : Dataset
        The netCDF dataset containing GOES ABI L1b or L2 data with ABI
        fixed grid projection information. It is .nc file opened using
        the netCDF4 library.
    corners : bool
        If True, calculate the coordinates of the intersections
        (corners) of the grid. If False, calculate the coordinates of
        the center of the grid.

    Returns
    -------
    tuple[ArrayFloat32, ArrayFloat32]
        A tuple containing the latitude and longitude grid data.
    """
    # Read in GOES ABI fixed grid projection variables and constants

    # E/W scanning angle in radians
    x_coordinate_1d = record.variables["x"][:].data

    # N/S elevation angle in radians
    y_coordinate_1d = record.variables["y"][:].data

    if corners:
        x_coordinate_1d = calculate_pixel_edges(x_coordinate_1d)
        y_coordinate_1d = calculate_pixel_edges(y_coordinate_1d)

    projection_info = record.variables["goes_imager_projection"]
    lon_origin = projection_info.longitude_of_projection_origin
    r_orb = (
        projection_info.perspective_point_height
        + projection_info.semi_major_axis
    )
    r_eq = projection_info.semi_major_axis
    r_pol = projection_info.semi_minor_axis

    # Create 2D coordinate matrices from 1D coordinate vectors
    x_coordinate_2d, y_coordinate_2d = meshgrid(
        x_coordinate_1d.astype(float64), y_coordinate_1d.astype(float64)
    )

    # Equations to calculate latitude and longitude
    lambda_0 = (lon_origin * pi) / 180.0
    a_var = power(sin(x_coordinate_2d), 2.0) + (
        power(cos(x_coordinate_2d), 2.0)
        * (
            power(cos(y_coordinate_2d), 2.0)
            + (
                ((r_eq * r_eq) / (r_pol * r_pol))
                * power(sin(y_coordinate_2d), 2.0)
            )
        )
    )

    b_var = -2.0 * r_orb * cos(x_coordinate_2d) * cos(y_coordinate_2d)
    c_var = (r_orb**2.0) - (r_eq**2.0)
    r_s = (-1.0 * b_var - sqrt((b_var**2) - (4.0 * a_var * c_var))) / (
        2.0 * a_var
    )
    s_x = r_s * cos(x_coordinate_2d) * cos(y_coordinate_2d)
    s_y = -r_s * sin(x_coordinate_2d)
    s_z = r_s * cos(x_coordinate_2d) * sin(y_coordinate_2d)

    abi_lat = (180.0 / pi) * (
        arctan(
            ((r_eq * r_eq) / (r_pol * r_pol))
            * (s_z / sqrt(((r_orb - s_x) * (r_orb - s_x)) + (s_y * s_y)))
        )
    )
    abi_lon = (lambda_0 - arctan(s_y / (r_orb - s_x))) * (180.0 / pi)

    abi_lat, abi_lon = make_common_mask(abi_lat, abi_lon)

    return abi_lat.astype(float32), abi_lon.astype(float32)
