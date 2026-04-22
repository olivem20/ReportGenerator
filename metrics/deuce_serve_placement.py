import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def deuce_serves_count(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    
    deuce_scores = [
        "0-0",
        "0-30",
        "30-0",
        "15-15",
        "40-15",
        "15-40",
        "30-30",
    ]

    tb_parts = df["Tiebreaker Score"].fillna("").str.split("-", expand=True)
    is_tb_deuce = (
        tb_parts[0].ne("") &
        (((tb_parts[0].astype(int) + tb_parts[1].astype(int)) % 2) == 0)
    )

    is_deuce_point = (df["Deuce"] == "Deuce") | (df["Game Score"].isin(deuce_scores) | is_tb_deuce)  ###### DON"T FORGET TO deuceD TIE BREAKERS HERE
    
    if first_serve == "Yes":
        count = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (is_deuce_point)
        ]
    else:
        count = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (is_deuce_point)
        ]

    return len(count)


def deuce_serves_win_pct(df: pd.DataFrame, player_name: str, first_serve: str, serve_location: str) -> float:
    denominator = deuce_serves_count(df, player_name, first_serve, serve_location)
    
    deuce_scores = [
        "0-0",
        "0-30",
        "30-0",
        "15-15",
        "40-15",
        "15-40",
        "30-30",
    ]


    is_deuce_point = (df["Deuce"] == "Deuce") | (df["Game Score"].isin(deuce_scores))

    if first_serve == "Yes":
        numerator = df[
            (df["Server"] == player_name) &
            (df["A2: 1st Serve Location"] == serve_location) &
            (df["A1: 1st Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (is_deuce_point)
        ]
    else:
        numerator = df[
            (df["Server"] == player_name) &
            (df["A4: 2nd Serve Location"] == serve_location) &
            (df["A3: 2nd Serve Made?"] == "Yes") &
            (df["C1: Point Winner"] == player_name) &
            (is_deuce_point)
        ]

    if denominator == 0:
        return 0

    return len(numerator) / denominator

