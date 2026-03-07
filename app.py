import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
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
    player = match_info["Player"]
    opponent = match_info["Opponent"]
    opponent_school = match_info["Opponent School"]
    location = match_info["Location"]
    date = match_info["Date"]

    player_first_name = player.split()[0]
    player_png = f"{player_first_name}.png"
    image_path = os.path.join("Headhsots", player_png) 

    # Match Winner  
    winner_col = "C1: Who Won Point?" 
    match_winner = df[winner_col].dropna().iloc[-1]

    col1, col2, col3, col4, col5, col6 = st.columns([1,1,3,2,1,1], gap="xxsmall")
    with col4:
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.write("Headshot not found")
    with col3:
        ### WRITE INFO ###  
        st.title(f"***Player:*** {player}", text_alignment="center")
        st.markdown(f"## ***Final Score:*** {final_score}")
        st.markdown(f"## ***Opponent:*** {opponent}")
        st.markdown(f"## ***Opponent School:*** {opponent_school}")
        st.markdown(f"## ***Match Winner:*** {match_winner}")
        st.markdown(f"## ***Location:*** {location}")
        st.markdown(f"## ***Date:*** {date}")



    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Serve Profile",
        "Return Profile",
        "Winners",
        "Errors",
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