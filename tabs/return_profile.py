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
)
from font import get_font


def render_return_profile(df, player, opponent):
    st.header("Return Profile")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    # Return Points Won Percentage
    returns = return_percentage(df, player)
    first_returns = first_return_pct(df, player, opponent)
    second_returns = second_return_pct(df, player, opponent)

    first_return_errors_count = first_return_errors(df, player, opponent)
    second_return_errors_count = second_return_errors(df, player, opponent)
    return_games_won_count = return_games_won(df, player)
    return_games_played_count = return_games_played(df, player)

    with col1:
        return_metrics_table = pd.DataFrame(
            [
                {"Metric": "% Return Points Won", "Value": f"{returns:.1%}"},
                {"Metric": "% 1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
                {"Metric": "% 2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
                {"Metric": "Return Games Won/Played", "Value": f"{return_games_won_count}/{return_games_played_count}"},
                {"Metric": "1st Serve Return Errors", "Value": int(first_return_errors_count)},
                {"Metric": "2nd Serve Return Errors", "Value": int(second_return_errors_count)},
            ]
        )

        st.subheader("Return Metrics")
        st.dataframe(
            return_metrics_table,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        ret = df[df["Server"] != player].copy()
        ret = ret[ret["B4: Return Outcome"].notna()].copy()
        ret["B4: Return Outcome"] = ret["B4: Return Outcome"].astype(str).str.strip()
        ret["WonPoint"] = (ret["C1: Point Winner"] == player)

        outcome = ret["B4: Return Outcome"].value_counts().reset_index()
        outcome.columns = ["Outcome", "Count"]

        wins = ret.groupby("B4: Return Outcome")["WonPoint"].sum().reset_index()
        wins.columns = ["Outcome", "Wins"]

        winrate = ret.groupby("B4: Return Outcome")["WonPoint"].mean().reset_index()
        winrate.columns = ["Outcome", "WinRate"]

        outcome = outcome.merge(wins, on="Outcome", how="left")
        outcome = outcome.merge(winrate, on="Outcome", how="left")

        outcome["Usage%"] = outcome["Count"] / outcome["Count"].sum() * 100
        outcome["Win%"] = outcome["WinRate"] * 100

        long = outcome.melt(
            id_vars=["Outcome", "Count", "Wins"],
            value_vars=["Usage%", "Win%"],
            var_name="Metric",
            value_name="Percent"
        )

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
        deuce_bh_cross = deuce_return_count(df, player, "Backhand", "Inside Out")
        deuce_bh_middle = deuce_return_count(df, player, "Backhand", "Middle")
        deuce_bh_line = deuce_return_count(df, player, "Backhand", "Inside In")

        deuce_bh_cross_win = deuce_return_win_pct(df, player, "Backhand", "Inside Out")
        deuce_bh_middle_win = deuce_return_win_pct(df, player, "Backhand", "Middle")
        deuce_bh_line_win = deuce_return_win_pct(df, player, "Backhand", "Inside In")

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

        draw.text((695, 282), f"{ad_bh_cross_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((960, 282), f"{ad_bh_middle_win:.1%}", fill=(0, 0, 0, 255), font=font)
        draw.text((1220, 282), f"{ad_bh_line_win:.1%}", fill=(0, 0, 0, 255), font=font)

        st.header("Ad Side Backhand Returns")
        st.image(img, use_container_width=True)

    return_input = st.text_area("Coach's Return Observations")
    st.write(return_input)

    st.write(
        "add something here about how often opponent attacked certain serves and also "
        "how often they won those points"
    )
    st.write(
        "this way we can see if serving was a liability or what not"
    )