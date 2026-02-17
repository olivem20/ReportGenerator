import pandas as pd
import streamlit as st

def winner_types(df: pd.DataFrame, player_name: str) -> float:
    winners = df[df["C1: Who Won Point?"] == player_name]
    
    return