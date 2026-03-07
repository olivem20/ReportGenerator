import streamlit as st
import pandas as pd
import plotly.express as px

def render_errors_profile(df, opponent):
    col1, col2, col25 = st.columns(3)
    col3, col4, col5 = st.columns(3)

    with col1:
        errors = df[df["C1: Who Won Point?"] == opponent].copy()

        # Keep rows where an error is recorded (shot error)
        errors = errors[errors["F3: Shot Error"].notna()].copy()

        # (Optional) If spin error is sometimes missing, fill it
        errors["F2: Spin Error"] = errors["F2: Spin Error"].fillna("Unknown")

        # Combine Shot Error + Spin Error
        errors["Error Label"] = (
            errors["F3: Shot Error"].astype(str).str.strip() + " - " +
            errors["F2: Spin Error"].astype(str).str.strip()
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
        # Only points the opponent won (i.e., player lost the point)
        loss_points = df[df["C1: Who Won Point?"] == opponent].copy()

        # Keep only the three outcomes we care about
        categories = ["Unforced Error", "Double Fault", "Forced Error", f"{opponent} Winner"]
        loss_points = loss_points[loss_points["F1: Error Type"].isin(categories)].copy()

        # Count each category (ensure missing categories appear as 0)
        counts = (
            loss_points["F1: Error Type"]
            .value_counts()
            .reindex(categories, fill_value=0)
        )

        summary = pd.DataFrame({
            "Category": counts.index,
            "Count": counts.values
        })

        # Add percent of these three (optional but nice for labels)
        total = summary["Count"].sum()
        summary["Percent"] = summary["Count"].div(total).mul(100).round(1) if total > 0 else 0

        # Single stacked bar needs a constant x
        summary["Bar"] = "Errors Breakdown"

        fig = px.bar(
            summary,
            x="Bar",
            y="Count",
            color="Category",
            text=summary.apply(lambda r: f'{int(r["Count"])} ({r["Percent"]}%)', axis=1),
            title="Errors Breakdown",
            barmode="stack"
        )

        fig.update_traces(textposition="inside")

        fig.update_layout( 
            xaxis_title="",
            yaxis_title="Count",
            legend_title_text="",
        )


        st.plotly_chart(fig, width="content")
        st.caption(
            "This chart shows the distribution of how you lost points. "
            "Forced error includes the number of points you made an error "
            "due to your opponent hitting a very good shot."
        )

    with col25:
        error_input = st.text_area("Coach's Error Observations")
        st.write(error_input)

    with col3:
        errors = df[
            (df["C1: Who Won Point?"] == opponent) & 
            (df["F1: Error Type"] == "Unforced Error")    
        ].copy()


        # ---- FOREHAND ----
        fh = errors[errors["F3: Shot Error"] == "Forehand"]

        fh_counts = (
            fh["F5: Placement Error"]
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
            (df["C1: Who Won Point?"] == opponent) & 
            (df["F1: Error Type"] == "Unforced Error")    
        ].copy()


        # ---- FOREHAND ----
        fh = errors[errors["F3: Shot Error"] == "Backhand"]

        fh_counts = (
            fh["F5: Placement Error"]
            .value_counts()
            .reset_index()
        )
        fh_counts.columns = ["Placement", "Count"]

        fig_fh = px.bar(
            fh_counts,
            x="Placement",
            y="Count",
            text="Count",
            title="Backhand Errors by Placement"
        )

        fig_fh.update_traces(textposition="outside")
        st.plotly_chart(fig_fh, use_container_width=True)