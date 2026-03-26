import pandas as pd

deuce_scores = ["0-0", "15-15", "30-30", "30-0", "0-30", "40-15", "15-40", "40-40"]
ad_scores = ["0-15", "15-0", "30-15", "15-30", "40-30", "30-40", "40-0", "0-40", "40-40"]

def return_count(df: pd.DataFrame, player_name: str) -> int:
    returns = df[df["Server"] != player_name]
    return len(returns)

def return_percentage(df: pd.DataFrame, player_name: str) -> float:
    returns = df[df["Server"] != player_name]
    total_returns = len(returns)
    returns_won = returns["C1: Point Winner"].eq(player_name).sum()
    return returns_won / total_returns

def first_return_pct(df: pd.DataFrame, player_name: str) -> float:
    returns = df[
        (df["Server"] != player_name) &
        (df["A1: 1st Serve Made?"] == "Yes")
    ]

    total_returns = len(returns)
    returns_won = returns["C1: Point Winner"].eq(player_name).sum()
    return returns_won / total_returns


def deuce_return_count(df: pd.DataFrame, player_name: str, return_shot: str, return_direction: str) -> int:
    deuce_stroke = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["Game Score"].isin(deuce_scores)) &
        (
            (df["Deuce"] == "Deuce") |
            (df["Deuce"].isna()) | 
            (df["Deuce"] == "")
        )
    ]

    return len(deuce_stroke)

def deuce_return_win_pct(df: pd.DataFrame, player_name: str, return_shot: str, return_direction: str) -> float:
    numerator = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["C1: Point Winner"] == player_name) &
        (df["Game Score"].isin(deuce_scores)) &
        (
            (df["Deuce"] == "Deuce") |
            (df["Deuce"].isna()) | 
            (df["Deuce"] == "")
        )
    ]


    denominator = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["Game Score"].isin(deuce_scores)) &
        (
            (df["Deuce"] == "Deuce") |
            (df["Deuce"].isna()) | 
            (df["Deuce"] == "")
        )
    ]


    if len(denominator) == 0:
        return 0.0

    return len(numerator) / len(denominator)


def ad_return_count(df: pd.DataFrame, player_name: str, return_shot: str, return_direction: str) -> int:
    ad_stroke = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["Game Score"].isin(ad_scores)) &
        (
            (df["Deuce"] == "Ad") | 
            (df["Deuce"].isna())
        )
    ]


    return len(ad_stroke) 

def ad_return_win_pct(df: pd.DataFrame, player_name: str, return_shot: str, return_direction: str) -> float:
    numerator = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["C1: Point Winner"] == player_name) &
        (df["Game Score"].isin(ad_scores)) &
        (
            (df["Deuce"] == "Ad") |
            (df["Deuce"].isna()) | 
            (df["Deuce"] == "")
        )
    ]
    


    denominator = df[
        (df["Server"] != player_name) &
        (df["B1: Return Shot"] == return_shot) &
        (df["B3: Return Direction"] == return_direction) &
        (df["Game Score"].isin(ad_scores)) &
        (
            (df["Deuce"] == "Ad") | 
            (df["Deuce"].isna())
        )
    ]


    if len(denominator) == 0:
        return 0.0
        
    return len(numerator) / len(denominator)


def second_return_pct(df: pd.DataFrame, player_name: str) -> float:
    returns = df[
        (df["Server"] != player_name) &
        (df["A1: 1st Serve Made?"] == "No")
        ]
    total_returns = len(returns)
    returns_won = returns["C1: Point Winner"].eq(player_name).sum()
    return returns_won / total_returns

def first_return_errors(df: pd.DataFrame, player_name: str) -> int:
    return_errors = df[
        (df["Server"] != player_name) &
        (df["A1: 1st Serve Made?"] == "Yes") &
        (df["E2: Shot Error"].isin(["Forehand Return", "Backhand Return"]))
    ]
    return len(return_errors)


def second_return_errors(df: pd.DataFrame, player_name: str) -> int:
    return_errors = df[
        (df["Server"] != player_name) &
        (df["A1: 1st Serve Made?"] == "No") &
        (df["E2: Shot Error"].isin(["Forehand Return", "Backhand Return"]))
    ] 
    return len(return_errors)

def return_games_won(df: pd.DataFrame, player_name: str) -> int:
    break_scores = ["0-40", "15-40", "30-40", "40-40"]

    return_games = df[
        (df["Server"] != player_name) &
        (df["Game Score"].isin(break_scores)) & 
        (df["C1: Point Winner"] == player_name)
    ]
    return len(return_games)

def return_games_played(df: pd.DataFrame, player_name: str) -> int:
    return_games = df[
        (df["Server"] != player_name) &
        (df["Game Score"] == "0-0") 
    ]  
    
    return len(return_games)

def forced_errors_w_return(df: pd.DataFrame, player_name: str) -> int:
    returns = df[df["Server"] != player_name]
    forced = returns[
        (returns["D1: Winner Type"] == "Forcing Error") & 
        (df["D3: Shot Winner"].isin(["Forehand Return", "Backhand Return"]))
        ]
    return len(forced)

def return_winners(df: pd.DataFrame, player_name: str) -> int:
    returns = df[df["Server"] != player_name]
    winners = returns[
        (returns["D1: Winner Type"] == "Winner") & 
        (df["D3: Shot Winner"].isin(["Forehand Return", "Backhand Return"]))
        ]
    return len(winners)


