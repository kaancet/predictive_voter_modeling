import polars as pl


def drop_columns_that_are_all_null(
    _df: pl.DataFrame, verbose: bool = True
) -> pl.DataFrame:
    """Drops the columns that are all null"""
    keeping = []
    for s in _df:
        if s.null_count() == _df.height:
            if verbose:
                print(f"Dropping {s.name}, all null values")
        else:
            keeping.append(s.name)
    if verbose:
        print(
            f"\n!! Dropped {len(_df.columns)-len(keeping)} columns of {len(_df.columns)} columns!!"
        )

    return _df[keeping]


def convert_dates(
    _df: pl.DataFrame,
    dt_format: str = "%Y-%m-%d %H:%M",
    date_format: str = "%Y-%m-%d",
    verbose: bool = True,
) -> pl.DataFrame:
    """Converts the date string to datetime, creates a new dataframe"""
    df_date = _df.clone()
    for c in df_date.columns:
        if c == "First Conversion Date":
            pass
        try:
            df_date = df_date.with_columns(pl.col(c).str.to_datetime(dt_format))
            x = 5
        except:
            try:
                if verbose:
                    print(f"{c} -> Trying without time")
                df_date = df_date.with_columns(pl.col(c).str.to_datetime(date_format))
            except:
                if verbose:
                    print(f"column {c} can't be converted ")
        pass
    return df_date
