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
from return_metrics import return_percentage, first_return_pct, second_return_pct, first_return_errors, second_return_errors
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
        st.title(f"***Match Winner:*** {match_winner}", text_alignment="center")
        st.markdown(f"## ***Final Score:*** {final_score}")
        st.markdown(f"## ***Player:*** {player}")
        st.markdown(f"## ***Opponent:*** {opponent}")
        st.markdown(f"## ***Opponent School:*** {opponent_school}")
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
            first_serve_input = st.text_area("Coaches 1st Serve Observations")
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
            second_serve_input = st.text_area("Coaches 2nd Serve Observations")
            st.write(second_serve_input)

    with tab2:
        ############## SERVE TABLE ##############
        ###### Returning Profile ######
        st.header("Return Profile")

        col1, col2, col3 = st.columns(3)
        # Return Points Won Percentage
        returns = return_percentage(df, player, opponent)

        # Return points won on 1st serve percentage
        first_returns = first_return_pct(df, player, opponent)

        # Return points won on 2nd serve percentage
        second_returns = second_return_pct(df, player, opponent)

        firstReturnErrors = first_return_errors(df, player, opponent)
        secondReturnErrors = second_return_errors(df, player, opponent)
        
        with col1:
            return_metrics_table = pd.DataFrame(
            [
                {"Metric": "Return Points Won", "Value": f"{returns:.1%}"},
                {"Metric": "1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
                {"Metric": "2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
                {"Metric": "1st Serve Returns Missed", "Value": int(firstReturnErrors)},
                {"Metric": "2nd Serve Returns Missed", "Value": int(secondReturnErrors)},
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

    with tab3:
        st.title("Winner Profile")

        col1, col2, col3 = st.columns(3)
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

            txt = st.text_area(
                "Please input your coaching here"
            )

            st.write(txt)
        

        with col2:
            # Keep rows where winner exists
            wins = wins[wins["D3: Shot Winner"].notna()].copy()

            # Clean fields
            wins["D3: Shot Winner"] = wins["D3: Shot Winner"].astype(str).str.strip()
            wins["D2: Spin Winner"] = wins["D2: Spin Winner"].astype(str).str.strip()
            wins["D4: Winner Direction"] = wins["D4: Winner Direction"].astype(str).str.strip()
            wins["A2: 1st Serve Location"] = wins["A2: 1st Serve Location"].astype(str).str.strip()

            def build_winner_label(row):
                if row["D3: Shot Winner"] == "Serve":
                    return f"Serve - {row['A2: 1st Serve Location']}"
                else:
                    return f"{row['D3: Shot Winner']} - {row['D2: Spin Winner']} - {row['D4: Winner Direction']}"

            wins["Winner Combo"] = wins.apply(build_winner_label, axis=1)
            # Count combinations
            combo_counts = (
                wins["Winner Combo"]
                .value_counts()
                .reset_index()
            )

            combo_counts.columns = ["Winner Combo", "Count"]

            # Add percent label
            total = combo_counts["Count"].sum()
            combo_counts["Percent"] = combo_counts["Count"] / total * 100
            combo_counts["Label"] = combo_counts["Percent"].round(0).astype(int).astype(str) + "%"

            # Create horizontal bar chart (better for long labels)
            fig = px.bar(
                combo_counts,
                x="Count",
                y="Winner Combo",
                orientation="h",
                text="Label",
                title="Winner Breakdown (Shot + Spin + Direction)"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Number of Winners / Forced Errors"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.write("This winner breakdown includes both winners and forced errors")
            txt2 = st.text_area(
                "Please input your coaching here "
            )

            st.write(txt2)

    with tab4:
        ###### Error Profile ######
        col1, col2, col3 = st.columns(3)
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

            # Filter to points where the OPPONENT won (i.e., player made the error)
            errors = df[df["C1: Who Won Point?"] == opponent].copy()

            # Keep rows where an error exists
            errors = errors[errors["F3: Shot Error"].notna()].copy()

            # Clean fields
            errors["F3: Shot Error"] = errors["F3: Shot Error"].astype(str).str.strip()
            errors["F2: Spin Error"] = errors["F2: Spin Error"].astype(str).str.strip()
            errors["F4: Error Direction"] = errors["F4: Error Direction"].astype(str).str.strip()

            # Optional: if some spin/direction are missing, keep label clean
            def build_error_label(row):
                parts = [row["F3: Shot Error"], row["F2: Spin Error"], row["F4: Error Direction"]]
                parts = [p for p in parts if p and str(p).lower() != "nan"]
                return " - ".join(parts)

            errors["Error Combo"] = errors.apply(build_error_label, axis=1)

            # Remove any accidental empty labels
            errors = errors[errors["Error Combo"].notna() & (errors["Error Combo"].str.strip() != "")].copy()

            # Count combinations
            combo_counts = (
                errors["Error Combo"]
                .value_counts()
                .reset_index()
            )
            combo_counts.columns = ["Error Combo", "Count"]

            # Add percent label
            total = combo_counts["Count"].sum()
            combo_counts["Percent"] = combo_counts["Count"] / total * 100
            combo_counts["Label"] = combo_counts["Percent"].round(0).astype(int).astype(str) + "%"

            # Horizontal bar chart
            fig = px.bar(
                combo_counts,
                x="Count",
                y="Error Combo",
                orientation="h",
                text="Label",
                title="Error Breakdown (Shot + Spin + Direction)"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Number of Errors"
            )

            st.plotly_chart(fig, use_container_width=True)
                    # Keep rows where winner exists
    


    ###### Pressure Points Profile ######

