import polars as pl


def get_session_key(
    session_df: pl.DataFrame, location: str | None = None, country: str | None = None
) -> int:
    """Get a list of sessions and filter by keywords to extract just one session.

    If there are multiple sessions with the provided filters, then the first one is
    chosen.

    Parameters
    ----------
    session_df : pl.DataFrame
        Sessions to select from
    location : str | None, optional
        Location like "Spa-Francorchamps". This will not be strictly compared, so 'spa'
        is sufficient to get this event. by default None
    country : str | None, optional
        Gets the event(s) in the given country, by default None

    Returns
    -------
    int
        session key given the filter arguments.
    """
    raise NotImplementedError("")
