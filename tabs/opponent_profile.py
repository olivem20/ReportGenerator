import streamlit as st
import pandas as pd
import plotly.express as px

def render_opponent_profile(df, player, opponent):
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
