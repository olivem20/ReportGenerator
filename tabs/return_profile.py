import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image, ImageDraw

from metrics.return_metrics import (
    ad_return_win_pct,
    ad_return_count,
    deuce_return_win_pct,
    deuce_return_count,
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
    deuce_fh_cross = deuce_return_count(df, player, "Forehand", "Cross Court")
    deuce_fh_middle = deuce_return_count(df, player, "Forehand", "Middle")
    deuce_fh_line = deuce_return_count(df, player, "Forehand", "Down Line")

    deuce_fh_cross_win = deuce_return_win_pct(df, player, "Forehand", "Cross Court")
    deuce_fh_middle_win = deuce_return_win_pct(df, player, "Forehand", "Middle")
    deuce_fh_line_win = deuce_return_win_pct(df, player, "Forehand", "Down Line")

    deuce_bh_cross = deuce_return_count(df, player, "Backhand", "Inside Out")
    deuce_bh_middle = deuce_return_count(df, player, "Backhand", "Middle")
    deuce_bh_line = deuce_return_count(df, player, "Backhand", "Inside In")

    deuce_bh_cross_win = deuce_return_win_pct(df, player, "Backhand", "Inside Out")
    deuce_bh_middle_win = deuce_return_win_pct(df, player, "Backhand", "Middle")
    deuce_bh_line_win = deuce_return_win_pct(df, player, "Backhand", "Inside In")

    #################################
    ############# AD ################
    ad_fh_inside_out = ad_return_count(df, player, "Forehand", "Inside Out")
    ad_fh_middle = ad_return_count(df, player, "Forehand", "Middle")
    ad_fh_inside_in = ad_return_count(df, player, "Forehand", "Inside In")

    ad_fh_inside_out_win = ad_return_win_pct(df, player, "Forehand", "Inside Out")
    ad_fh_middle_win = ad_return_win_pct(df, player, "Forehand", "Middle")
    ad_fh_inside_in_win = ad_return_win_pct(df, player, "Forehand", "Inside In")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric("Return Pts Won", f"{returns:.1%}")

    with k2:
        st.metric("1st Return Pts Won", f"{first_returns:.1%}")

    with k3:
        st.metric("2nd Return Pts Won", f"{second_returns:.1%}")

    with k4:
        st.metric("Return Games", f"{return_games_won_count}/{return_games_played_count}")


    k5, k6, k7, k8 = st.columns(4) 

    with k5:
        st.metric("1st Return Errors", int(first_return_errors_count))

    with k6:
        st.metric("2nd Return Errors", int(second_return_errors_count))

    with k7:
        st.metric("Return Winners", int(winners))

    with k8:
        st.metric("Forced Errors", int(forced))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2) 
    col5, col6 = st.columns(2)

    # with col1:
    #     return_metrics_table = pd.DataFrame(
    #         [
    #             {"Metric": "% Return Points Won", "Value": f"{returns:.1%}"},
    #             {"Metric": "% 1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
    #             {"Metric": "% 2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
    #             {"Metric": "Return Games Won/Played", "Value": f"{return_games_won_count}/{return_games_played_count}"},
    #             {"Metric": "1st Serve Return Errors", "Value": int(first_return_errors_count)},
    #             {"Metric": "2nd Serve Return Errors", "Value": int(second_return_errors_count)},
    #             {"Metric": "Return Winners", "Value": int(winners)},
    #             {"Metric": "Returns that Forced Errors", "Value": int(forced)},
    #         ] 
    #     )

    #     st.subheader("Return Metrics")
    #     st.dataframe(
    #         return_metrics_table,
    #         use_container_width=True,
    #         hide_index=True
    #     )




    with col2:
        st.write


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

        draw.text((695, 282), f"{deuce_fh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((960, 282), f"{deuce_fh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1220, 282), f"{deuce_fh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)

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

        draw.text((695, 282), f"{deuce_bh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((960, 282), f"{deuce_bh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1220, 282), f"{deuce_bh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Deuce Side Backhand Returns")
        st.image(img, use_container_width=True)

    with col5:
        ad_fh_inside_out = ad_return_count(df, player, "Forehand", "Inside Out")
        ad_fh_middle = ad_return_count(df, player, "Forehand", "Middle")
        ad_fh_inside_in = ad_return_count(df, player, "Forehand", "Inside In")

        ad_fh_inside_out_win = ad_return_win_pct(df, player, "Forehand", "Inside Out")
        ad_fh_middle_win = ad_return_win_pct(df, player, "Forehand", "Middle")
        ad_fh_inside_in_win = ad_return_win_pct(df, player, "Forehand", "Inside In")
 
        img = Image.open("assets/ad_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(ad_fh_inside_in), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(ad_fh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(ad_fh_inside_out), fill=(0, 0, 0, 255), font=font)

        draw.text((695, 282), f"{ad_fh_inside_in_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((960, 282), f"{ad_fh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1220, 282), f"{ad_fh_inside_out_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Ad Side Forehand Returns")
        st.image(img, use_container_width=True)

    with col6:
        ad_bh_cross = ad_return_count(df, player, "Backhand", "Cross Court")
        ad_bh_middle = ad_return_count(df, player, "Backhand", "Middle")
        ad_bh_line = ad_return_count(df, player, "Backhand", "Down Line")

        ad_bh_cross_win = ad_return_win_pct(df, player, "Backhand", "Cross Court")
        ad_bh_middle_win = ad_return_win_pct(df, player, "Backhand", "Middle")
        ad_bh_line_win = ad_return_win_pct(df, player, "Backhand", "Down Line")

        img = Image.open("assets/ad_return.png").convert("RGBA")
        draw = ImageDraw.Draw(img)
        font = get_font(40)

        draw.text((205, 145), "Key", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 256), "Count", fill=(0, 0, 0, 255), font=font)
        draw.text((180, 390), "Win %", fill=(0, 0, 0, 255), font=font)

        draw.text((735, 177), str(ad_bh_line), fill=(0, 0, 0, 255), font=font)
        draw.text((997, 177), str(ad_bh_middle), fill=(0, 0, 0, 255), font=font)
        draw.text((1265, 177), str(ad_bh_cross), fill=(0, 0, 0, 255), font=font)

        draw.text((695, 282), f"{ad_bh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((960, 282), f"{ad_bh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1220, 282), f"{ad_bh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Ad Side Backhand Returns")
        st.image(img, use_container_width=True)

    return_input = st.text_area("Coach's Return Observations")
    st.write(return_input)
