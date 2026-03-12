import streamlit as st
import pandas as pd
import plotly.express as px

def render_errors_profile(df, opponent):
    col1, col2, col25 = st.columns(3)
    col3, col4, col5 = st.columns(3)

    with col1:
        errors = df[df["C1: Point Winner"] == opponent].copy()

        # Keep rows where an error is recorded (shot error)
        errors = errors[errors["E2: Shot Error"].notna()].copy()

        # (Optional) If spin error is sometimes missing, fill it
        errors["E3: Spin Error"] = errors["E3: Spin Error"].fillna("Unknown")

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

    with col2:
    # Only points won by the player
        won_points = df[df["C1: Point Winner"] == opponent].copy()

        # Count winner types
        winner_counts = (
            won_points["D1: Winner Type"]
            .dropna()
            .value_counts()
            .reset_index()
        )
        winner_counts.columns = ["Category", "Count"]
        winner_counts["Group"] = "Winner Types"

        # Count error types
        error_counts = (
            won_points["E1: Error Type"]
            .dropna()
            .value_counts()
            .reset_index()
        )
        error_counts.columns = ["Category", "Count"]
        error_counts["Group"] = "Error Types"

        # Combine both
        summary = pd.concat([winner_counts, error_counts], ignore_index=True)

        # Plot stacked bar
        fig = px.bar(
            summary,
            x="Group",
            y="Count",
            color="Category",
            title="How Player Lost Points",
            barmode="stack"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Count",
            legend_title_text=""
        )

        st.plotly_chart(fig, width="content")


    with col25:
        error_input = st.text_area("Coach's Error Observations")
        st.write(error_input)

    with col3:
        errors = df[
            (df["C1: Point Winner"] == opponent) & 
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

    with col4:
        errors = df[
            (df["C1: Point Winner"] == opponent) & 
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