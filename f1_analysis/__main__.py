from f1_analysis.data_handler.openf1_api import OpenF1API


def main(year: int) -> None:
    f1_api = OpenF1API()
    session_keys = f1_api.get_session_keys(year)

    for session_key in session_keys:
        drivers = f1_api.get_session_drivers(session_key)
        for driver in drivers:
            car_data = f1_api.get_session_car_data(session_key, driver.number)
            break
        break


if __name__ == "__main__":
    # TODO: Make argparse or Hydra config
    year = 2023
    main(year)
