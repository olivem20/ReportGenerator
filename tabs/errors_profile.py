import streamlit as st
import pandas as pd
import plotly.express as px

def render_errors_profile(df, player):
    col1, col2, col3 = st.columns(3)
    col4, col5= st.columns(2)

    with col1:
        errors = df[df["C1: Point Winner"] != player].copy()

        # Keep rows where an error is recorded (shot error)
        errors = errors[errors["E2: Shot Error"].notna()].copy()
        
        # Combine Shot Error + Spin Error
        errors["Error Label"] = (
            errors["E2: Shot Error"].astype(str).str.strip() + " - " +
            errors["E3: Spin Error"].astype(str).str.strip()
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

  

    with col3:
        lost_points = df[df["C1: Point Winner"] != player].copy()

        opp_aggressive = lost_points[
            (lost_points["C2: Last Shot Winner"] != player) &
            (lost_points["C2: Last Shot Winner"].notna())
            ].shape[0]
        errors = lost_points[lost_points["C3: Last Shot Unforced Error"] == player].shape[0]

        profile = pd.DataFrame({
            "Style": ["Opponent Aggressive", "Unforced Errors"],
            "Count": [opp_aggressive, errors]
        })

        total = profile["Count"].sum()
        profile["Percent"] = (
            profile["Count"] / total * 100
        ).round(1) if total > 0 else 0

        fig = px.pie(
            profile,
            names="Style",
            values="Count",
            title="How You Won Points",
            color="Style",
            color_discrete_map={
                "Opponent Aggressive": "#98df8a",   # green
                "Unforced": "#df8a8a"        # lighter green
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
            hole=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "Aggressive = points you finished with a winning shot. "
            "Steady = points won because of opponent making an unforced error."
        )


    with col4:
        errors = df[
            (df["C1: Point Winner"] != player) & 
            (df["E1: Error Type"] == "Unforced Error")    
        ].copy()


        # ---- FOREHAND ----
        fh = errors[errors["E2: Shot Error"] == "Forehand"]

        fh_counts = (
            fh["E5: Error Location"]
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

    with col5:
        errors = df[
            (df["C1: Point Winner"] != player) & 
            (df["E1: Error Type"] == "Unforced Error")    
        ].copy()


        # ---- FOREHAND ----
        fh = errors[errors["E2: Shot Error"] == "Backhand"]

        fh_counts = (
            fh["E5: Error Location"]
            .value_counts()
            .reset_index()
        )
        fh_counts.columns = ["Location", "Count"]

        fig_fh = px.bar(
            fh_counts,
            x="Location",
            y="Count",
            text="Count",
            title="Backhand Errors by Location"
        )

        fig_fh.update_traces(textposition="outside")
        st.plotly_chart(fig_fh, use_container_width=True)


    with col2:
        lost_points = df[df["C1: Point Winner"] != player].copy()

        # Clean columns
        lost_points["C2: Last Shot Winner"] = lost_points["C2: Last Shot Winner"].fillna("").astype(str).str.strip()
        lost_points["D1: Winner Type"] = lost_points["D1: Winner Type"].fillna("").astype(str).str.strip()
        lost_points["E1: Error Type"] = lost_points["E1: Error Type"].fillna("").astype(str).str.strip()

        # Start with error type
        lost_points["Loss Type"] = lost_points["E1: Error Type"]

        # If opponent hit a winner, overwrite with winner type
        mask_opp_winner = (
            (lost_points["C2: Last Shot Winner"] != "") &
            (lost_points["C2: Last Shot Winner"] != player)
        )

        lost_points.loc[mask_opp_winner, "Loss Type"] = lost_points.loc[mask_opp_winner, "D1: Winner Type"]

        # Optional fallback if D1 is blank
        lost_points["Loss Type"] = lost_points["Loss Type"].replace("", "Other")

        counts = lost_points["Loss Type"].value_counts()

        summary = pd.DataFrame({
            "Loss Type": counts.index,
            "Count": counts.values
        })

        total = summary["Count"].sum()
        summary["Percent"] = summary["Count"].div(total).mul(100).round(1) if total > 0 else 0
        summary["Bar"] = "Loss Breakdown"

        fig = px.bar(
            summary,
            x="Bar",
            y="Count",
            color="Loss Type",
            text=summary.apply(lambda r: f'{int(r["Count"])} ({r["Percent"]}%)', axis=1),
            title="How You Lost Points",
            barmode="stack"
        )

        fig.update_traces(textposition="inside")
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Count",
            legend_title_text=""
        )

        st.plotly_chart(fig, use_container_width=True)
