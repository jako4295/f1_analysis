import requests

from f1_analysis.data_structures.enums import OpenF1Versions


class OpenF1API:

    def __init__(self, base_url: str = "https://api.openf1.org"):
        self.base_url = base_url
        self.session = requests.Session()

    def request(
        self,
        endpoint: str,
        parameters: dict[str, str],
        method: str = "GET",
        version: OpenF1Versions = OpenF1Versions.V1,
    ) -> requests.Response:
        _url = self.base_url if not self.base_url.endswith("/") else self.base_url[:-1]
        _ep = endpoint if not endpoint.startswith("/") else endpoint[1:]
        _ep = endpoint if not endpoint.endswith("/") else endpoint[:1]

        url = f"{_url}/{version.value}/{_ep}"


if __name__ == "__main__":
    import json
    from urllib.request import urlopen

    response = urlopen(
        "https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315"
    )
    data = json.loads(response.read().decode("utf-8"))
    print(data)
