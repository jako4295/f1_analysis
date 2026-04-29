from typing import TypeAlias

import polars as pl

from f1_analysis.data_structures._df_column_base import DataFrameColumnsBase

CarDataDF: TypeAlias = pl.DataFrame


class CarDataColumns(DataFrameColumnsBase):
    BRAKE = "brake"
    DATE = "date"
    DRIVER_NUMBER = "driver_number"
    DRS = "drs"
    MEETING_KEY = "meeting_key"
    N_GEAR = "n_gear"
    RPM = "rpm"
    SESSION_KEY = "session_key"
    SPEED = "speed"
    THROTTLE = "throttle"

    @classmethod
    def schema(cls):
        return {
            cls.BRAKE: pl.Int8,
            cls.DATE: pl.Datetime(time_unit="us", time_zone="UTC"),
            cls.DRIVER_NUMBER: pl.UInt8,
            cls.DRS: pl.UInt8,
            cls.MEETING_KEY: pl.Int32,
            cls.N_GEAR: pl.UInt8,
            cls.RPM: pl.Int32,
            cls.SESSION_KEY: pl.Int32,
            cls.SPEED: pl.UInt32,
            cls.THROTTLE: pl.Int8,
        }
