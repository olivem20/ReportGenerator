import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

from metrics.serve_metrics import opp_serve_count

def render_opponent_profile(df, player, opponent):
    st.header("Opponent Scouting")

    col1, col3 = st.columns(2)

    # -------------------------
    # 1) Opponent Winners + Forced Errors
    # -------------------------
    with col1:
        st.subheader("How opponent won points (Winners + Forcing Errors)")

        opp_offense = df[df["C2: Last Shot Winner"] == opponent].copy()

        # Combine Shot + Spin into one label
        opp_offense["Winner Label"] = (
            opp_offense["D3: Shot Winner"] + " - " + opp_offense["D2: Spin Winner"]
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
            color="Winner Label",
            color_discrete_sequence=px.colors.sequential.Greens[::-1]  # optional
        )

        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.subheader("How Opponent Lost Points (Unforced Errors)")

        opp_errors = df[df["C3: Last Shot Unforced Error"] == opponent].copy()


        # Combine Shot + Spin
        opp_errors["Error Label"] = (
            opp_errors["E2: Shot Error"] + " - " +
            opp_errors["E3: Spin Error"]
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
            color="Error Label",
            color_discrete_sequence=px.colors.sequential.Reds[::-1]
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside"
        )

        st.plotly_chart(fig, use_container_width=True)
    




    col1, col2 = st.columns(2)
    

    with col1:
        st.subheader("Ad Side Serve Locations")

        ad_serves = opp_serve_count(df, player, "Ad")

        ad_chart = alt.Chart(ad_serves).mark_bar().encode(
            x=alt.X("Serve Location:N", sort=["Wide", "Body", "T"]),
            y=alt.Y("Count:Q"),
            tooltip=["Serve Location", "Count"]
        )

        st.altair_chart(ad_chart, use_container_width=True)
 
    with col2:
        st.subheader("Deuce Side Serve Locations")

        deuce_serves = opp_serve_count(df, player, "Deuce")

        deuce_chart = alt.Chart(deuce_serves).mark_bar().encode(
            x=alt.X("Serve Location:N", sort=["T", "Body", "Wide"]),
            y=alt.Y("Count:Q"),
            tooltip=["Serve Location", "Count"]
        )

        st.altair_chart(deuce_chart, use_container_width=True)