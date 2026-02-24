import pandas as pd
import altair as alt

########## SERVING ##########
def first_serve_percentage(df: pd.DataFrame, player_name: str) -> float:
    serves = df[df["Server"] == player_name]
    total_first_serves = len(serves)
    first_serves_in = serves["A1: 1st Serve Made?"].eq("Yes").sum()
    return first_serves_in / total_first_serves

def second_serve_percentage(df: pd.DataFrame, player_name: str) -> float:
    # Filter for this player's service points
    serves = df[df["Server"] == player_name]
    # A second serve happens when the first serve was missed
    second_serves_attempted = serves[serves["A1: 1st Serve Made?"] == "No"]
    # Second serves made
    second_serves_made = second_serves_attempted[
        second_serves_attempted["A3: 2nd Serve Made?"] == "Yes"
    ]
    total_attempted = len(second_serves_attempted)
    if total_attempted == 0:
        return 0.0  # prevents ZeroDivisionError

    return len(second_serves_made) / total_attempted

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

def service_winners(df: pd.DataFrame, player_name: str) -> float:
    serves = df[
        (df["Server"] == player_name) &
        (df["D3: Shot Winner"] == "Serve") &
        (df["D1: Winner Type"] == "Forced Error")
    ]
    return len(serves)
