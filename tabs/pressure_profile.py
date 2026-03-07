import streamlit as st
import pandas as pd

def render_pressure_profile(df, player):
    st.header("Deuce Points")
    deuce_points = df[df["Deuce"].notna()].copy()

    deuce_points_played = len(deuce_points)

    deuce_points_won = len(
        deuce_points[deuce_points["C1: Who Won Point?"] == player]
    )

    win_pct = (deuce_points_won / deuce_points_played) * 100 if deuce_points_played > 0 else 0

    st.metric(
        "Deuce Points Won",
        f"{deuce_points_won}/{deuce_points_played} ({win_pct:.0f}%)"
    )

    st.header("Momentum")