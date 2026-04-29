from typing import Dict, List

import requests

from f1_analysis.data_structures.enums import OpenF1Versions


class OpenF1API:
    def __init__(self, base_url: str = "https://api.openf1.org"):
        self.base_url = base_url
        self.session = requests.Session()

    def request(
        self,
        endpoint: str,
        parameters: Dict[str, str] | Dict[str, List[str]],
        method: str = "GET",
        version: OpenF1Versions = OpenF1Versions.V1,
    ) -> requests.Response:
        _url = self.base_url if not self.base_url.endswith("/") else self.base_url[:-1]
        _ep = endpoint if not endpoint.startswith("/") else endpoint[1:]
        _ep = endpoint if not endpoint.endswith("/") else endpoint[:1]
        params = _fmt_params(parameters)

        url = f"{_url}/{version.value}/{_ep}{params}"
        res = self.session.request(method, url=url)

        res.raise_for_status()

        return res


def _fmt_params(parameters: Dict[str, str] | Dict[str, List[str]]) -> str:
    params = "?"
    for key, val in parameters.items():
        if isinstance(val, list):
            for _str in val:
                _fmt_params({key: _str})
        if not isinstance(val, str):
            raise ValueError("Unexpected parameter type")

        params += (
            f"{key}={val}" if not val.startswith("<") or val.startswith(">") else val
        )

    return params


if __name__ == "__main__":
    endpoint = "session"
    parameters = {"year": "2023", "session_type": "Qualifying"}

    f1_api = OpenF1API()
    qual_events = f1_api.request(endpoint, parameters)
