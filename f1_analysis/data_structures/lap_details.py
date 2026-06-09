from dataclasses import dataclass
from datetime import datetime, timedelta

import polars as pl

from f1_analysis.data_structures.api_datacls import Driver
from f1_analysis.data_structures.df_columns import (
    CarDataColumns,
    CarDF,
    LapDataColumns,
    LapDF,
)


@dataclass
class LapDetails:
    """Details for a lap. Contains car data for a given lap."""

    lap_row: LapDF
    car_data: CarDF
    driver: Driver

    def __post_init__(self):
        """Check inputs to class satisfy condition."""
        self.lap_row = LapDataColumns.validate(self.lap_row)
        self.car_data = CarDataColumns.validate(self.car_data)
        if self.lap_row.height != 1:
            raise ValueError("Lap data should only contain one lap")
        if self.car_data[CarDataColumns.DATE].min() <= self.start_time:
            raise ValueError("Car data is not within the lap time")
        if self.car_data[CarDataColumns.DATE].max() >= self.end_time:
            raise ValueError("Car data is not within the lap time")

    @property
    def start_time(self) -> datetime:
        """Lap start time."""
        return self.lap_row[LapDataColumns.DATE_START].item()

    @property
    def end_time(self) -> datetime:
        """Lap end time."""
        return self.start_time + timedelta(seconds=self.lap_time)

    @property
    def lap_time(self) -> float:
        """Lap time in seconds."""
        return self.lap_row[LapDataColumns.LAP_DURATION].item()

    def normalized_lap_index(self) -> pl.Series:
        """Get index from 0 to 1 indicating the normalized lap."""
        lap_in_sec = self.car_data[CarDataColumns.DATE].map_elements(
            lambda _date: (_date - self.start_time).total_seconds()
        )
        return lap_in_sec / self.lap_time
