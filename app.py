import streamlit as st
import pandas as pd
from serve_metrics import first_serve_percentage, first_serve_points_won, second_serve_points_won, num_double_faults, num_aces

st.title("Report Generator")

uploaded_file = st.file_uploader("Please upload Match CSV")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    #st.write(df)

    ### EXTRACT NOTES ###
    match_info = df.iloc[0]

    final_score = match_info["Final Score"]
    player = match_info["Player"]
    opponent = match_info["Opponent"]
    opponent_school = match_info["Opponent School"]
    location = match_info["Location"]
    date = match_info["Date"]

    # Match Winner
    winner_col = "C1: Who Won Point?"
    match_winner = df[winner_col].dropna().iloc[-1]

    ### WRITE INFO ###
    st.title(f"Match Winner: {match_winner}")
    st.subheader(f"**Final Score:** {final_score}")

    st.write(f"**Player:** {player}")
    st.write(f"**Opponent:** {opponent}")
    st.write(f"**Opponent School:** {opponent_school}")
    st.write(f"**Location:** {location}")
    st.write(f"**Date:** {date}")

    ########### PLAYER DATA ###########

    # Serving Profile
    st.header("Serving Profile")
    fs_pct = first_serve_percentage(df, player)
    st.write(f"1st Serve Percentage: {fs_pct:.1%}")
    
    fs_points_won = first_serve_points_won(df, player)
    st.write(f"1st Serve Points Won: {fs_points_won:.1%}")

    ss_points_won = second_serve_points_won(df, player)
    st.write(f"2nd Serve Points Won: {ss_points_won:.1%}")

    # Double Faults and Aces
    double_faults = num_double_faults(df, player)
    aces = num_aces(df, player)
    st.write(f"Double Faults: {double_faults}")
    st.write(f"Aces: {aces}")

    # Returning Profile

    # Winner Profile

    # Error Profile

    # Pressure Points Profile

