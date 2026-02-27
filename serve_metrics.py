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
    total_second_serve_points = len(serves)
    return points_won / total_second_serve_points

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

def serve_points_won(df: pd.DataFrame, player_name: str) -> float:
    serves = df[df["Server"] == player_name]

    total_service_points = len(serves)
    if total_service_points == 0:
        return 0.0

    points_won = serves["C1: Who Won Point?"].eq(player_name).sum()

    return points_won / total_service_points

def service_games_held(df: pd.DataFrame, player_name: str) -> int:
    serves = df[df["Server"] == player_name]

    # Score BEFORE the point
    score = serves["Name"].astype(str).str.strip()

    holds = serves[
        score.str.startswith("40-") & 
        (serves["C1: Who Won Point?"] == player_name)
    ]
    return len(holds)

def service_games_broken(df: pd.DataFrame, player_name: str) -> int:
    serves = df[df["Server"] == player_name].copy()

    # Extract only the score portion before the space
    score = (
        serves["Name"]
        .astype(str)
        .str.strip()
        .str.split(" ")
        .str[0]
    )

    broken = serves[
        score.isin(["0-40", "15-40", "30-40", "40-40"]) &
        (serves["C1: Who Won Point?"] != player_name)
    ]

    return len(broken)

def break_points_faced(df: pd.DataFrame, player_name: str) -> int:
    serves = df[df["Server"] == player_name].copy()

    # Extract only the score portion before the space
    score = (
        serves["Name"]
        .astype(str)
        .str.strip()
        .str.split(" ")
        .str[0]
    )

    break_points = serves[
        score.isin(["0-40", "15-40", "30-40", "40-40"]) 
    ]

    return len(break_points)

def break_points_saved(df: pd.DataFrame, player_name: str) -> int:
    serves = df[df["Server"] == player_name].copy()

    # Extract only the score portion before the space
    score = (
        serves["Name"]
        .astype(str)
        .str.strip()
        .str.split(" ")
        .str[0]
    )

    break_points = serves[
        score.isin(["0-40", "15-40", "30-40", "40-40"]) &
        (serves["C1: Who Won Point?"] == player_name)
    ]

    return len(break_points)