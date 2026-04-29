from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeAlias

import polars as pl

Schema: TypeAlias = dict[str, pl.DataType]


class DataFrameColumnsBase(ABC):
    """Base class for string-based dataframe column namespaces."""

    @classmethod
    def _column_names(cls) -> list[str]:
        """Return declared public column values in definition order.

        Returns
        -------
        List[str]
            Declared column values.
        """
        return [
            getattr(cls, name)
            for name in cls.__annotations__
            if not name.startswith("_")
        ]

    @classmethod
    @abstractmethod
    def _schema(cls) -> Schema:
        """Return the raw schema for the column namespace.

        Returns
        -------
        Schema
            Raw schema mapping from column name to Polars dtype.
        """

    @classmethod
    def schema(cls) -> Schema:
        """Validate and return the schema.

        Returns
        -------
        Schema
            Validated schema mapping.

        Raises
        ------
        TypeError
            If the schema is invalid.
        """
        schema: Schema = cls._schema()
        columns = cls._column_names()

        missing = sorted(set(columns) - set(schema))
        extra = sorted(set(schema) - set(columns))

        if missing or extra:
            parts: list[str] = []
            if missing:
                parts.append(f"missing columns in schema: {missing}")
            if extra:
                parts.append(f"extra schema keys: {extra}")
            raise TypeError(f"{cls.__name__}.schema() is invalid: {'; '.join(parts)}")

        return schema

    @classmethod
    def columns(cls) -> list[str]:
        """Return all declared columns.

        Returns
        -------
        List[str]
            Declared column values.
        """
        return cls._column_names()

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Validate concrete subclasses at class creation time.

        Parameters
        ----------
        **kwargs : object
            Extra subclass initialization arguments.
        """
        super().__init_subclass__(**kwargs)

        if cls.__dict__.get("__abstractmethods__"):
            return

        cls.schema()
