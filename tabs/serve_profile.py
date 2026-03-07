import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

from serve_metrics import (
    break_points_saved, break_points_faced, service_games_broken,
    service_winners, first_serve_percentage, second_serve_percentage,
    serve_points_won, first_serve_points_won, second_serve_points_won,
    num_double_faults, num_aces, service_games_held
)
from deuce_serve_placement import deuce_serves, deuce_serves_win_pct
from ad_serve_placement import ad_serves, ad_serves_win_pct
from font import get_font


def render_serve_profile(df, player):
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
            font = get_font(40)
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
            font = get_font(40)
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