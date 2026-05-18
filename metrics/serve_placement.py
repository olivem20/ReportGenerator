import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def serve_count(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str, side:str) -> float:
    if first_serve == "Yes":
        count = df[
            (df["Side"] == side) &
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location)
        ]
    else:
        count = df[
            (df["Side"] == side) &
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location)
        ]

    return len(count)


def serve_win_pct(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str, side:str) -> float:
    denominator = serve_count(df, player_name, first_serve, serve_location, side)
    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (df["Side"] == side)
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A3: 2nd Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (df["Side"] == side)
        ]

    if denominator == 0:
        return 0

    return len(numerator) / denominator

