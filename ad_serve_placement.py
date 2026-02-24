import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def ad_serves(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    base_score = df["Name"].astype(str).str.split(" ").str[0]
    
    ad_scores = [
        "0-15",
        "0-40",
        "15-30",
        "15-0",
        "40-0",
        "40-30",
        "30-40",
        "30-15",
    ]

    is_ad_point = (df["Deuce"] == "Ad") | (base_score.isin(ad_scores))

    numerator = df[
        (df["Server"] == player_name) &
        (df["A2: 1st Serve Location"] == serve_location) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (base_score.isin(ad_scores))
    ]


    denominator = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (base_score.isin(ad_scores))
    ]

    return len(numerator) / len(denominator)


def ad_serves_win_pct(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    base_score = df["Name"].astype(str).str.split(" ").str[0]
    
    ad_scores = [
        "0-15",
        "0-40",
        "15-30",
        "15-0",
        "40-0",
        "40-30",
        "30-40",
        "30-15",
    ]


    is_ad_point = (df["Deuce"] == "Ad") | (base_score.isin(ad_scores))

    numerator = df[
        (df["Server"] == player_name) &
        (df["A2: 1st Serve Location"] == serve_location) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (df["C1: Who Won Point?"] == player_name) &
        (base_score.isin(ad_scores))
    ]


    denominator = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (df["A2: 1st Serve Location"] == serve_location) &
        (base_score.isin(ad_scores))
    ]

    return len(numerator) / len(denominator)

