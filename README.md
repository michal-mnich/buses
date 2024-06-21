# Buses - Analyze bus traffic in Warsaw

## Get started

### Installing

```bash
git clone https://github.com/michal-mnich/buses
cd buses
pip install .

```

### Usage

This package provides two scripts: `run-scraper` and `run-analyzer`.
They manage all of the package's functionality
For specific options, run them with flag `--help`

### Development

This package uses Poetry as the main packaging/build tool.
Its configuration is in the `pyproject.toml` file.
After changing the source code, you need to rebuild the distribution and
reinstall the package by issuing:

```bash
poetry build && pip install .
```

For additional info, refer to the Poetry documentation.
