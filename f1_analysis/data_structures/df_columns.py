from typing import Any, Final

import polars as pl

from f1_analysis.data_structures._df_column_base import DataFrameColumnsBase

type CarDataDF = pl.DataFrame
type LapDataDF = pl.DataFrame


class CarDataColumns(DataFrameColumnsBase):
    """DataFrame columns for data containing car data."""

    BRAKE: Final[str] = "brake"
    DATE: Final[str] = "date"
    DRIVER_NUMBER: Final[str] = "driver_number"
    DRS: Final[str] = "drs"
    MEETING_KEY: Final[str] = "meeting_key"
    N_GEAR: Final[str] = "n_gear"
    RPM: Final[str] = "rpm"
    SESSION_KEY: Final[str] = "session_key"
    SPEED: Final[str] = "speed"
    THROTTLE: Final[str] = "throttle"

    @classmethod
    def schema(cls) -> dict[str, Any]:
        """Validate DataFrame with car data with this attribute.

        Returns
        -------
        dict[str, Any]
            Schema for CarDataColumns
        """
        return {
            cls.DATE: pl.Datetime(time_unit="us", time_zone="UTC"),
            cls.BRAKE: pl.Int8,
            cls.DRIVER_NUMBER: pl.UInt8,
            cls.DRS: pl.UInt8,
            cls.MEETING_KEY: pl.Int32,
            cls.N_GEAR: pl.UInt8,
            cls.RPM: pl.Int32,
            cls.SESSION_KEY: pl.Int32,
            cls.SPEED: pl.UInt32,
            cls.THROTTLE: pl.Int8,
        }


class LapDataColumns(DataFrameColumnsBase):
    """DataFrame columns for data containing lap data."""

    DATE_START: Final[str] = "date_start"
    DRIVER_NUMBER: Final[str] = "driver_number"
    DURATION_SECTOR_1: Final[str] = "duration_sector_1"
    DURATION_SECTOR_2: Final[str] = "duration_sector_2"
    DURATION_SECTOR_3: Final[str] = "duration_sector_3"
    I1_SPEED: Final[str] = "i1_speed"
    I2_SPEED: Final[str] = "i2_speed"
    IS_PIT_OUT_LAP: Final[str] = "is_pit_out_lap"
    LAP_DURATION: Final[str] = "lap_duration"
    LAP_NUMBER: Final[str] = "lap_number"
    MEETING_KEY: Final[str] = "meeting_key"
    SEGMENTS_SECTOR_1: Final[str] = "segments_sector_1"
    SEGMENTS_SECTOR_2: Final[str] = "segments_sector_2"
    SEGMENTS_SECTOR_3: Final[str] = "segments_sector_3"
    SESSION_KEY: Final[str] = "session_key"
    ST_SPEED: Final[str] = "st_speed"

    @classmethod
    def schema(cls) -> dict[str, Any]:
        """Validate DataFrame with lap data with this attribute.

        Returns
        -------
        dict[str, Any]
            Schema for lap data
        """
        return {
            cls.DATE_START: pl.Datetime(time_unit="us", time_zone="UTC"),
            cls.DRIVER_NUMBER: pl.Int64,
            cls.DURATION_SECTOR_1: pl.Float64,
            cls.DURATION_SECTOR_2: pl.Float64,
            cls.DURATION_SECTOR_3: pl.Float64,
            cls.I1_SPEED: pl.Int64,
            cls.I2_SPEED: pl.Int64,
            cls.IS_PIT_OUT_LAP: pl.Boolean,
            cls.LAP_DURATION: pl.Float64,
            cls.LAP_NUMBER: pl.Int64,
            cls.MEETING_KEY: pl.Int64,
            cls.SEGMENTS_SECTOR_1: pl.List(pl.Int64),
            cls.SEGMENTS_SECTOR_2: pl.List(pl.Int64),
            cls.SEGMENTS_SECTOR_3: pl.List(pl.Int64),
            cls.SESSION_KEY: pl.Int64,
            cls.ST_SPEED: pl.Int64,
        }
