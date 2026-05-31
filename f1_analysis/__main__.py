from f1_analysis.data_manipulation.lap_data import (
    get_car_data_per_lap,
    get_fastest_laptime,
)
from f1_analysis.data_structures.df_columns import CarDataDF
from f1_analysis.openf1_api import OpenF1API


def main(year: int) -> None:
    """Run main module of ``f1_analysis``.

    Parameters
    ----------
    year : int
        Year to analyze

    Returns
    -------
    None
    """
    f1_api = OpenF1API()
    session_keys = f1_api.get_session_keys(year)

    # for now choose first key but switch to get_session_key when implemented
    session_key = session_keys[0]
    # session_key = get_session_key()

    drivers = f1_api.get_session_drivers(session_key)
    car_dat_per_driver: dict[int, CarDataDF] = {}
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
