import pandas as pd

########## SERVING ##########
def first_serve_percentage(df: pd.DataFrame, player_name: str) -> float:
    serves = df[df["Server"] == player_name]
    total_first_serves = len(serves)
    first_serves_in = serves["A1: 1st Serve Made?"].eq("Yes").sum()
    return first_serves_in / total_first_serves

def first_serve_points_won(df: pd.DataFrame, player_name: str) -> float:
    serves = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "Yes")
    ]
    points_won = serves["C1: Who Won Point?"].eq(player_name).sum()
    total_first_serve_points = len(serves)
    return points_won / total_first_serve_points


def second_serve_points_won(df: pd.DataFrame, player_name: str) -> float:
    serves = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "No")
    ]
    points_won = serves["C1: Who Won Point?"].eq(player_name).sum()
    total_first_serve_points = len(serves)
    return points_won / total_first_serve_points

def num_double_faults(df: pd.DataFrame, player_name: str) -> float:
    serves = df[
        (df["Server"] == player_name) &
        (df["A3: 2nd Serve Made?"] == "No")
    ]
    return len(serves)

def num_aces(df: pd.DataFrame, player_name: str) -> float:
    serves = df[
        (df["Server"] == player_name) &
        (df["D3: Shot Winner"] == "Serve") &
        (df["D1: Winner Type"] == "Winner")
    ]
    return len(serves)

## SERVE PLACEMENENT FUNCTIONS ##

def deuce_wide(df: pd.DataFrame, player_name: str) -> float:
    base_score = df["Name"].str.split(" ").str[0]

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

    serves = base_score[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "Yes") &
        (df["A2: 1st Serve Location"] == "Wide") &
        (base_score.isin(deuce_scores))
    ]
    return int(len(serves))

def deuce_body(df: pd.DataFrame, player_name: str) -> float:
    return

def deuce_t(df: pd.DataFrame, player_name: str) -> float:
    return

def ad_wide(df: pd.DataFrame, player_name: str) -> float:
    return

def ad_body(df: pd.DataFrame, player_name: str) -> float:
    return

def ad_t(df: pd.DataFrame, player_name: str) -> float:
    return