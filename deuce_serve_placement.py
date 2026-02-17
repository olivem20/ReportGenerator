import pandas as pd
## SERVE PLACEMENENT FUNCTIONS ##

def deuce_wide(df: pd.DataFrame, player_name: str) -> float:
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

    first_serves = df[
        (df["Server"] == player_name) &
        (base_score.isin(deuce_scores))
    ]

    first_serves_wide = df[
        (df["Server"] == player_name) &
        (df["A2: 1st Serve Location"] == "Wide") &
        (base_score.isin(deuce_scores))
    ]

    return len(first_serves_wide) / len(first_serves)

def deuce_body(df: pd.DataFrame, player_name: str) -> float:
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

    first_serves = df[
        (df["Server"] == player_name) &
        (base_score.isin(deuce_scores))
    ]

    first_serves_body = df[
        (df["Server"] == player_name) &
        (df["A2: 1st Serve Location"] == "Body") &
        (base_score.isin(deuce_scores))
    ]

    return len(first_serves_body) / len(first_serves)

def deuce_t(df: pd.DataFrame, player_name: str) -> float:
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

    first_serves = df[
        (df["Server"] == player_name) &
        (base_score.isin(deuce_scores))
    ]

    first_serves_t = df[
        (df["Server"] == player_name) &
        (df["A2: 1st Serve Location"] == "T") &
        (base_score.isin(deuce_scores))
    ]

    return len(first_serves_t) / len(first_serves)

def ad_wide(df: pd.DataFrame, player_name: str) -> float:
    return

def ad_body(df: pd.DataFrame, player_name: str) -> float:
    return

def ad_t(df: pd.DataFrame, player_name: str) -> float:
    return


################## WIN PCT ##################

def deuce_body_win_pct(df: pd.DataFrame, player_name: str) -> float:
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

    serves_body = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "Yes") &
        (df["A2: 1st Serve Location"] == "Body") &
        (base_score.isin(deuce_scores))
    ]

    total = len(serves_body)
    if total == 0:
        return 0.0

    won = serves_body["C1: Who Won Point?"].eq(player_name).sum()

    return won / total

def deuce_t_win_pct(df: pd.DataFrame, player_name: str) -> float:
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

    serves_body = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "Yes") &
        (df["A2: 1st Serve Location"] == "T") &
        (base_score.isin(deuce_scores))
    ]

    total = len(serves_body)
    if total == 0:
        return 0.0

    won = serves_body["C1: Who Won Point?"].eq(player_name).sum()

    return won / total

def deuce_wide_win_pct(df: pd.DataFrame, player_name: str) -> float:
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

    serves_body = df[
        (df["Server"] == player_name) &
        (df["A1: 1st Serve Made?"] == "Yes") &
        (df["A2: 1st Serve Location"] == "Wide") &
        (base_score.isin(deuce_scores))
    ]

    total = len(serves_body)
    if total == 0:
        return 0.0

    won = serves_body["C1: Who Won Point?"].eq(player_name).sum()

    return won / total