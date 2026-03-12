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
    
    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (is_ad_point)
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (is_ad_point)
        ]



    denominator = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == first_serve) &
        (is_ad_point)
    ]

    if len(denominator) == 0:
        return 0.0

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

    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["C1: Point Winner"] == player_name) &
            (is_ad_point)
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["C1: Point Winner"] == player_name) &
            (is_ad_point)
        ]


    if first_serve == "Yes":
        denominator = df[
            (df["Server"] == player_name) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (is_ad_point)
        ]
    else:
        denominator = df[
            (df["Server"] == player_name) &
            (df["A1: 1st Serve Made?"] == first_serve) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (is_ad_point)
        ]
    if len(denominator) == 0:
        return 0.0

    return len(numerator) / len(denominator)

