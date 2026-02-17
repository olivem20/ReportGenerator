import pandas as pd

def return_percentage(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[df["Server"] == opponent_name]
    total_returns = len(returns)
    returns_won = returns["C1: Who Won Point?"].eq(player_name).sum()
    return returns_won / total_returns

def first_return_pct(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[
        (df["Server"] == opponent_name) &
        (df["A1: 1st Serve Made?"] == "Yes")
        ]

    total_returns = len(returns)
    returns_won = returns["C1: Who Won Point?"].eq(player_name).sum()
    return returns_won / total_returns

def second_return_pct(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[
        (df["Server"] == opponent_name) &
        (df["A1: 1st Serve Made?"] == "No")
        ]
    total_returns = len(returns)
    returns_won = returns["C1: Who Won Point?"].eq(player_name).sum()
    return returns_won / total_returns

def first_return_errors(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[
        (df["Server"] == opponent_name) &
        (df["B4: Return Outcome"] == "Error") &
        (df["A1: 1st Serve Made?"] == "Yes")
        ]
    return len(returns)

def second_return_errors(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[
        (df["Server"] == opponent_name) &
        (df["B4: Return Outcome"] == "Error") &
        (df["A1: 1st Serve Made?"] == "No")
        ]
    return len(returns)
