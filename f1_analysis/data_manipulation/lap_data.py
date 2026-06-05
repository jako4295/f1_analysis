from datetime import datetime, timedelta

import polars as pl

from f1_analysis.data_structures.df_columns import (
    CarDataColumns,
    CarDF,
    LapDataColumns,
    LapDF,
)


def get_fastest_laptime(df: LapDF) -> LapDF:
    """Get fastest lap time of lap df.

    Parameters
    ----------
    df : LapDF
        Dataframe with columns from ``LapDataColumns``

    Returns
    -------
    LapDF
        Column with lowest lap time
    """
    df = df.drop_nulls()  # remove laps with not finished sectors etc.
    df = LapDataColumns.validate(df)

    arg_min_duration = df[LapDataColumns.LAP_DURATION].arg_min()

    if arg_min_duration is None:
        return pl.DataFrame(schema=LapDataColumns.schema())

    return df.slice(arg_min_duration, 1)


def get_car_data_per_lap(lap_df: LapDF, car_data_df: CarDF) -> CarDF:
    """Get car data for a given lap.

    Parameters
    ----------
    lap_df : LapDF
        Only one row of lap data (meaning only containing one lap)
    car_data_df : CarDF
        Car data for a given race.

    Returns
    -------
    CarDF
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
