from datetime import datetime, timedelta

import polars as pl

from f1_analysis.data_structures.df_columns import (
    CarDataColumns,
    CarDataDF,
    LapDataColumns,
    LapDataDF,
)


def get_fastest_laptime(df: LapDataDF) -> LapDataDF:
    """Get fastest lap time of lap df.

    Parameters
    ----------
    df : LapDataDF
        Dataframe with columns from ``LapDataColumns``

    Returns
    -------
    LapDataDF
        Column with lowest lap time
    """
    duration_col = LapDataColumns.LAP_DURATION
    if duration_col not in df.columns:
        raise ValueError("DataFrame must contain column 'lap_duration'")
    arg_min_duration = df[duration_col].arg_min()

    if arg_min_duration is None:
        return pl.DataFrame(schema=df.schema)

    return df.slice(arg_min_duration, 1)


def get_car_data_per_lap(lap_df: LapDataDF, car_data_df: CarDataDF) -> CarDataDF:
    """Get car data for a given lap.

    Parameters
    ----------
    lap_df : LapDataDF
        Only one row of lap data (meaning only containing one lap)
    car_data_df : CarDataDF
        Car data for a given race.

    Returns
    -------
    CarDataDF
        Car data for a given lap
    """
    if lap_df.height != 1:
        raise ValueError(
            "Multiple laps were provided, this method can only handle single laps"
        )

    lap_start: datetime = lap_df.select(pl.col(LapDataColumns.DATE_START)).item()
    duration: float = lap_df.select(pl.col(LapDataColumns.LAP_DURATION)).item()
    lap_end = lap_start + timedelta(seconds=duration)

    return car_data_df.filter(
        (pl.col(CarDataColumns.DATE) > lap_start)
        & (pl.col(CarDataColumns.DATE) < lap_end)
    )
