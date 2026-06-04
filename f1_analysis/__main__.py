from f1_analysis.data_manipulation.lap_data import (
    get_car_data_per_lap,
    get_fastest_laptime,
)
from f1_analysis.data_manipulation.session_data import get_session_key
from f1_analysis.data_structures.df_columns import CarDF, SessionDataColumns
from f1_analysis.openf1_api import OpenF1API


def main(
    year: int,
    session_name: str = "Qualifying",
    session_attribute: str = SessionDataColumns.CIRCUIT_SHORT_NAME,
    session_value: str = "Spa-Francorchamps",
) -> None:
    """Run main module of ``f1_analysis``.

    Parameters
    ----------
    year : int
        Year to analyze
    session_name : str
        The type of session (more specific than session_type). See
        [api](https://openf1.org/docs/#sessions) for documentation.
    session_attribute : str
        Attribute from the sessions endpoint to match session_value against. Default is
        SessionDataColumns.CIRCUIT_SHORT_NAME
    session_value : str
        Value to match a column against. Default "Spa-Francorchamps"

    Returns
    -------
    None
    """
    f1_api = OpenF1API()
    session_df = f1_api.get_session_data(year)

    # for now choose first key but switch to get_session_key when implemented
    session_key = get_session_key(
        session_df,
        session_name=session_name,
        key_name=session_attribute,
        matching_value=session_value,
    )

    drivers = f1_api.get_session_drivers(session_key)
    car_dat_per_driver: dict[int, CarDF] = {}
    for driver in drivers:
        car_data = f1_api.get_session_car_data(session_key, driver.number)
        laps = f1_api.get_lap_data(session_key, driver.number)

        fastest_lap = get_fastest_laptime(laps)
        car_data_per_lap = get_car_data_per_lap(fastest_lap, car_data)
        car_dat_per_driver[driver.number] = car_data_per_lap

    # TODO: Visualize data


if __name__ == "__main__":
    # TODO: Make argparse or Hydra config
    # TODO: Match against 'location' in session (for instance 'spa')
    # TODO: Match against 'session_type': Practice, (sprint) Qualifying, Race

    # TODO: Move to using pydantic basemodel for easier validating data

    # TODO: create visualization module to show percentage of track done vs car details
    #       parameter
    #           - Resample times to 0-100%
    #           - Plot:
    #               - Speed vs lap progress (main chart)
    #               - Throttle heatmap
    #               - Brake heatmap
    #               - Gear trace
    year = 2023
    main(year)
