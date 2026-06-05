import argparse

from f1_analysis.data_manipulation.lap_data import (
    get_car_data_per_lap,
    get_fastest_laptime,
)
from f1_analysis.data_manipulation.session_data import get_session_key
from f1_analysis.data_structures.df_columns import CarDF, SessionDataColumns
from f1_analysis.openf1_api import OpenF1API
from f1_analysis.visualization.lap_visualizer import (
    plot_brake_heatmap,
    plot_gear_trace,
    plot_speed_vs_lap_progress,
    plot_throttle_heatmap,
)


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
        [api](https://openf1.org/docs/#sessions) for documentation. Default 'Qualifying'
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

    plot_speed_vs_lap_progress()
    plot_throttle_heatmap()
    plot_brake_heatmap()
    plot_gear_trace()


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments for f1 arguments.

    Returns
    -------
    argparse.Namespace
        Namespace with f1 relevant args.
    """
    parser = argparse.ArgumentParser(
        description="Arguments for what data to be analyzed in the f1_analysis. "
        "It will only analyze one meeting within a session."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2023,
        help="Year to search for a session in.",
    )
    parser.add_argument(
        "--session_name",
        type=str,
        default="Qualifying",
        help="Session name to search within.",
    )
    parser.add_argument(
        "--session_attribute",
        type=str,
        default=SessionDataColumns.CIRCUIT_SHORT_NAME,
        help="Select one attribute of the sessions endpoint in "
        "https://openf1.org/docs/#sessions to match a session_value against",
    )
    parser.add_argument(
        "--session_value",
        type=str,
        default="Spa-Francorchamps",
        help="Value to match against to find a given race session. Looks in the "
        "session_attribute for this keyword. It is a contains-like comparison of names"
        "and the name does therefore not need to be exact.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # TODO: create visualization module to show percentage of track done vs car details
    #       parameter
    #           - Resample times to 0-100%
    #           - Plot:
    #               - Speed vs lap progress (main chart)
    #               - Throttle heatmap
    #               - Brake heatmap
    #               - Gear trace
    args = _parse_args()
    main(**vars(args))
