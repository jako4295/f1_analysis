from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from f1_analysis.data_structures.df_columns import CarDataColumns
from f1_analysis.data_structures.lap_details import LapDetails

plt.style.use("bmh")


def plot_speed_vs_lap_progress(
    lap_details: list[LapDetails], output_folder: Path
) -> None:
    """Speed vs lap progress plot for each driver in one figure.

    Parameters
    ----------
    lap_details : list[LapDetails]
        Information about a given lap.
    output_folder : Path
        Path to the folder where figure will be saved.
    """
    # Fastest lap at top
    laps = sorted(lap_details, key=lambda lap: lap.lap_time)

    n_bins = 200

    heatmap_rows = []
    y_labels = []

    for lap in laps:
        x = lap.normalized_lap_index().to_numpy()

        speed = lap.car_data[CarDataColumns.SPEED].cast(pl.Float64).to_numpy()

        grid = np.linspace(0.0, 1.0, n_bins)

        row = np.interp(grid, x, speed)

        heatmap_rows.append(row)

        y_labels.append(f"{lap.driver.full_name} ({lap.lap_time:.3f}s)")

    heatmap = np.vstack(heatmap_rows)

    _fig, ax = plt.subplots(figsize=(14, 8))

    im = ax.imshow(
        heatmap,
        aspect="auto",
        origin="upper",
        interpolation="nearest",
        extent=(0.0, 100.0, float(len(lap_details)), 0.0),
        cmap="turbo",
    )

    ax.set_xlabel("Lap Progress (%)")
    ax.set_ylabel("Driver")

    ax.set_yticks(np.arange(len(y_labels)) + 0.5)
    ax.set_yticklabels(y_labels)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Speed (km/h)")

    plt.tight_layout()
    plt.savefig(output_folder / "speed_vs_lap_progress.png")
    plt.close()


def plot_throttle_brake_heatmap(
    lap_details: list[LapDetails], output_folder: Path
) -> None:
    """Heatmap plot of throttle and brake over time.

    x-axis is the time in percent, y-axis is the drivers, and the color indicate the
    speed (and one plot similar for brake).

    Parameters
    ----------
    lap_details : list[LapDetails]
        Information about a given lap.
    output_folder : Path
        Path to the folder where figure will be saved.
    """
    lap_details = sorted(
        lap_details,
        key=lambda lap: lap.lap_time,
    )

    n_bins = 100
    grid = np.linspace(0.0, 1.0, n_bins)

    throttle_rows = []
    brake_rows = []
    labels = []

    for lap in lap_details:
        x = lap.normalized_lap_index().to_numpy()

        throttle = lap.car_data[CarDataColumns.THROTTLE].cast(pl.Float64).to_numpy()

        brake = lap.car_data[CarDataColumns.BRAKE].cast(pl.Float64).to_numpy()

        throttle_rows.append(np.interp(grid, x, throttle))

        brake_rows.append(np.interp(grid, x, brake))

        labels.append(f"{lap.driver.full_name} " f"({lap.lap_time:.3f}s)")

    throttle_matrix = np.asarray(throttle_rows)
    brake_matrix = np.asarray(brake_rows)

    _fig, (ax1, ax2) = plt.subplots(
        nrows=2,
        figsize=(14, 10),
        sharex=True,
        sharey=True,
        height_ratios=[2, 1],
    )

    throttle_im = ax1.imshow(
        throttle_matrix,
        aspect="auto",
        origin="upper",
        interpolation="nearest",
        extent=(0.0, 100.0, float(len(labels)), 0.0),
        vmin=0,
        vmax=100,
    )

    brake_im = ax2.imshow(
        brake_matrix,
        aspect="auto",
        origin="upper",
        interpolation="nearest",
        extent=(0.0, 100.0, float(len(labels)), 0.0),
        vmin=0,
        vmax=100,
    )

    ax1.set_title("Throttle (%)")
    ax2.set_title("Brake")

    yticks = np.arange(len(labels)) + 0.5

    ax1.set_yticks(yticks)
    ax1.set_yticklabels(labels)

    ax2.set_yticks(yticks)
    ax2.set_yticklabels(labels)

    ax2.set_xlabel("Lap Progress (%)")

    plt.colorbar(
        throttle_im,
        ax=ax1,
        label="Throttle (%)",
    )

    plt.colorbar(
        brake_im,
        ax=ax2,
        label="Brake",
    )

    plt.tight_layout()
    plt.savefig(output_folder / "throttle_brake.png")
    plt.close()


def plot_gear_trace_heatmap(lap_details: list[LapDetails], output_folder: Path) -> None:
    """Gear trace plot.

    Gear means: Current gear selection, ranging from 1 to 8. 0 indicates neutral or no
    gear engaged.

    Parameters
    ----------
    lap_details : list[LapDetails]
        Information about a given lap.
    output_folder : Path
        Path to the folder where figure will be saved.
    """
    lap_details = sorted(
        lap_details,
        key=lambda lap: lap.lap_time,
    )

    n_bins = 200
    grid = np.linspace(0.0, 1.0, n_bins)

    gear_rows = []
    labels = []

    for lap in lap_details:
        x = lap.normalized_lap_index().to_numpy()

        gear = lap.car_data[CarDataColumns.N_GEAR].cast(pl.Float64).to_numpy()

        # nearest-neighbor interpolation is better than linear
        idx = np.searchsorted(x, grid, side="left")
        idx = np.clip(idx, 0, len(gear) - 1)

        gear_rows.append(gear[idx])

        labels.append(f"{lap.driver.full_name} " f"({lap.lap_time:.3f}s)")

    gear_matrix = np.asarray(gear_rows)

    _fig, ax = plt.subplots(figsize=(14, 8))

    im = ax.imshow(
        gear_matrix,
        aspect="auto",
        origin="upper",
        interpolation="nearest",
        extent=(0.0, 100.0, float(len(labels)), 0.0),
        vmin=0,
        vmax=8,
    )

    ax.set_xlabel("Lap Progress (%)")
    ax.set_ylabel("Driver")
    ax.set_title("Gear Trace")

    yticks = np.arange(len(labels)) + 0.5

    ax.set_yticks(yticks)
    ax.set_yticklabels(labels)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Gear")

    cbar.set_ticks(range(9))

    plt.tight_layout()
    plt.savefig(output_folder / "gear_trace_heatmap.png")
    plt.close()
