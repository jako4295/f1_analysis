import polars as pl
import requests

from f1_analysis.data_structures._df_column_base import DataFrameColumnsBase
from f1_analysis.data_structures.api_datacls import Driver
from f1_analysis.data_structures.df_columns import (
    CarDataColumns,
    CarDF,
    LapDataColumns,
    LapDF,
    SessionDataColumns,
    SessionDF,
)


class OpenF1API:
    """API for requesting data from OpenF1 API.

    Parameters
    ----------
    base_url : str, optional
        Website to request data from. Could also work with localhosted api. Default
        https://api.openf1.org.
    """

    def __init__(self, base_url: str = "https://api.openf1.org") -> None:
        self.base_url = base_url
        self.session = requests.Session()

    def request(
        self,
        endpoint: str,
        parameters: dict[str, str] | dict[str, list[str]],
        method: str = "GET",
        version: str = "v1",
    ) -> requests.Response:
        """Request data from OpenF1.

        Parameters
        ----------
        endpoint : str
            Endpoints from https://openf1.org/docs/#api-endpoints. For example
            `sessions`
        parameters : Dict[str, str] | Dict[str, List[str]]
            Parameters for the endpoint. By default it will set key=val in dict but if
            the value starts with <, >, <=, >=, then this will be the matching instead.
            If you want to provide the same argument multiple times, then use
            `key=[arg1,arg2,...`.
        method : str, optional
            Method for requesting data through the requests library, by default "GET"
        version : str, optional
            Version of the API, by default "v1"

        Returns
        -------
        requests.Response
            Response from the api
        """
        _url = self.base_url if not self.base_url.endswith("/") else self.base_url[:-1]
        _ep = endpoint if not endpoint.startswith("/") else endpoint[1:]
        _ep = endpoint if not endpoint.endswith("/") else endpoint[:1]
        params = _fmt_params(parameters)

        url = f"{_url}/{version}/{_ep}{params}"
        res = self.session.request(method, url=url)

        res.raise_for_status()

        return res

    def get_session_data(
        self, year: int, session_type: str = "Qualifying"
    ) -> SessionDF:
        """Attribute for getting all sessions in a year (of a given session type).

        Parameters
        ----------
        year : int
            The year to get sessions from.
        session_type : str, optional
            The type for the session. By default "Qualifying"

        Returns
        -------
        SessionDF
            Session data info
        """
        parameters = {"year": f"{year}", "session_type": session_type}
        sessions_res = self.request("sessions", parameters)
        return _response2df(sessions_res, SessionDataColumns)

    def get_session_drivers(self, session_key: int) -> list[Driver]:
        """Get the drivers that are in the provided session.

        Parameters
        ----------
        session_key : int
            Key for the session.

        Returns
        -------
        List[Driver]
            List of drivers in the session provided
        """
        parameters = {"session_key": f"{session_key}"}
        drivers_req = self.request("drivers", parameters)
        drivers_json = drivers_req.json()

        return Driver.from_json_response(drivers_json)

    def get_session_car_data(self, session_key: int, driver_number: int) -> CarDF:
        """Car data per session and driver.

        It is ambiguous to import for all drivers and the call will fail - therefore
        `driver_number` must be specified. Use `self.get_session_drivers` to see the
        available drivers for a given session.

        Parameters
        ----------
        session_key : int
            Key for the session.
        driver_number : int
            Number of the driver to obtain data from

        Returns
        -------
        CarDF
            pl.DataFrame with requested car data. See `CarDataColumns` for columns and
            schema of the dataframe.
        """
        parameters = {
            "session_key": f"{session_key}",
            "driver_number": f"{driver_number}",
        }
        car_res = self.request("car_data", parameters)
        return _response2df(car_res, CarDataColumns)

    def get_lap_data(
        self, session_key: int, driver_number: int, is_pit_out_lap: bool = False
    ) -> LapDF:
        """Laps for a given driver at a given session.

        Parameters
        ----------
        session_key : int
            Key for the session.
        driver_number : int
            Number of the driver to obtain data from
        is_pit_out_lap : bool, optional
            If True the out laps will be included, otherwise excluded. Default False.

        Returns
        -------
        LapDF
            pl.DataFrame with requested car data. See `LapDataColumns` for columns and
            schema of the dataframe.
        """
        parameters = {
            "session_key": f"{session_key}",
            "driver_number": f"{driver_number}",
            "is_pit_out_lap": f"{is_pit_out_lap}".lower(),
        }
        lap_res = self.request("laps", parameters)
        return _response2df(lap_res, LapDataColumns)


def _fmt_params(parameters: dict[str, str] | dict[str, list[str]]) -> str:
    params = "?"
    for key, val in parameters.items():
        if isinstance(val, list):
            for _str in val:
                _fmt_params({key: _str})
        if not isinstance(val, str):
            raise ValueError("Unexpected parameter type")

        params += (
            f"{key}={val}&"
            if not val.startswith("<") or val.startswith(">")
            else f"{key}{val}&"
        )

    return params[:-1] if params.endswith("&") else params


def _response2df(
    response: requests.Response, df_columns: type[DataFrameColumnsBase]
) -> pl.DataFrame:
    json_response = response.json()
    _df = pl.DataFrame(json_response)

    df = pl.DataFrame(
        _df[df_columns.columns()],
        schema_overrides=df_columns.schema(),
    )
    return df_columns.validate(df)
