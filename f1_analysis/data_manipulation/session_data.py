import polars as pl

from f1_analysis.data_structures.df_columns import SessionDataColumns, SessionDF


def get_session_key(
    session_df: SessionDF,
    session_name: str = "Qualifying",
    key_name: str = SessionDataColumns.CIRCUIT_SHORT_NAME,
    matching_value: str = "Spa-Francorchamps",
) -> int:
    """Get a list of sessions and filter by keywords to extract just one session.

    ``key_name`` is a column of ``SessionDataColumns`` and ``matching_value`` is the
    value that will be looked for in that column.

    If there are multiple sessions with the provided filters, then the first one is
    chosen.

    Parameters
    ----------
    session_df : pl.DataFrame
        Sessions to select from
    session_nane : str
        Strictly matching of session name. Session type does not distinguish
        "Qualifying" and "Sprint Qualifying", but session_name does.
        Default "Qualifying"
    key_name : str, optional
        Key to look for in dataframe. Default SessionDataColumns.CIRCUIT_SHORT_NAME
    matching_value : str, optional
        Value to match against in the df of column key_name. Default "Spa-Francorchamps"

    Returns
    -------
    int
        session key given the filter arguments.
    """
    df = SessionDataColumns.validate(session_df)

    lower_case_col = pl.col(key_name).str.to_lowercase()
    lower_case_val = matching_value.lower()

    df_filtered = df.filter(lower_case_col.str.contains(lower_case_val)).filter(
        pl.col(SessionDataColumns.SESSION_NAME) == session_name
    )
    session_key = df_filtered[SessionDataColumns.SESSION_KEY].first()

    if not isinstance(session_key, int):
        raise ValueError("Unable to extract session_key from DataFrame")

    return session_key
