from typing import Dict, List

import polars as pl
import requests

from f1_analysis.data_structures.api_datacls import Driver
from f1_analysis.data_structures.df_columns import CarDataColumns, CarDataDF
from f1_analysis.data_structures.enums import OpenF1Versions


class OpenF1API:
    """
    API for requesting data from OpenF1 API

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
        parameters: Dict[str, str] | Dict[str, List[str]],
        method: str = "GET",
        version: OpenF1Versions = OpenF1Versions.V1,
    ) -> requests.Response:
        """Request data from OpenF1

        Parameters
        ----------
        endpoint : str
            Endpoints from https://openf1.org/docs/#api-endpoints. For example `sessions`
        parameters : Dict[str, str] | Dict[str, List[str]]
            Parameters for the endpoint. By default it will set key=val in dict but if the value
            starts with <, >, <=, >=, then this will be the matching instead. If you want to provide
            the same argument multiple times, then use `key=[arg1,arg2,...`.
        method : str, optional
            Method for requesting data through the requests library, by default "GET"
        version : OpenF1Versions, optional
            Version of the API, by default OpenF1Versions.V1

        Returns
        -------
        requests.Response
            Response from the api
        """
        _url = self.base_url if not self.base_url.endswith("/") else self.base_url[:-1]
        _ep = endpoint if not endpoint.startswith("/") else endpoint[1:]
        _ep = endpoint if not endpoint.endswith("/") else endpoint[:1]
        params = _fmt_params(parameters)

        url = f"{_url}/{version.value}/{_ep}{params}"
        res = self.session.request(method, url=url)

        res.raise_for_status()

        return res

    def get_session_keys(
        self, year: int, session_type: str = "Qualifying"
    ) -> List[int]:
        """Method for getting all sessions in a year (of a given session type).

        Parameters
        ----------
        year : int
            The year to get sessions from.
        session_type : str, optional
            The type for the session. By default "Qualifying"

        Returns
        -------
        List[int]
            List of session keys.
        """
        parameters = {"year": f"{year}", "session_type": session_type}
        sessions_req = self.request("sessions", parameters)
        sessions_json = sessions_req.json()

        session_keys = []
        for session in sessions_json:
            session_key = session.get("session_key", None)
            if session_key is None:
                continue

            session_keys.append(session_key)

        return session_keys

    def get_session_drivers(self, session_key: int) -> List[Driver]:
        """Get the drivers that are in the provided session

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

    def get_session_car_data(self, session_key: int, driver_number: int) -> CarDataDF:
        """Car data per session and driver. It is ambiguous to import for all drivers and the call
        will fail - therefore `driver_numbe` must be specified. Use `self.get_session_drivers` to
        see the available drivers for a given session.

        Parameters
        ----------
        session_key : int
            Key for the session.
        driver_number : int
            Number of the driver to obtain data from

        Returns
        -------
        CarDataDF
            pl.DataFrame with requested car data. See `CarDataColumns` for columns and schema of the
            dataframe.
        """
        parameters = {
            "session_key": f"{session_key}",
            "driver_number": f"{driver_number}",
        }
        car_req = self.request("car_data", parameters)
        car_json = car_req.json()
        _df = pl.DataFrame(car_json)

        return pl.DataFrame(_df, schema=CarDataColumns.schema())


def _fmt_params(parameters: Dict[str, str] | Dict[str, List[str]]) -> str:
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
