import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def deuce_serves(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    base_score = df["Name"].astype(str).str.split(" ").str[0]
    
    deuce_scores = [
        "0-0",
        "15-15",
        "30-30",
        "40-40",
        "30-0",
        "0-30",
        "40-15",
        "15-40"
    ]

    is_deuce_point = (df["Deuce"] == "Deuce") | (base_score.isin(deuce_scores))


    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (base_score.isin(deuce_scores))
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (base_score.isin(deuce_scores))
        ]




    denominator = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (base_score.isin(deuce_scores))
    ]

    if len(denominator) == 0:
        return 0.0

    return len(numerator) / len(denominator)


def deuce_serves_win_pct(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    base_score = df["Name"].astype(str).str.split(" ").str[0]
    
    deuce_scores = [
        "0-0",
        "15-15",
        "30-30",
        "40-40",
        "30-0",
        "0-30",
        "40-15",
        "15-40"
    ]


    is_deuce_point = (df["Deuce"] == "Deuce") | (base_score.isin(deuce_scores))

    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["C1: Who Won Point?"] == player_name) &
            (base_score.isin(deuce_scores))
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["C1: Who Won Point?"] == player_name) &
            (base_score.isin(deuce_scores))
        ]

    if first_serve == "Yes":
        denominator = df[
            (df["Server"] == player_name) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (base_score.isin(deuce_scores))
        ]
    else:
        denominator = df[
            (df["Server"] == player_name) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (base_score.isin(deuce_scores))
        ]

    if len(denominator) == 0:
        return 0.0
    
    return len(numerator) / len(denominator)

