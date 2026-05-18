import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw

from metrics.serve_metrics import (
    break_points_saved, break_points_faced, service_games_broken,
    service_winners, first_serve_percentage, second_serve_percentage,
    serve_points_won, first_serve_points_won, second_serve_points_won,
    num_double_faults, num_aces, service_games_held
)
from metrics.serve_placement import serve_count, serve_win_pct

from font import get_font

def stat_card(title, value, subtitle="", bg="rgba(59, 130, 246, 0.10)", border="#3b82f6"):
    st.markdown(
        f"""
        <div style="
            background:{bg};
            border-left:6px solid {border};
            padding:16px 18px;
            border-radius:12px;
            min-height:110px;
            margin-bottom:12px;
        ">
            <div style="font-size:15px; color:white; font-weight:600; margin-bottom:8px;">
                {title}
            </div>
            <div style="font-size:32px; font-weight:800; color:white; line-height:1.1;">
                {value}
            </div>
            <div style="font-size:14px; color:#6b7280; margin-top:8px;">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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
        ad_wide_1st = serve_count(df, player, "Yes", "Wide", "Ad")
        ad_wide_1st_win_pct = serve_win_pct(df, player, "Yes", "Wide", "Ad")
        ad_wide_2nd = serve_count(df, player, "No", "Wide", "Ad")
        ad_wide_2nd_win_pct = serve_win_pct(df, player, "No", "Wide", "Ad")
        
        ad_body_1st = serve_count(df, player, "Yes", "Body", "Ad")
        ad_body_1st_win_pct = serve_win_pct(df, player, "Yes", "Body", "Ad")
        ad_body_2nd = serve_count(df, player, "No", "Body", "Ad")
        ad_body_2nd_win_pct = serve_win_pct(df, player, "No", "Body", "Ad")
        
        ad_t_1st = serve_count(df, player, "Yes", "T", "Ad")
        ad_t_1st_win_pct = serve_win_pct(df, player, "Yes", "T", "Ad")
        ad_t_2nd = serve_count(df, player, "No", "T", "Ad")
        ad_t_2nd_win_pct = serve_win_pct(df, player, "No", "T", "Ad")

        ######## DEUCE STATS ########
        deuce_wide_1st = serve_count(df, player, "Yes", "Wide", "Deuce")
        deuce_wide_1st_win_pct = serve_win_pct(df, player, "Yes", "Wide", "Deuce")
        deuce_wide_2nd = serve_count(df, player, "No", "Wide", "Deuce")
        deuce_wide_2nd_win_pct = serve_win_pct(df, player, "No", "Wide", "Deuce")
        
        deuce_body_1st = serve_count(df, player, "Yes", "Body", "Deuce")
        deuce_body_1st_win_pct = serve_win_pct(df, player, "Yes", "Body", "Deuce")
        deuce_body_2nd = serve_count(df, player, "No", "Body", "Deuce")
        deuce_body_2nd_win_pct = serve_win_pct(df, player, "No", "Body", "Deuce")
        
        deuce_t_1st = serve_count(df, player, "Yes", "T", "Deuce")
        deuce_t_1st_win_pct = serve_win_pct(df, player, "Yes", "T", "Deuce")
        deuce_t_2nd = serve_count(df, player, "No", "T", "Deuce")
        deuce_t_2nd_win_pct = serve_win_pct(df, player, "No", "T", "Deuce")


        st.header("Serve Summary")

        impact1, impact2, impact3, impact4 = st.columns(4)
   
        with impact1:
            stat_card(
                "Aces / Service Winners",
                f"{int(aces)} / {int(service_winners_count)}",
                "Free points created on serve",
                bg="rgba(34, 197, 94, 0.10)",
                border="#16a34a"
            )
        with impact2:
            stat_card(
                "Double Faults",
                f"{int(double_faults)}",
                "Points lost on serve",
                bg="rgba(239, 68, 68, 0.10)",
                border="#dc2626"
            )

        with impact3:
            saved_pct = (break_points_won / break_points_total) if break_points_total else 0
            stat_card(
                "Break Points Saved",
                f"{break_points_won}/{break_points_total}",
                f"{saved_pct:.1%} saved" if break_points_total else "No break points faced",
                bg="rgba(249, 115, 22, 0.10)",
                border="#ead40c"
            )
        with impact4:
            hold_pct_base = serve_games_won + serve_games_broke
            hold_pct = (serve_games_won / hold_pct_base) if hold_pct_base else 0
            stat_card(
                "Hold Rate",
                f"{hold_pct:.1%}",
                f"Held {serve_games_won} of {hold_pct_base} service games" if hold_pct_base else "No service games logged",
                bg="rgba(99, 102, 241, 0.10)",
                border="#4f46e5"
            )

        st.subheader("Serve Stats Detail")

        serve_metrics_table = pd.DataFrame(
            [
                {"Metric": "1st Serve %", "Value": f"{fs_pct:.1%}"},
                {"Metric": "2nd Serve %", "Value": f"{ss_pct:.1%}"},
                {"Metric": "1st Serve Points Won %", "Value": f"{fs_points_won:.1%}"},
                {"Metric": "2nd Serve Points Won %", "Value": f"{ss_points_won:.1%}"},
                {"Metric": "Serve Points Won %", "Value": f"{service_points_won_pct:.1%}"},
            ]
        )

        st.dataframe(
            serve_metrics_table,
            use_container_width=True,
            hide_index=True
        )


        st.header("1st Serve Placement Chart")
        img = Image.open("assets/serve_placement_NEW.png").convert("RGBA")
        draw = ImageDraw.Draw(img)

        # If you have a .ttf font file, use it; otherwise PIL default
        font = get_font(35)
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
        font = get_font(35)
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


