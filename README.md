# GOES-DR — GOES Satellite Imagery Dataset Reader

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
