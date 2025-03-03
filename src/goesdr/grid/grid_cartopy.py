"""
Calculate latitude and longitude grids data using cartopy.

Notes
-----
See GOES-R Product User Guide (PUG) Volume 5 (L2 products) Section 4.2.8
for details & example of calculations.

Functions
---------
calculate_latlon_grid_cartopy
    Calculate latitude and longitude grids using the cartopy package.
"""

from netCDF4 import Dataset  # pylint: disable=no-name-in-module
from numpy import float32, meshgrid

from ..projection import GOESABIFixedGridArray, GOESProjection
from .array import ArrayFloat32, ArrayFloat64
from .grid_helper import calculate_pixel_edges, make_consistent


def calculate_latlon_grid_cartopy(
    record: Dataset, corners: bool, step: tuple[int, int] | None
) -> tuple[ArrayFloat32, ArrayFloat32]:
    """
    Calculate latitude and longitude grids using the cartopy package.

    Calculate latitude and longitude from GOES ABI fixed grid projection
    data. GOES ABI fixed grid projection is a map projection relative to
    the GOES satellite.

    Units: latitude in °N (°S < 0), longitude in °E (°W < 0)

    Parameters:
    -----------
    record : Dataset
        The netCDF dataset containing GOES ABI L1b or L2 data with ABI
        fixed grid projection information. It is .nc file opened using
        the netCDF4 library.
    corners : bool
        If True, calculate the coordinates of the intersections
        (corners) of the grid. If False, calculate the coordinates of
        the center of the grid.

    Returns:
    --------
    tuple[ArrayFloat32, ArrayFloat32]
        A tuple containing the latitude and longitude grid data.
    """
    try:
        import cartopy.crs as ccrs
    except ImportError as error:
        raise ImportError(
            "The 'cartopy' package is required for this functionality."
        ) from error

    grid_data = GOESABIFixedGridArray(record)
    projection_info = GOESProjection(record)

    x_m: ArrayFloat64 = grid_data.x * projection_info.perspective_point_height
    y_m: ArrayFloat64 = grid_data.y * projection_info.perspective_point_height

    if corners:
        x_m = calculate_pixel_edges(x_m)
        y_m = calculate_pixel_edges(y_m)

    if step:
        x_m = x_m[:: step[1]]
        y_m = y_m[:: step[0]]

    x_m, y_m = meshgrid(x_m, y_m)

    globe = ccrs.Globe(
        ellipse=None,
        semimajor_axis=projection_info.semi_major_axis,
        semiminor_axis=projection_info.semi_minor_axis,
    )

    geos_proj = ccrs.Geostationary(
        satellite_height=projection_info.perspective_point_height,
        central_longitude=projection_info.longitude_of_projection_origin,
        sweep_axis=projection_info.sweep_angle_axis,
        globe=globe,
    )

    globe_grs80 = ccrs.Globe(ellipse="GRS80")

    plate_carree = ccrs.PlateCarree(globe=globe_grs80)

    points = plate_carree.transform_points(geos_proj, x_m, y_m)

    abi_lon: ArrayFloat64 = points[..., 0]
    abi_lat: ArrayFloat64 = points[..., 1]

    abi_lon, abi_lat = make_consistent(abi_lon, abi_lat)

    return abi_lat.astype(float32), abi_lon.astype(float32)
