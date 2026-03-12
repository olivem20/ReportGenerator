import os
import streamlit as st
import pandas as pd

from tabs.serve_profile import render_serve_profile
from tabs.return_profile import render_return_profile
from tabs.winners_profile import render_winners_profile
from tabs.errors_profile import render_errors_profile
from tabs.pressure_profile import render_pressure_profile
from tabs.opponent_profile import render_opponent_profile

st.title("Report Generator")

uploaded_file = st.file_uploader("Please upload Match CSV")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    #st.write(df)

    ### EXTRACT NOTES ###
    match_info = df.iloc[0]

    final_score = match_info["Final Score"]
    player = match_info["Player Name"]
    opponent = match_info["Opponent Name"]
    opponent_school = match_info["Opponent School"]
    location = match_info["Location"]
    date = match_info["Date"]
    singles_line = match_info["Singles Line"]
    overall_score = match_info["Overall Score"]
   
    player_first_name = player.split()[0]
    player_png = f"{player_first_name}.png"
    image_path = os.path.join("Headshots", player_png) 

    opponent_png = f"{opponent_school}.png"
    opponent_image_path = os.path.join("School Logos", opponent_png)


    # Match Winner  
    winner_col = "C1: Point Winner" 
    match_winner = df[winner_col].dropna().iloc[-1]

    # Extract Win Data
    is_win = str(match_winner).strip().lower() == str(player).strip().lower()

    bubble_color = "#22c55e" if is_win else "#ef4444"   # green if win, red if loss
    result_text = "WIN" if is_win else "LOSS"

    col1, col2, col3 = st.columns([1,2,1], gap = "large")
    with col1:
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.write("Headshot not found")
    with col2:
        st.markdown(
            f"""
            <div style="text-align:center;">
                <div style="font-size:80px; font-weight:800; margin-bottom:0;">
                    {player}
                </div>
                <div style="font-size:34px; font-weight:800; color:gray; margin-top:-10px; margin-bottom:20px;">
                    vs. {opponent} ({opponent_school})
                </div>
                <div style="
                    display:inline-block;
                    background-color:{bubble_color};
                    color:white;
                    font-size:32px;
                    font-weight:700;
                    padding:12px 28px;
                    border-radius:999px;
                    margin-bottom:20px;
                ">
                    {final_score} • {result_text}
                </div>
                <div style="font-size:28px; margin-top:10px; margin-bottom:20px;">
                    📍 {location} |  📅 {date}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
            if os.path.exists(image_path):
                st.image(opponent_image_path, use_container_width=True)
            else:
                st.write("Headshot not found")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Serve Profile",
        "Return Profile",
        "Points Won",
        "Points Lost",
        "Pressure",
        "Opponent Stats"
    ])

    with tab1:
        render_serve_profile(df, player)
       
    with tab2:
        render_return_profile(df, player, opponent)

    with tab3:
        render_winners_profile(df, player)

    with tab4: 
        render_errors_profile(df, opponent)
        
    with tab5:
        render_pressure_profile(df, player)
    
    with tab6:
        render_opponent_profile(df, player, opponent)