# GOES-DR — GOES Satellite Imagery Dataset Reader

*Since 1975, Geostationary Operational Environmental Satellites (GOES) have
provided continuous imagery and data on atmospheric conditions and solar
activity (space weather). They have even aided in search and rescue of people
in distress. GOES data products have led to more accurate and timely weather
forecasts and better understanding of long-term climate conditions. The
National Aeronautics and Space Administration (NASA) builds and launches the
GOES, and the National Oceanic and Atmospheric Administration (NOAA) operates
them &#91;[6](#hist)&#93;.*

**GOES-DR** is an open-source Python package that streamlines the process of
reading Level 2 GOES R series satellite imagery. This toolkit enables efficient
reading and extraction of snapshot data segments directly from NetCDF4 files
produced by GOES-R Series satellites &#91;[2](#goesr)&#93;.

## Supported Datasets

1. **GOES 4th Generation (GOES-16 to GOES-18)**: Also known as the R to U
   Series, these satellites offer advanced imagery and atmospheric measurements
   with better spatial, spectral, and temporal resolution &#91;[7](#goesr)&#93;.

## Data Sources

1. **NOAA AWS Cloud Archive**: GOES-16 to GOES-18 data and GridSat-B1 Climate
   Data Record are accessible via the NOAA archive hosted on AWS.

## Project description

Toolset for reading Level 2 GOES R series satellite imagery. Enables the
extraction of snapshot data segments from NetCDF4 files containing GOES R
series (GOES-16 to GOES-18) satellite imagery.

**Keywords:**
[goes](https://github.com/topics/goes),
[satellite](https://github.com/topics/satellite),
[satellite-dataset](https://github.com/topics/satellite-dataset),
[satellite-imagery](https://github.com/topics/satellite-imagery),
[satellite-imagery-analysis](https://github.com/topics/satellite-imagery-analysis),
[satellite-imagery-python](https://github.com/topics/satellite-imagery-python),
[satellite-data](https://github.com/topics/satellite-data),
[noaa](https://github.com/topics/noaa),
[noaa-satellite](https://github.com/topics/noaa-satellite),
[ncei](https://github.com/topics/ncei),
[unidata](https://github.com/topics/unidata),
[unidata-netcdf](https://github.com/topics/unidata-netcdf),
[netcdf](https://github.com/topics/netcdf),
[netcdf4](https://github.com/topics/netcdf4),
[aws](https://github.com/topics/aws),
[open-data](https://github.com/topics/open-data),
[open-source](https://github.com/topics/open-source),
[open-datasets](https://github.com/topics/open-datasets),
[xarray](https://github.com/topics/xarray)

## Contributing

Contributions to **GOES-DR** are welcome! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Open a pull request with a description of your changes.

Please make sure to include tests for any new functionality.

## Requirements

- Python 3.9+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## Acknowledgments

This package relies on data provided by NOAA’s NCEI and NOAA’s archive on AWS.

## Credits

When using **GOES-DR** in any research, publication or website, please cite this
package as:

> Villamayor-Venialbo, W. (2025): *GOES-DR: A Python package for reading
> GOES R Series Level 2 Imagery datasets (Version 0.0.0)* [Software]. GitHub.
> [git:wvenialbo/GOES-DR](https://github.com/wvenialbo/GOES-DR), *[indicate
> access date]*.

**Dataset Citation:**

> GOES-R Algorithm Working Group, and GOES-R Series Program (2017): NOAA GOES-R
> Series Advanced Baseline Imager (ABI) Level 2 Cloud and Moisture Imagery
> Products (CMIP). *[indicate subset used]*. *NOAA National Centers for
> Environmental Information*,
> [doi:10.7289/V5736P36]((https://doi.org/10.7289/V5736P36)), *[access date]*.

Visit [NOAA National Centers for Environmental Information](https://www.ncei.noaa.gov/)
for other product credits.

## Contact and Support

For issues, questions, or requests, feel free to open an issue on this
repository or contact the author, [wvenialbo at
gmail.com](mailto:wvenialbo@gmail.com).

---

## Similar Projects

- [Brian Blaylock's goes2go](https://github.com/blaylockbk/goes2go): Download
  and process GOES-16 and GOES-17 data from NOAA's archive on AWS using Python.
  ([readthedocs](https://goes2go.readthedocs.io/))
- [Joao Henry's GOES](https://github.com/joaohenry23/GOES): Python package to
  download and manipulate GOES-16/17/18 data.

## References

1. GOES-R Algorithm Working Group, and GOES-R Series Program (2017): NOAA
   GOES-R Series Advanced Baseline Imager (ABI) Level 2 Cloud and Moisture
   Imagery Products (CMIP). *[indicate subset used]*. *NOAA National Centers
   for Environmental Information*,
   [doi:10.7289/V5736P36]((https://doi.org/10.7289/V5736P36)), *[access date]*.

2. GOES-R Series Data Products. *GOES-R Website*,
   https://www.goes-r.gov/products/overview.html, retrieved on 2024.<a
   name="goesr"></a>

[0]: hidden_references:
[1]: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00993
[2]: https://registry.opendata.aws/noaa-goes/
[3]: https://docs.opendata.aws/noaa-goes16/cics-readme.html
[4]: https://www.goes-r.gov/
[5]: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00829
