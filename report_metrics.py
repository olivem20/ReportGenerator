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

def second_serve_points_won(df: pd.DataFrame, player_name: str) -> float:
    return


