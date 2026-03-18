import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

from metrics.serve_metrics import (
    break_points_saved, break_points_faced, service_games_broken,
    service_winners, first_serve_percentage, second_serve_percentage,
    serve_points_won, first_serve_points_won, second_serve_points_won,
    num_double_faults, num_aces, service_games_held
)
from metrics.deuce_serve_placement import deuce_serves_count, deuce_serves_win_pct
from metrics.ad_serve_placement import ad_serves_count, ad_serves_win_pct
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
        ad_wide_1st = ad_serves_count(df, player, "Yes", "Wide")
        ad_wide_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "Wide")
        ad_wide_2nd = ad_serves_count(df, player, "No", "Wide")
        ad_wide_2nd_win_pct = ad_serves_win_pct(df, player, "No", "Wide")
        
        ad_body_1st = ad_serves_count(df, player, "Yes", "Body")
        ad_body_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "Body")
        ad_body_2nd = ad_serves_count(df, player, "No", "Body")
        ad_body_2nd_win_pct = ad_serves_win_pct(df, player, "No", "Body")
        
        ad_t_1st = ad_serves_count(df, player, "Yes", "T")
        ad_t_1st_win_pct = ad_serves_win_pct(df, player, "Yes", "T")
        ad_t_2nd = ad_serves_count(df, player, "No", "T")
        ad_t_2nd_win_pct = ad_serves_win_pct(df, player, "No", "T")

        ######## DEUCE STATS ########
        deuce_wide_1st = deuce_serves_count(df, player, "Yes", "Wide")
        deuce_wide_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "Wide")
        deuce_wide_2nd = deuce_serves_count(df, player, "No", "Wide")
        deuce_wide_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "Wide")
        
        deuce_body_1st = deuce_serves_count(df, player, "Yes", "Body")
        deuce_body_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "Body")
        deuce_body_2nd = deuce_serves_count(df, player, "No", "Body")
        deuce_body_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "Body")
        
        deuce_t_1st = deuce_serves_count(df, player, "Yes", "T")
        deuce_t_1st_win_pct = deuce_serves_win_pct(df, player, "Yes", "T")
        deuce_t_2nd = deuce_serves_count(df, player, "No", "T")
        deuce_t_2nd_win_pct = deuce_serves_win_pct(df, player, "No", "T")


        st.header("1st Serve Placement Chart")
        img = Image.open("assets/serve_placement_NEW.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        # If you have a .ttf font file, use it; otherwise PIL default
        font = get_font(40)
        #font = ImageFont.load_default()

        draw.text((177, 95), "Key", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((154, 188), "Count", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((155, 305), "Win %", fill=(0,0,0,255), font=font) #USAGE %

        ########### AD ###########
        draw.text((690, 190), f"{ad_wide_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((655, 305), f"{ad_wide_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((660, 70), "Wide", fill=(0,0,0,255), font=font) #LABEL

        draw.text((920, 190), f"{ad_body_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((880, 305), f"{ad_body_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((880, 70), "Body", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1150, 190), f"{ad_t_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1110, 305), f"{ad_t_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1150, 70), "T", fill=(0,0,0,255), font=font) #LABEL

        draw.text((830, 600), "Ad Serves", fill=(255,255,255,255), font=font) #LABEL
        ########### DEUCE ###########
        draw.text((1373, 190), f"{deuce_t_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1335, 305), f"{deuce_t_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1373, 70), "T", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1600, 190), f"{deuce_body_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1560, 305), f"{deuce_body_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1570, 70), "Body", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1810, 190), f"{deuce_wide_1st}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1787, 305), f"{deuce_wide_1st_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1799, 70), "Wide", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1480, 600), "Deuce Serves", fill=(255,255,255,255), font=font) #LABEL

        st.image(img, use_container_width=True)

        st.header("2nd Serve Placement Chart")
        img = Image.open("assets/serve_placement_NEW.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        # If you have a .ttf font file, use it; otherwise PIL default
        font = get_font(40)
        #font = ImageFont.load_default()

        draw.text((177, 95), "Key", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((154, 188), "Count", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((155, 305), "Win %", fill=(0,0,0,255), font=font) #USAGE %

        ########### AD ###########
        draw.text((690, 190), f"{ad_wide_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((655, 305), f"{ad_wide_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((660, 70), "Wide", fill=(0,0,0,255), font=font) #LABEL

        draw.text((920, 190), f"{ad_body_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((880, 305), f"{ad_body_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((880, 70), "Body", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1150, 190), f"{ad_t_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1110, 305), f"{ad_t_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1150, 70), "T", fill=(0,0,0,255), font=font) #LABEL

        draw.text((830, 600), "Ad Serves", fill=(255,255,255,255), font=font) #LABEL
        ########### DEUCE ###########
        draw.text((1373, 190), f"{deuce_t_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1335, 305), f"{deuce_t_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1373, 70), "T", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1600, 190), f"{deuce_body_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1560, 305), f"{deuce_body_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1570, 70), "Body", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1810, 190), f"{deuce_wide_2nd}", fill=(0,0,0,255), font=font) #USAGE %
        draw.text((1787, 305), f"{deuce_wide_2nd_win_pct:.1%}", fill=(0,0,0,255), font=font) #WIN %
        draw.text((1799, 70), "Wide", fill=(0,0,0,255), font=font) #LABEL

        draw.text((1480, 600), "Deuce Serves", fill=(255,255,255,255), font=font) #LABEL

        st.image(img, use_container_width=True)





        col1, col2, col3 = st.columns([4,2,2])

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
            st.dataframe(
                serve_metrics_table,
                width="stretch",
                hide_index=True
            )

        with col2:
            st.metric(label="Serve Points Won %", value=f"{service_points_won_pct:.1%}", width="stretch", height="content", border=True)
            st.metric(label="Games Held / Games Broken", value=f"{serve_games_won} / {serve_games_broke}", width="stretch", height="content", border=True)
        with col3:
            st.metric(label="Break Points Faced", value=break_points_total, width="stretch", height="content", border=True)
            st.metric(label="Break Points Saved", value=break_points_won, width="stretch", height="content", border=True)


        second_serve_input = st.text_area("Coach's Serving Observations")
        st.write(second_serve_input)

