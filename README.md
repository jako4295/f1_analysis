# F1 Analysis

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Analysis of OpenF1 API data.

The module shows an overview of results of the session specified. It will show the speed vs lap progress, throttle/brake vs lap progress, and gear trace vs lap progress. Below are the plots:

![speed](.img/speed_vs_lap_progress.png)
![throttle-brake](.img/throttle_brake.png)
![gear](.img/gear_trace_heatmap.png)

> [!NOTE]
> Note that there currently is a rate limit set by OpenF1, so there will be a 60 seconds timeout during the request of the data for this visualization.

## Installation

To install the package, first make sure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) (you can always check this using `uv --version`).

```bash
uv sync
```

## Usage

To run module code (at `f1_analysis/__main__.py`) use `uv run python -m f1_analysis`, and to see the input arguments use the `--help` flag.
