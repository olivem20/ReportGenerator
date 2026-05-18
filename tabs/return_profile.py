import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image, ImageDraw

from metrics.return_metrics import (
    return_win_pct,
    return_count,
    return_games_won,
    return_games_played,
    return_percentage,
    first_return_pct,
    second_return_pct,
    first_return_errors,
    second_return_errors,
    forced_errors_w_return,
    return_winners
)
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


def render_return_profile(df, player):
    st.header("Return Profile")


 
    # Return Points Won Percentage
    returns = return_percentage(df, player)
    first_returns = first_return_pct(df, player)
    second_returns = second_return_pct(df, player)

    first_return_errors_count = first_return_errors(df, player)
    second_return_errors_count = second_return_errors(df, player)
    return_games_won_count = return_games_won(df, player)
    return_games_played_count = return_games_played(df, player)
    forced = forced_errors_w_return(df, player)
    winners = return_winners(df, player)

    #################################
    ############# DEUCE ############# 
    deuce_fh_cross = return_count(df, player, "Forehand", "Cross Court", "Deuce")
    deuce_fh_middle = return_count(df, player, "Forehand", "Middle", "Deuce")
    deuce_fh_line = return_count(df, player, "Forehand", "Down Line", "Deuce")

    deuce_fh_cross_win = return_win_pct(df, player, "Forehand", "Cross Court", "Deuce")
    deuce_fh_middle_win = return_win_pct(df, player, "Forehand", "Middle", "Deuce")
    deuce_fh_line_win = return_win_pct(df, player, "Forehand", "Down Line", "Deuce")

    deuce_bh_cross = return_count(df, player, "Backhand", "Inside Out", "Deuce")
    deuce_bh_middle = return_count(df, player, "Backhand", "Middle", "Deuce")
    deuce_bh_line = return_count(df, player, "Backhand", "Inside In", "Deuce")

    deuce_bh_cross_win = return_win_pct(df, player, "Backhand", "Inside Out", "Deuce")
    deuce_bh_middle_win = return_win_pct(df, player, "Backhand", "Middle", "Deuce")
    deuce_bh_line_win = return_win_pct(df, player, "Backhand", "Inside In", "Deuce")

    #################################
    ############# AD ################
    ad_fh_inside_out = return_count(df, player, "Forehand", "Inside Out", "Ad")
    ad_fh_middle = return_count(df, player, "Forehand", "Middle", "Ad")
    ad_fh_inside_in = return_count(df, player, "Forehand", "Inside In", "Ad")

    ad_fh_inside_out_win = return_win_pct(df, player, "Forehand", "Inside Out", "Ad")
    ad_fh_middle_win = return_win_pct(df, player, "Forehand", "Middle", "Ad")
    ad_fh_inside_in_win = return_win_pct(df, player, "Forehand", "Inside In", "Ad")

    ad_bh_inside_out = return_count(df, player, "Backhand", "Inside Out", "Ad")
    ad_bh_middle = return_count(df, player, "Backhand", "Middle", "Ad")
    ad_bh_inside_in = return_count(df, player, "Backhand", "Inside In", "Ad")

    ad_bh_inside_out_win = return_win_pct(df, player, "Backhand", "Inside Out", "Ad")
    ad_bh_middle_win = return_win_pct(df, player, "Backhand", "Middle", "Ad")
    ad_bh_inside_in_win = return_win_pct(df, player, "Backhand", "Inside In", "Ad")



    col1, col2 = st.columns([1,1])
    col3, col4 = st.columns(2) 
    col5, col6 = st.columns(2)

    with col2:
        return_metrics_table = pd.DataFrame(
            [
                {"Metric": "% Return Points Won", "Value": f"{returns:.1%}"},
                {"Metric": "% 1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
                {"Metric": "% 2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
                {"Metric": "Return Games Won/Played", "Value": f"{return_games_won_count}/{return_games_played_count}"},
            ] 
        )

        st.subheader("Return Metrics")
        st.dataframe(
            return_metrics_table,
            use_container_width=True,
            hide_index=True,
            height=272
        )

    with col1:
        st.subheader("Return Impact")
        impact_col1, impact_col2 = st.columns(2)
        with impact_col2:
            

            stat_card(
                "1st Return Errors",
                f"{int(first_return_errors_count)}",
                "Missed returns off of first-serve",
                bg="rgba(239, 68, 68, 0.18)",
                border="#ef4444"
            )

            stat_card(
                "2nd Return Errors",
                f"{int(second_return_errors_count)}",
                "Missed returns off of second-serve",
                bg="rgba(249, 115, 22, 0.18)",
                border="#f97316"
            )
        with impact_col1:
            stat_card(
                "Return Winners",
                f"{int(winners)}",
                "Clean winners hit on return",
                bg="rgba(34, 197, 94, 0.18)",
                border="#22c55e"
            )

            stat_card(
                "Forced Errors",
                f"{int(forced)}",
                "Returns that forced errors",
                bg="rgba(59, 130, 246, 0.18)",
                border="#3b82f6"
            )



    with col3:
        
        img = Image.open("assets/deuce_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(deuce_fh_cross), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(deuce_fh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(deuce_fh_line), fill=(0, 0, 0, 255), font=font)

        draw.text((680, 285), f"{deuce_fh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((956, 285), f"{deuce_fh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1210, 285), f"{deuce_fh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Deuce Side Forehand Returns")
        st.image(img, use_container_width=True)

    with col4:
        img = Image.open("assets/deuce_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(deuce_bh_cross), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(deuce_bh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(deuce_bh_line), fill=(0, 0, 0, 255), font=font)

        draw.text((680, 285), f"{deuce_bh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((956, 285), f"{deuce_bh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1210, 285), f"{deuce_bh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Deuce Side Backhand Returns")
        st.image(img, use_container_width=True)

    with col5:
        img = Image.open("assets/ad_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(ad_fh_inside_in), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(ad_fh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(ad_fh_inside_out), fill=(0, 0, 0, 255), font=font)

        draw.text((680, 285), f"{ad_fh_inside_in_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((955, 285), f"{ad_fh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1210, 285), f"{ad_fh_inside_out_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Ad Side Forehand Returns")
        st.image(img, use_container_width=True)

    with col6:
        ad_bh_cross = return_count(df, player, "Backhand", "Cross Court", "Ad")
        ad_bh_middle = return_count(df, player, "Backhand", "Middle", "Ad")
        ad_bh_line = return_count(df, player, "Backhand", "Down Line", "Ad")

        ad_bh_cross_win = return_win_pct(df, player, "Backhand", "Cross Court", "Ad")
        ad_bh_middle_win = return_win_pct(df, player, "Backhand", "Middle", "Ad")
        ad_bh_line_win = return_win_pct(df, player, "Backhand", "Down Line", "Ad")

        img = Image.open("assets/ad_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(ad_bh_line), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(ad_bh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(ad_bh_cross), fill=(0, 0, 0, 255), font=font)

        draw.text((680, 285), f"{ad_bh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((955, 285), f"{ad_bh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1210, 285), f"{ad_bh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Ad Side Backhand Returns")
        st.image(img, use_container_width=True)

