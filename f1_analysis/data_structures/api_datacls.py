from dataclasses import dataclass
from typing import Self


@dataclass
class Driver:
    """Dataclass for import of driver data."""

    full_name: str
    team: str
    number: int

    @classmethod
    def from_json_response(
        cls, json_response: list[dict[str, str | int]]
    ) -> list[Self]:
        """Load drivers from a json api response (using the drivers endpoint).

        Parameters
        ----------
        json_response : List[Dict[str, str  |  int]]
            List of dictionaries on the format from https://openf1.org/docs/#drivers

        Returns
        -------
        List[Self]
            List of drivers.
        """
        drivers = []
        for dict_ in json_response:
            name = dict_.get("full_name", None)
            team = dict_.get("team_name", None)
            number = dict_.get("driver_number", None)

            if not (
                isinstance(name, str)
                and isinstance(team, str)
                and isinstance(number, int)
            ):
                continue

            drivers.append(cls(full_name=name, team=team, number=number))

        return drivers
