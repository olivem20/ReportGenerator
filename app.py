import os
from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from serve_metrics import break_points_saved, break_points_faced, service_games_broken, service_winners, first_serve_percentage, second_serve_percentage, serve_points_won, first_serve_points_won, second_serve_points_won, num_double_faults, num_aces, service_games_held
from deuce_serve_placement import deuce_serves, deuce_serves_win_pct
from ad_serve_placement import ad_serves, ad_serves_win_pct
from group_bar_chart import grouped_percentage_bar_chart
from return_metrics import ad_return_win_pct, ad_return_count, deuce_return_win_pct, deuce_return_count, return_games_won, return_games_played, return_percentage, first_return_pct, second_return_pct, first_return_errors, second_return_errors
from themes import WINNER_PIE_COLORS, ERROR_PIE_COLORS, SERVE_COLORS

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
        
        ########### PLAYER DATA ###########

        ###### Serving Profile ######
        st.header("Serving Profile")
        fs_pct = first_serve_percentage(df, player)
        ss_pct = second_serve_percentage(df, player)
        
        fs_points_won = first_serve_points_won(df, player)

        ss_points_won = second_serve_points_won(df, player)

        service_points_won_pct = serve_points_won(df, player)

        serve_games_won = service_games_held(df, player)
        serve_games_broke = service_games_broken(df, player)

        break_points_total = break_points_faced(df, player)
        break_points_won = break_points_saved(df, player)

        # Double Faults and Aces
        double_faults = num_double_faults(df, player)
        aces = num_aces(df, player)
        service_winners_count = service_winners(df, player)

        ######## AD STATS ########
        ad_wide_1st = ad_serves(df, player, "Yes", "Wide")
        ad_wide_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "Wide")
        ad_wide_2nd = ad_serves(df, player, "No", "Wide")
        ad_wide_2nd_win_pct = ad_serves_win_pct(df, player, "No", "Wide")
        
        ad_body_1st = ad_serves(df, player, "Yes", "Body")
        ad_body_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "Body")
        ad_body_2nd = ad_serves(df, player, "No", "Body")
        ad_body_2nd_win_pct = ad_serves_win_pct(df, player, "No", "Body")
        
        ad_t_1st = ad_serves(df, player, "Yes", "T")
        ad_t_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "T")
        ad_t_2nd = ad_serves(df, player, "No", "T")
        ad_t_2nd_win_pct = ad_serves_win_pct(df, player, "No", "T")

        ######## DEUCE STATS ########
        deuce_wide_1st = deuce_serves(df, player, "Yes", "Wide")
        deuce_wide_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "Wide")
        deuce_wide_2nd = deuce_serves(df, player, "No", "Wide")
        deuce_wide_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "Wide")
        
        deuce_body_1st = deuce_serves(df, player, "Yes", "Body")
        deuce_body_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "Body")
        deuce_body_2nd = deuce_serves(df, player, "No", "Body")
        deuce_body_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "Body")
        
        deuce_t_1st = deuce_serves(df, player, "Yes", "T")
        deuce_t_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "T")
        deuce_t_2nd = deuce_serves(df, player, "No", "T")
        deuce_t_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "T")

        col1, col2, col3 = st.columns([1,1,1])
        ############## SERVE TABLE ##############
        with col1:
            serve_metrics_table = pd.DataFrame(
            [
                {"Metric": "1st Serve %", "Value": f"{fs_pct:.1%}"},
                {"Metric": "2nd Serve %", "Value": f"{ss_pct:.1%}"},
                {"Metric": "1st Serve Points Won %", "Value": f"{fs_points_won:.1%}"},
                {"Metric": "2nd Serve Points Won %", "Value": f"{ss_points_won:.1%}"},
                {"Metric": "Aces", "Value": int(aces)},
                {"Metric": "Service Winners", "Value": int(service_winners_count)},
                {"Metric": "Double Faults", "Value": int(double_faults)},
            ]
            )

            st.subheader("Serve Metrics")
            st.dataframe(
                serve_metrics_table,
                width="stretch",
                hide_index=True
            )

        with col2:
            st.subheader(" ")
            st.metric(label="Serve Points Won %", value=f"{service_points_won_pct:.1%}", width="stretch", height="stretch")
            st.metric(label="Break Points Faced", value=break_points_total, width="stretch", height="stretch")
        with col3:
            st.subheader(" ")
            st.metric(label="Games Held / Games Broken", value=f"{serve_games_won} / {serve_games_broke}", width="stretch", height="stretch")
            st.metric(label="Break Points Saved", value=break_points_won, width="stretch", height="stretch")


        ######################################################################### 
        ######################################################################### 
        ####### ADD BEST SERVE AND LEAST SUCCESSFUL SERVE FOR 1ST AND 2ND #######
        #########################################################################   
        ######################################################################### 

        ################ SERVE PLACEMENT ################


        col1, col2 = st.columns(2)

        with col1:  
            st.header("1st Serve Placement Chart")
            img = Image.open("serve_placement.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()

            ########### AD ###########
            draw.text((902, 299), f"{ad_wide_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((902, 430), f"{ad_wide_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((875, 100), "Ad Wide", fill=(0,0,0,255), font=font) #LABEL

            draw.text((1155, 299), f"{ad_body_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1155, 430), f"{ad_body_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1130, 100), "Ad Body", fill=(0,0,0,255), font=font) #LABEL

            draw.text((1413, 299), f"{ad_t_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1413, 430), f"{ad_t_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1420, 100), "Ad T", fill=(0,0,0,255), font=font) #LABEL

            ########### DEUCE ###########
            draw.text((1660, 299), f"{deuce_t_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1660, 430), f"{deuce_t_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1640, 100), "Deuce T", fill=(0,0,0,255), font=font) #LABEL

            draw.text((1915, 299), f"{deuce_body_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1915, 430), f"{deuce_body_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1856, 100), "Deuce Body", fill=(0,0,0,255), font=font) #LABEL

            draw.text((2167, 299), f"{deuce_wide_1st:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((2167, 430), f"{deuce_wide_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((2110, 100), "Deuce Wide", fill=(0,0,0,255), font=font) #LABEL

            st.image(img, use_container_width=True)
            first_serve_input = st.text_area("Coach's 1st Serve Observations")
            st.write(first_serve_input)

        with col2:
            st.header("2nd Serve Placement Chart")
            img = Image.open("serve_placement.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()

            ########### AD ###########
            draw.text((902, 299), f"{ad_wide_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((902, 430), f"{ad_wide_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((875, 100), "Ad Wide", fill=(0,0,0,255), font=font) #LABEL


            draw.text((1155, 299), f"{ad_body_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1155, 430), f"{ad_body_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1130, 100), "Ad Body", fill=(0,0,0,255), font=font) #LABEL

            draw.text((1413, 299), f"{ad_t_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1413, 430), f"{ad_t_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1420, 100), "Ad T", fill=(0,0,0,255), font=font) #LABEL

            ########### DEUCE ###########
            draw.text((1660, 299), f"{deuce_t_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1660, 430), f"{deuce_t_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1640, 100), "Deuce T", fill=(0,0,0,255), font=font) #LABEL

            draw.text((1915, 299), f"{deuce_body_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((1915, 430), f"{deuce_body_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((1856, 100), "Deuce Body", fill=(0,0,0,255), font=font) #LABEL

            draw.text((2167, 299), f"{deuce_wide_2nd:.1%}", fill=(0,0,0,255), font=font) #USAGE %
            draw.text((2167, 430), f"{deuce_wide_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
            draw.text((2110, 100), "Deuce Wide", fill=(0,0,0,255), font=font) #LABEL



            st.image(img, use_container_width=True)
            second_serve_input = st.text_area("Coach's 2nd Serve Observations")
            st.write(second_serve_input)

    with tab2:
        ############## SERVE TABLE ##############
        ###### Returning Profile ######
        st.header("Return Profile")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        # Return Points Won Percentage
        returns = return_percentage(df, player, opponent)

        # Return points won on 1st serve percentage
        first_returns = first_return_pct(df, player, opponent)

        # Return points won on 2nd serve percentage
        second_returns = second_return_pct(df, player, opponent)

        firstReturnErrors = first_return_errors(df, player, opponent)
        secondReturnErrors = second_return_errors(df, player, opponent)
        returnGamesWon = return_games_won(df, player)
        returnGamesPlayed = return_games_played(df, player)


        with col1:
            return_metrics_table = pd.DataFrame(
            [
                {"Metric": "% Return Points Won", "Value": f"{returns:.1%}"},
                {"Metric": "% " "1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
                {"Metric": "% " "2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
                {"Metric": "Return Games Won/Played", "Value": f"{returnGamesWon}/{returnGamesPlayed}"},
                {"Metric": "1st Serve Return Errors", "Value": int(firstReturnErrors)},
                {"Metric": "2nd Serve Return Errors", "Value": int(secondReturnErrors)},
            ]
            )

            st.subheader("Return Metrics")
            st.dataframe(
                return_metrics_table,
                use_container_width=True,
                hide_index=True
            )
            # Return direction profile, usage and win percenrage for each return
        # %  of offensive returns, win % of offensice returns
        with col2:
            # Filter to points where player was the returner
            ret = df[df["Returner"] == player].copy()

            ret = ret[ret["B4: Return Outcome"].notna()].copy()

            # Clean
            ret["B4: Return Outcome"] = ret["B4: Return Outcome"].astype(str).str.strip()

            # Win flag
            ret["WonPoint"] = (ret["C1: Who Won Point?"] == player)

            # Usage counts (total per outcome)
            outcome = (ret["B4: Return Outcome"].value_counts().reset_index())
            outcome.columns = ["Outcome", "Count"]

            # Wins per outcome  ✅ NEW
            wins = ret.groupby("B4: Return Outcome")["WonPoint"].sum().reset_index()
            wins.columns = ["Outcome", "Wins"]

            # Win rate per outcome
            winrate = ret.groupby("B4: Return Outcome")["WonPoint"].mean().reset_index()
            winrate.columns = ["Outcome", "WinRate"]

            # Merge
            outcome = outcome.merge(wins, on="Outcome", how="left")
            outcome = outcome.merge(winrate, on="Outcome", how="left")

            outcome["Usage%"] = outcome["Count"] / outcome["Count"].sum() * 100
            outcome["Win%"] = outcome["WinRate"] * 100

            # Long format
            long = outcome.melt(
                id_vars=["Outcome", "Count", "Wins"],
                value_vars=["Usage%", "Win%"],
                var_name="Metric",
                value_name="Percent"
            )

            # ✅ Labels: Usage uses Count, Win% uses Wins
            long["Label"] = long.apply(
                lambda r: f"{r['Percent']:.0f}% ({int(r['Count'])})"
                if r["Metric"] == "Usage%"
                else f"{r['Percent']:.0f}% ({int(r['Wins'])})",
                axis=1
            )

            fig = px.bar(
                long,
                x="Outcome",
                y="Percent",
                color="Metric",
                barmode="group",
                text="Label",
                title="Return Outcome: Usage% vs Win%"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(yaxis_range=[0, 100])

            st.plotly_chart(fig, use_container_width=True)

        with col3:
            deuce_fh_cross = deuce_return_count(df, player, "Forehand", "Cross Court")
            deuce_fh_middle = deuce_return_count(df, player, "Forehand", "Middle")
            deuce_fh_line = deuce_return_count(df, player, "Forehand", "Down Line")

            deuce_fh_cross_win = deuce_return_win_pct(df, player, "Forehand", "Cross Court")
            deuce_fh_middle_win = deuce_return_win_pct(df, player, "Forehand", "Middle")
            deuce_fh_line_win = deuce_return_win_pct(df, player, "Forehand", "Down Line")

             
            img = Image.open("deuce_return.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()


            ########### KEY ###########
            draw.text((205, 145), "Key", fill=(0,0,0,255), font=font) 
            draw.text((180, 256), "Count", fill=(0,0,0,255), font=font) 
            draw.text((180, 390), "Win %", fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((735, 177), str(deuce_fh_cross), fill=(0,0,0,255), font=font) 
            draw.text((997, 177), str(deuce_fh_middle), fill=(0,0,0,255), font=font) 
            draw.text((1265 , 177), str(deuce_fh_line), fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((695, 282), f"{deuce_fh_cross_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((960, 282), f"{deuce_fh_middle_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((1220, 282), f"{deuce_fh_line_win:.1%}", fill=(0,0,0,255), font=font)

            st.header("Deuce Side Forehand Returns")
            st.image(img, use_container_width=True)

        with col4:
            deuce_bh_cross = deuce_return_count(df, player, "Backhand", "Inside Out")
            deuce_bh_middle = deuce_return_count(df, player, "Backhand", "Middle")
            deuce_bh_line = deuce_return_count(df, player, "Backhand", "Inside In")

            deuce_bh_cross_win = deuce_return_win_pct(df, player, "Backhand", "Inside Out")
            deuce_bh_middle_win = deuce_return_win_pct(df, player, "Backhand", "Middle")
            deuce_bh_line_win = deuce_return_win_pct(df, player, "Backhand", "Inside In")

             
            img = Image.open("deuce_return.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()


            ########### KEY ###########
            draw.text((205, 145), "Key", fill=(0,0,0,255), font=font) 
            draw.text((180, 256), "Count", fill=(0,0,0,255), font=font) 
            draw.text((180, 390), "Win %", fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((735, 177), str(deuce_bh_cross), fill=(0,0,0,255), font=font) 
            draw.text((997, 177), str(deuce_bh_middle), fill=(0,0,0,255), font=font) 
            draw.text((1265 , 177), str(deuce_bh_line), fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((695, 282), f"{deuce_bh_cross_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((960, 282), f"{deuce_bh_middle_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((1220, 282), f"{deuce_bh_line_win:.1%}", fill=(0,0,0,255), font=font)

            st.header("Deuce Side Backhand Returns")
            st.image(img, use_container_width=True)

        with col5:
            ad_fh_inside_out = ad_return_count(df, player, "Forehand", "Inside Out")
            ad_fh_middle = ad_return_count(df, player, "Forehand", "Middle")
            ad_fh_inside_in = ad_return_count(df, player, "Forehand", "Inside In")

            ad_fh_inside_out_win = ad_return_win_pct(df, player, "Forehand", "Inside Out")
            ad_fh_middle_win = ad_return_win_pct(df, player, "Forehand", "Middle")
            ad_fh_inside_in_win = ad_return_win_pct(df, player, "Forehand", "Inside In")

             
            img = Image.open("ad_return.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()


            ########### KEY ###########
            draw.text((205, 145), "Key", fill=(0,0,0,255), font=font) 
            draw.text((180, 256), "Count", fill=(0,0,0,255), font=font) 
            draw.text((180, 390), "Win %", fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((735, 177), str(ad_fh_inside_in), fill=(0,0,0,255), font=font) 
            draw.text((997, 177), str(ad_fh_middle), fill=(0,0,0,255), font=font) 
            draw.text((1265 , 177), str(ad_fh_inside_out), fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((695, 282), f"{ad_fh_inside_in_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((960, 282), f"{ad_fh_middle_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((1220, 282), f"{ad_fh_inside_out_win:.1%}", fill=(0,0,0,255), font=font)

            st.header("Ad Side Forehand Returns")
            st.image(img, use_container_width=True)
    
        with col6:
            ad_bh_cross = ad_return_count(df, player, "Backhand", "Cross Court")
            ad_bh_middle = ad_return_count(df, player, "Backhand", "Middle")
            ad_bh_line = ad_return_count(df, player, "Backhand", "Down Line")

            ad_bh_cross_win = ad_return_win_pct(df, player, "Backhand", "Cross Court")
            ad_bh_middle_win = ad_return_win_pct(df, player, "Backhand", "Middle")
            ad_bh_line_win = ad_return_win_pct(df, player, "Backhand", "Down Line")

             
            img = Image.open("ad_return.png").convert("RGBA")
            draw = ImageDraw.Draw(img)

            # If you have a .ttf font file, use it; otherwise PIL default
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 40)
            #font = ImageFont.load_default()


            ########### KEY ###########
            draw.text((205, 145), "Key", fill=(0,0,0,255), font=font) 
            draw.text((180, 256), "Count", fill=(0,0,0,255), font=font) 
            draw.text((180, 390), "Win %", fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((735, 177), str(ad_bh_line), fill=(0,0,0,255), font=font) 
            draw.text((997, 177), str(ad_bh_middle), fill=(0,0,0,255), font=font) 
            draw.text((1265 , 177), str(ad_bh_cross), fill=(0,0,0,255), font=font) 

            ########### STATS ###########
            draw.text((695, 282), f"{ad_bh_cross_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((960, 282), f"{ad_bh_middle_win:.1%}", fill=(0,0,0,255), font=font) 
            draw.text((1220, 282), f"{ad_bh_line_win:.1%}", fill=(0,0,0,255), font=font)

            st.header("Ad Side Backhand Returns")
            st.image(img, use_container_width=True)

        ###################################################################
        ##################### ADD OPPONENT RETURNS ########################
        ###################################################################


        return_input = st.text_area("Coach's Return Observations")
        st.write(return_input)

        st.write("add something here about how often opponent attacked certain serves and also" \
        "how often they won those points")
        st.write("this way we can see if serving was a liability or what not")

    with tab3:
        st.title("Winner Profile")
        col1, col2, col22 = st.columns(3) 
        col3, col4, col5 = st.columns(3) 
        
        ###### Winner Profile ######
        with col1:
            # Only points player won
            wins = df[df["C1: Who Won Point?"] == player].copy()

            # Keep rows where there is a winner recorded
            wins = wins[wins["D3: Shot Winner"].notna()]

            # Combine Spin + Shot
            wins["Winner Label"] = (
                wins["D3: Shot Winner"].astype(str).str.strip() + " - " +
                wins["D2: Spin Winner"].astype(str).str.strip()
            )

            winner_counts = (
                wins["Winner Label"]
                .value_counts()
                .reset_index()
            )

            winner_counts.columns = ["Winner Label", "Count"]

            fig = px.pie(
            winner_counts,
                names="Winner Label",
                values="Count",
                title="Winner Distribution (Shot + Spin)",
                color="Winner Label",
                color_discrete_sequence=px.colors.sequential.Greens[::-1]
            )

            fig.update_traces(
                textinfo="percent+label",
                textposition="inside"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.write("This winner distribution includes both winners and shots that forced an error")
        
        
        with col2:
                    # Points where YOU hit the winner (i.e., you won the point)
            winner_points = df[df["C1: Who Won Point?"] == player].copy()

            # Clean Winner Type
            winner_points["D1: Winner Type"] = winner_points["D1: Winner Type"].astype("string").str.strip()

            # Keep only rows where Winner Type exists
            winner_points = winner_points[
                winner_points["D1: Winner Type"].notna() &
                (winner_points["D1: Winner Type"].str.strip() != "")
            ].copy()

            # Count each Winner Type
            counts = winner_points["D1: Winner Type"].value_counts()

            summary = pd.DataFrame({
                "Winner Type": counts.index,
                "Count": counts.values
            })

            # Add percent (for labels)
            total = summary["Count"].sum()
            summary["Percent"] = summary["Count"].div(total).mul(100).round(1) if total > 0 else 0

            # Single stacked bar needs a constant x
            summary["Bar"] = "Winners Breakdown"

            fig = px.bar(
                summary,
                x="Bar",
                y="Count",
                color="Winner Type",
                text=summary.apply(lambda r: f'{int(r["Count"])} ({r["Percent"]}%)', axis=1),
                title="Winners Breakdown",
                barmode="stack"
            )

            fig.update_traces(textposition="inside")

            fig.update_layout(
                xaxis_title="",
                yaxis_title="Count",
                legend_title_text="",
            )

            st.plotly_chart(fig, use_container_width=True)
            st.write("This chart breaksdown how you won your points," \
            "whether you won the point being offensive or if your opponent made" \
            "an error")

        with col3:
            winners = df[
                (df["C1: Who Won Point?"] == player) &
                (df["D1: Winner Type"].notna())
            ].copy()

            winners["D3: Shot Winner"] = winners["D3: Shot Winner"].astype(str).str.strip()
            winners["D4: Winner Direction"] = winners["D4: Winner Direction"].astype(str).str.strip()

            # ---- FOREHAND ----
            fh = winners[winners["D3: Shot Winner"] == "Forehand"]

            fh_counts = (
                fh["D4: Winner Direction"]
                .value_counts()
                .reset_index()
            )
            fh_counts.columns = ["Direction", "Count"]

            fig_fh = px.bar(
                fh_counts,
                x="Direction",
                y="Count",
                text="Count",
                title="Forehand Winners by Direction"
            )

            fig_fh.update_traces(textposition="outside")
            st.plotly_chart(fig_fh, use_container_width=True)

        with col4:
            # ---- BACKHAND ----
            bh = winners[winners["D3: Shot Winner"] == "Backhand"]

            bh_counts = (
                bh["D4: Winner Direction"]
                .value_counts()
                .reset_index()
            )
            bh_counts.columns = ["Direction", "Count"]

            fig_bh = px.bar(
                bh_counts,
                x="Direction",
                y="Count",
                text="Count",
                title="Backhand Winners by Direction"
            )

            fig_bh.update_traces(textposition="outside")
            st.plotly_chart(fig_bh, use_container_width=True)

        with col22:
            points_won = len(df[df["C1: Who Won Point?"] == player].copy())
            points_played = len(df) - 1

            points_won_pct = points_won / points_played

            st.metric(label="Points Won / Points Played", value=f"{points_won} / {points_played}", width="stretch")
            
            st.metric(label="% Points Won", value=f"{points_won_pct:.1%}", width="stretch")

            winner_input = st.text_area("Coach's Winner Observations")
            st.write(winner_input)

    with tab4: 
        ###### Error Profile ######
        col1, col2, col25 = st.columns(3)
        col3, col4, col5 = st.columns(3)

        with col1:
            errors = df[df["C1: Who Won Point?"] == opponent].copy()

            # Keep rows where an error is recorded (shot error)
            errors = errors[errors["F3: Shot Error"].notna()].copy()

            # (Optional) If spin error is sometimes missing, fill it
            errors["F2: Spin Error"] = errors["F2: Spin Error"].fillna("Unknown")

            # Combine Shot Error + Spin Error
            errors["Error Label"] = (
                errors["F3: Shot Error"].astype(str).str.strip() + " - " +
                errors["F2: Spin Error"].astype(str).str.strip()
            )

            error_counts = (
                errors["Error Label"]
                .value_counts()
                .reset_index()
            )
            error_counts.columns = ["Error Label", "Count"]

            fig = px.pie(
                error_counts,
                names="Error Label",
                values="Count",
                title="Error Distribution (Shot + Spin)",
                color="Error Label",
                color_discrete_sequence=px.colors.sequential.Reds[::-1]
            )

            fig.update_traces(
                textinfo="percent+label",
                textposition="inside"
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Only points the opponent won (i.e., player lost the point)
            loss_points = df[df["C1: Who Won Point?"] == opponent].copy()

            # Keep only the three outcomes we care about
            categories = ["Unforced Error", "Double Fault", "Forced Error", f"{opponent} Winner"]
            loss_points = loss_points[loss_points["F1: Error Type"].isin(categories)].copy()

            # Count each category (ensure missing categories appear as 0)
            counts = (
                loss_points["F1: Error Type"]
                .value_counts()
                .reindex(categories, fill_value=0)
            )

            summary = pd.DataFrame({
                "Category": counts.index,
                "Count": counts.values
            })

            # Add percent of these three (optional but nice for labels)
            total = summary["Count"].sum()
            summary["Percent"] = summary["Count"].div(total).mul(100).round(1) if total > 0 else 0

            # Single stacked bar needs a constant x
            summary["Bar"] = "Errors Breakdown"

            fig = px.bar(
                summary,
                x="Bar",
                y="Count",
                color="Category",
                text=summary.apply(lambda r: f'{int(r["Count"])} ({r["Percent"]}%)', axis=1),
                title="Errors Breakdown",
                barmode="stack"
            )

            fig.update_traces(textposition="inside")

            fig.update_layout( 
                xaxis_title="",
                yaxis_title="Count",
                legend_title_text="",
            )


            st.plotly_chart(fig, width="content")
            st.caption(
                "This chart shows the distribution of how you lost points. "
                "Forced error includes the number of points you made an error "
                "due to your opponent hitting a very good shot."
            )

        with col25:
            error_input = st.text_area("Coach's Error Observations")
            st.write(error_input)

        with col3:
            errors = df[
                (df["C1: Who Won Point?"] == opponent) & 
                (df["F1: Error Type"] == "Unforced Error")    
            ].copy()


            # ---- FOREHAND ----
            fh = errors[errors["F3: Shot Error"] == "Forehand"]

            fh_counts = (
                fh["F5: Placement Error"]
                .value_counts()
                .reset_index()
            )
            fh_counts.columns = ["Placement", "Count"]

            fig_fh = px.bar(
                fh_counts,
                x="Placement",
                y="Count",
                text="Count",
                title="Forehand Errors by Placement"
            )

            fig_fh.update_traces(textposition="outside")
            st.plotly_chart(fig_fh, use_container_width=True)

        with col4:
            errors = df[
                (df["C1: Who Won Point?"] == opponent) & 
                (df["F1: Error Type"] == "Unforced Error")    
            ].copy()


            # ---- FOREHAND ----
            fh = errors[errors["F3: Shot Error"] == "Backhand"]

            fh_counts = (
                fh["F5: Placement Error"]
                .value_counts()
                .reset_index()
            )
            fh_counts.columns = ["Placement", "Count"]

            fig_fh = px.bar(
                fh_counts,
                x="Placement",
                y="Count",
                text="Count",
                title="Backhand Errors by Placement"
            )

            fig_fh.update_traces(textposition="outside")
            st.plotly_chart(fig_fh, use_container_width=True)
        
    with tab5:
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
    
    with tab6:
        st.header("Opponent Scouting")

        col1, col2, col3, col4 = st.columns([3, 1, 2, 1])

        # -------------------------
        # 1) Opponent Winners + Forced Errors
        # -------------------------
        with col1:
            st.subheader("How opponent won points (Winners + Forced Errors)")

            opp_offense = df[df["C1: Who Won Point?"] == opponent].copy()

            opp_offense = df[
                (df["C1: Who Won Point?"] == opponent) & 
                (df["G1: Opp. Winner Shot"].notna())    
            ].copy()


            # Combine Shot + Spin into one label
            opp_offense["Winner Label"] = (
                opp_offense["G1: Opp. Winner Shot"] + " - " + opp_offense["G2: Opp. Winner Spin"]
            )

            winner_counts = (
                opp_offense["Winner Label"]
                .value_counts()
                .reset_index()
            )
            winner_counts.columns = ["Winner Label", "Count"]

            fig = px.pie(
                winner_counts,
                names="Winner Label",
                values="Count",
                title="Opponent Winner Distribution (Shot + Spin)",
                color="Winner Label",
                color_discrete_sequence=px.colors.sequential.Greens[::-1]  # optional
            )

            fig.update_traces(textinfo="percent+label", textposition="inside")
            st.plotly_chart(fig, use_container_width=True)


        with col3:
            st.subheader("How Opponent Lost Points (Unforced Errors)")

            opp_errors = df[
                (df["C1: Who Won Point?"] == player) &
                (df["E2: Opp. Unforced Error Shot"].notna())
            ].copy()

            # Clean columns
            opp_errors["E2: Opp. Unforced Error Shot"] = (
                opp_errors["E2: Opp. Unforced Error Shot"]
                .astype(str)
                .str.strip()
            )

            opp_errors["E1: Opp. Unforced Error Spin"] = (
                opp_errors["E1: Opp. Unforced Error Spin"]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
            )

            # Combine Shot + Spin
            opp_errors["Error Label"] = (
                opp_errors["E2: Opp. Unforced Error Shot"] + " - " +
                opp_errors["E1: Opp. Unforced Error Spin"]
            )

            error_counts = (
                opp_errors["Error Label"]
                .value_counts()
                .reset_index()
            )

            error_counts.columns = ["Error Label", "Count"]

            fig = px.pie(
                error_counts,
                names="Error Label",
                values="Count",
                title="Opponent Unforced Errors (Shot + Spin)",
                color="Error Label",
                color_discrete_sequence=px.colors.sequential.Reds[::-1]
            )

            fig.update_traces(
                textinfo="percent+label",
                textposition="inside"
            )

            st.plotly_chart(fig, use_container_width=True)
        
        scout_input = st.text_area("Coach's Scouting Observations")
        st.write(scout_input)
