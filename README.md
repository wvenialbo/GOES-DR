# GOES-DR — GOES Satellite Imagery Dataset Reader

*Since 1975, Geostationary Operational Environmental Satellites (GOES) have
provided continuous imagery and data on atmospheric conditions and solar
activity (space weather). They have even aided in search and rescue of people
in distress. GOES data products have led to more accurate and timely weather
forecasts and better understanding of long-term climate conditions. The
National Aeronautics and Space Administration (NASA) builds and launches the
GOES, and the National Oceanic and Atmospheric Administration (NOAA) operates
them &#91;[2](#hist)&#93;.*

**GOES-DR** is an open-source Python package that streamlines the process of
reading Level 2 GOES R series satellite imagery. This toolkit enables efficient
reading and extraction of snapshot data segments directly from NetCDF4 files
produced by GOES-R Series satellites &#91;[3](#goesr)&#93;.

## Supported Datasets

1. **GOES 4th Generation (GOES-16 to GOES-18)**: Also known as the R to U
   Series, these satellites offer advanced imagery and atmospheric measurements
   with better spatial, spectral, and temporal resolution &#91;[3](#goesr)&#93;.

See [NOAA Geostationary Operational Environmental Satellites (GOES) 16, 17 &
18][11] and [NOAA GOES on AWS (CICS)][12] for information on the GOES-R Series
data available from NOAA on AWS. You can find much more detailed information
about GOES-R Series data from NOAA's [Geostationary Operational Environmental
Satellites - R Series][0].

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

### Credits for GOES-R Series Data

**Dataset Citation:**

For Cloud and Moisture Imagery Products (CMIP), please cite the following:

> GOES-R Algorithm Working Group, and GOES-R Series Program (2017): NOAA GOES-R
> Series Advanced Baseline Imager (ABI) Level 2 Cloud and Moisture Imagery
> Products (CMIP). *[indicate subset used]*. *NOAA National Centers for
> Environmental Information*, [doi:10.7289/V5736P36][51], *[access date]*.

For other products, please, visit [NOAA National Centers for Environmental
Information][10].

## Contact and Support

For issues, questions, or requests, feel free to open an issue on this
repository or contact the author, [wvenialbo at
gmail.com](mailto:wvenialbo@gmail.com).

---

## Similar Projects

- [Brian Blaylock's goes2go][22]: Download and process GOES-16 and GOES-17 data
  from NOAA's archive on AWS using Python.  ([readthedocs][31])
- [Joao Henry's GOES][23]: Python package to download and manipulate
  GOES-16/17/18 data.

<!-- markdownlint-capture -->
<!-- markdownlint-disable MD033 -->

## References

1. GOES-R Algorithm Working Group, and GOES-R Series Program (2017): NOAA
   GOES-R Series Advanced Baseline Imager (ABI) Level 2 Cloud and Moisture
   Imagery Products (CMIP). *[indicate subset used]*. *NOAA National Centers
   for Environmental Information*,
   [doi:10.7289/V5736P36]((https://doi.org/10.7289/V5736P36)), *[access date]*.
2. GOES History. *GOES-R Website*,
   [https://www.goes-r.gov/mission/history.html][1], retrieved on 2024.<a
   name="hist"></a>
3. GOES-R Series Data Products. *GOES-R Website*,
   [https://www.goes-r.gov/products/overview.html][2], retrieved on 2024.<a
   name="goesr"></a>
4. NOAA Big Data Program, *NOAA Open Data Dissemination Program*,
   [https://github.com/NOAA-Big-Data-Program/bdp-data-docs][21], retrieved on
   2024.
5. Beginner’s Guide to GOES-R Series Data: How to acquire, analyze, and
   visualize GOES-R Series data, *Resources compiled by GOES-R Product Readiness
   and Operations*, Satellite Products and Services Division, National Oceanic
   and Atmospheric Administration.  [PDF][42]. Last Updated on May 23, 2024,
   retrieved on 2024.
6. GOES-R Series Data Book, *GOES-R Series Program Office*, Goddard Space
    Flight Center, National Aeronautics and Space Administration. [PDF][41],
    retrieved on 2024.

<!-- markdownlint-restore -->

<!-- hidden-references: named links -->

[0]: https://www.goes-r.gov/
[1]: https://www.goes-r.gov/mission/history.html
[2]: https://www.goes-r.gov/products/overview.html
[10]: https://www.ncei.noaa.gov/
[11]: https://registry.opendata.aws/noaa-goes/
[12]: https://docs.opendata.aws/noaa-goes16/cics-readme.html
[21]: https://github.com/NOAA-Big-Data-Program/bdp-data-docs
[22]: https://github.com/blaylockbk/goes2go
[23]: https://github.com/joaohenry23/GOES
[31]: https://goes2go.readthedocs.io/
[41]: https://www.goes-r.gov/downloads/resources/documents/GOES-RSeriesDataBook.pdf
[42]: https://www.goes-r.gov/downloads/resources/documents/Beginners_Guide_to_GOES-R_Series_Data.pdf
[51]: https://doi.org/10.7289/V5736P36
