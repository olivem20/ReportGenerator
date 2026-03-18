import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def ad_serves_count(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    
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

    is_ad_point = (df["Deuce"] == "Ad") | (df["Game Score"].isin(ad_scores))  ###### DON"T FORGET TO ADD TIE BREAKERS HERE
    
    if first_serve == "Yes":
        count = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (is_ad_point)
        ]
    else:
        count = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (is_ad_point)
        ]

    return len(count)


def ad_serves_win_pct(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    denominator = ad_serves_count(df, player_name, first_serve, serve_location)
    
    ad_scores = [
        "0-15",
        "15-0",
        "0-40",
        "40-0",
        "15-30",
        "30-15",
        "40-30",
        "30-40"
    ]


    is_ad_point = (df["Deuce"] == "Ad") | (df["Game Score"].isin(ad_scores))

    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (is_ad_point)
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A3: 2nd Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (is_ad_point)
        ]

    if denominator == 0:
        return 0

    return len(numerator) / denominator

