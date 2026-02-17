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

def return_errors(df: pd.DataFrame, player_name: str, opponent_name: str) -> float:
    returns = df[
        (df["Server"] == opponent_name) &
        (df["B4: Return Outcome"] == "Error")
        ]
    return len(returns)

def return_direction_usage(df: pd.DataFrame, player_name: str) -> pd.Series:
    returns = df[df["Returner"] == player_name]

    usage = (
        returns["B3: Returm Direction"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts(normalize=True)
    )

    return usage


def return_direction_win_pct(df: pd.DataFrame, player_name: str) -> pd.Series:
    returns = df[
        (df["Returner"] == player_name) &
        (df["B3: Returm Direction"].notna())
    ].copy()

    returns["won"] = returns["C1: Who Won Point?"].astype(str).str.strip().eq(player_name)

    win_pct = (
        returns
        .groupby(returns["B3: Returm Direction"].astype(str).str.strip())["won"]
        .mean()
    )

    return win_pct
