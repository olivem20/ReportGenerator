import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from serve_metrics import service_winners, first_serve_percentage, first_serve_points_won, second_serve_points_won, num_double_faults, num_aces
from deuce_serve_placement import deuce_wide, deuce_body, deuce_t, deuce_body_win_pct, deuce_wide_win_pct, deuce_t_win_pct
from ad_serve_placement import ad_wide, ad_body, ad_t, ad_body_win_pct, ad_wide_win_pct, ad_t_win_pct
from group_bar_chart import grouped_percentage_bar_chart
from return_metrics import return_percentage, first_return_pct, second_return_pct, first_return_errors, second_return_errors
from themes import WINNER_PIE_COLORS, ERROR_PIE_COLORS, SERVE_COLORS

st.title("Report Generator")

uploaded_file = st.file_uploader("Please upload Match CSV")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    #st.write(df)

    ### EXTRACT NOTES ###
    match_info = df.iloc[0]

    final_score = match_info["Final Score"]
    player = match_info["Player"]
    opponent = match_info["Opponent"]
    opponent_school = match_info["Opponent School"]
    location = match_info["Location"]
    date = match_info["Date"]

    # Match Winner
    winner_col = "C1: Who Won Point?"
    match_winner = df[winner_col].dropna().iloc[-1]

    ### WRITE INFO ###
    st.title(f"Match Winner: {match_winner}")
    st.subheader(f"**Final Score:** {final_score}")

    st.write(f"**Player:** {player}")
    st.write(f"**Opponent:** {opponent}")
    st.write(f"**Opponent School:** {opponent_school}")
    st.write(f"**Location:** {location}")
    st.write(f"**Date:** {date}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Serve Profile",
        "Return Profile",
        "Winners",
        "Errors",
        "Pressure"
    ])

    with tab1:
        
        ########### PLAYER DATA ###########

        ###### Serving Profile ######
        st.header("Serving Profile")
        fs_pct = first_serve_percentage(df, player)
        
        fs_points_won = first_serve_points_won(df, player)

        ss_points_won = second_serve_points_won(df, player)

        # Double Faults and Aces
        double_faults = num_double_faults(df, player)
        aces = num_aces(df, player)
        service_winners_count = service_winners(df, player)

        # Deuce Serve Location
        deuce_wide_serves = deuce_wide(df, player)
        deuce_body_serves = deuce_body(df, player)
        deuce_t_serves = deuce_t(df, player)

        deuce_body_win = deuce_body_win_pct(df, player)
        deuce_t_win = deuce_t_win_pct(df, player)
        deuce_wide_win = deuce_wide_win_pct(df, player)

        # Ad Serve Location
        ad_wide_serves = ad_wide(df, player)
        ad_body_serves = ad_body(df, player)
        ad_t_serves = ad_t(df, player)

        ad_body_win = ad_body_win_pct(df, player)
        ad_t_win = ad_t_win_pct(df, player)
        ad_wide_win = ad_wide_win_pct(df, player)
        
        
        col1, col2, col3 = st.columns(3)
        ############## SERVE TABLE ##############
        with col1:
            serve_metrics_table = pd.DataFrame(
            [
                {"Metric": "1st Serve %", "Value": f"{fs_pct:.1%}"},
                {"Metric": "1st Serve Points Won %", "Value": f"{fs_points_won:.1%}"},
                {"Metric": "2nd Serve Points Won %", "Value": f"{ss_points_won:.1%}"},
                {"Metric": "Aces", "Value": int(aces)},
                {"Metric": "Service Winners", "Value": int(service_winners_count)},
                {"Metric": "Double Faults", "Value": int(double_faults)},
            ]
            )

            st.subheader("Serve Metrics")
            st.dataframe(
                serve_metrics_table,
                use_container_width=True,
                hide_index=True
            )

        ############## DEUCE CHART ##############
        with col2:
            categories_deuce = ["Wide", "Body", "T"]
            categories_ad = ["T", "Body", "Wide"]

            usage_values = [
                deuce_wide_serves,
                deuce_body_serves,
                deuce_t_serves
            ]

            win_values = [
                deuce_wide_win,
                deuce_body_win,
                deuce_t_win
            ]

            # Create DataFrame
            # Convert to percentage (0–100)
            usage_values = [v * 100 for v in usage_values]
            win_values = [v * 100 for v in win_values]

            df_deuce = pd.DataFrame({
                "Placement": categories_deuce,
                "Usage %": usage_values,
                "Win %": win_values
            })

            # Melt for grouped bars
            df_deuce = df_deuce.melt(
                id_vars="Placement",
                var_name="Metric",
                value_name="Percent"
            )

            # Base chart
            base = alt.Chart(df_deuce).encode(
                x=alt.X("Placement:N", axis=alt.Axis(labelAngle=0), scale=alt.Scale(domain=categories_deuce)),
                xOffset="Metric:N",
                color="Metric:N"
            )

            # Bars
            bars = base.mark_bar().encode(
                y=alt.Y(
                    "Percent:Q",
                    axis=alt.Axis(format=".0f"),
                    scale=alt.Scale(domain=[0, 100])
                )
            )

            # Text labels
            text = base.mark_text(
                dy=-5,                 # moves text above bar
                fontSize=12,
                fontWeight="bold"
            ).encode(
                y="Percent:Q",
                text=alt.Text("Percent:Q", format=".0f")  # shows whole number
            )

            # Combine
            chart = (bars + text).properties(
                title="Deuce Side: 1st Serve Placement"
            )

            st.altair_chart(chart, use_container_width=True)


        ############## AD CHART #############
        with col3:
            usage_values = [
                ad_t_serves,
                ad_body_serves,
                ad_wide_serves
            ]

            win_values = [
                ad_wide_win,
                ad_body_win,
                ad_t_win
            ]

            # Create DataFrame
            # Convert to percentage (0–100)
            usage_values = [v * 100 for v in usage_values]
            win_values = [v * 100 for v in win_values]

            df_ad = pd.DataFrame({
                "Placement": categories_ad,
                "Usage %": usage_values,
                "Win %": win_values
            })

            # Melt for grouped bars
            df_ad = df_ad.melt(
                id_vars="Placement",
                var_name="Metric",
                value_name="Percent"
            )

            # Base chart
            base = alt.Chart(df_ad).encode(
                x=alt.X("Placement:N", axis=alt.Axis(labelAngle=0), scale=alt.Scale(domain=categories_ad)),
                xOffset="Metric:N",
                color="Metric:N"
            )

            # Bars
            bars = base.mark_bar().encode(
                y=alt.Y(
                    "Percent:Q",
                    axis=alt.Axis(format=".0f"),
                    scale=alt.Scale(domain=[0, 100])
                )
            )

            # Text labels
            text = base.mark_text(
                dy=-5,                 # moves text above bar
                fontSize=12,
                fontWeight="bold"
            ).encode(
                y="Percent:Q",
                text=alt.Text("Percent:Q", format=".0f")  # shows whole number
            )

            # Combine
            chart = (bars + text).properties(
                title="Ad Side: 1st Serve Placement"
            )

            st.altair_chart(chart, use_container_width=True)

        


    with tab2:
        ############## SERVE TABLE ##############
        ###### Returning Profile ######
        st.header("Return Profile")

        col1, col2, col3 = st.columns(3)
        # Return Points Won Percentage
        returns = return_percentage(df, player, opponent)

        # Return points won on 1st serve percentage
        first_returns = first_return_pct(df, player, opponent)

        # Return points won on 2nd serve percentage
        second_returns = second_return_pct(df, player, opponent)

        firstReturnErrors = first_return_errors(df, player, opponent)
        secondReturnErrors = second_return_errors(df, player, opponent)
        
        with col1:
            return_metrics_table = pd.DataFrame(
            [
                {"Metric": "Return Points Won", "Value": f"{returns:.1%}"},
                {"Metric": "1st Serve Return Points Won", "Value": f"{first_returns:.1%}"},
                {"Metric": "2nd Serve Return Points Won", "Value": f"{second_returns:.1%}"},
                {"Metric": "1st Serve Returns Missed", "Value": int(firstReturnErrors)},
                {"Metric": "2nd Serve Returns Missed", "Value": int(secondReturnErrors)},
            ]
            )

            st.subheader("Return Metrics")
            st.dataframe(
                return_metrics_table,
                use_container_width=True,
                hide_index=True
            )
            # Return direction profile, usage and win percenrage for each return
        # %  of offensive returns, win % of offensice returns
        with col2:
            # Filter to points where player was the returner
            ret = df[df["Returner"] == player].copy()

            ret = ret[ret["B4: Return Outcome"].notna()].copy()

            # Clean
            ret["B4: Return Outcome"] = ret["B4: Return Outcome"].astype(str).str.strip()

            # Win flag
            ret["WonPoint"] = (ret["C1: Who Won Point?"] == player)

            # Usage counts (total per outcome)
            outcome = (ret["B4: Return Outcome"].value_counts().reset_index())
            outcome.columns = ["Outcome", "Count"]

            # Wins per outcome  ✅ NEW
            wins = ret.groupby("B4: Return Outcome")["WonPoint"].sum().reset_index()
            wins.columns = ["Outcome", "Wins"]

            # Win rate per outcome
            winrate = ret.groupby("B4: Return Outcome")["WonPoint"].mean().reset_index()
            winrate.columns = ["Outcome", "WinRate"]

            # Merge
            outcome = outcome.merge(wins, on="Outcome", how="left")
            outcome = outcome.merge(winrate, on="Outcome", how="left")

            outcome["Usage%"] = outcome["Count"] / outcome["Count"].sum() * 100
            outcome["Win%"] = outcome["WinRate"] * 100

            # Long format
            long = outcome.melt(
                id_vars=["Outcome", "Count", "Wins"],
                value_vars=["Usage%", "Win%"],
                var_name="Metric",
                value_name="Percent"
            )

            # ✅ Labels: Usage uses Count, Win% uses Wins
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

    with tab3:
        st.title("Winner Profile")

        col1, col2, col3 = st.columns(3)
        ###### Winner Profile ######
        with col1:
            # Only points player won
            wins = df[df["C1: Who Won Point?"] == player].copy()

            # Keep rows where there is a winner recorded
            wins = wins[wins["D3: Shot Winner"].notna()]

            # Combine Spin + Shot
            wins["Winner Label"] = (
                wins["D3: Shot Winner"].astype(str).str.strip() + " - " +
                wins["D2: Spin Winner"].astype(str).str.strip()
            )

            winner_counts = (
                wins["Winner Label"]
                .value_counts()
                .reset_index()
            )

            winner_counts.columns = ["Winner Label", "Count"]

            fig = px.pie(
            winner_counts,
                names="Winner Label",
                values="Count",
                title="Winner Distribution (Shot + Spin)",
                color="Winner Label",
                color_discrete_sequence=px.colors.sequential.Greens[::-1]
            )

            fig.update_traces(
                textinfo="percent+label",
                textposition="inside"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.write("This winner distribution includes both winners and shots that forced an error")

            txt = st.text_area(
                "Please input your coaching here"
            )

            st.write(txt)
        

        with col2:
            # Keep rows where winner exists
            wins = wins[wins["D3: Shot Winner"].notna()].copy()

            # Clean fields
            wins["D3: Shot Winner"] = wins["D3: Shot Winner"].astype(str).str.strip()
            wins["D2: Spin Winner"] = wins["D2: Spin Winner"].astype(str).str.strip()
            wins["D4: Winner Direction"] = wins["D4: Winner Direction"].astype(str).str.strip()
            wins["A2: 1st Serve Location"] = wins["A2: 1st Serve Location"].astype(str).str.strip()

            def build_winner_label(row):
                if row["D3: Shot Winner"] == "Serve":
                    return f"Serve - {row['A2: 1st Serve Location']}"
                else:
                    return f"{row['D3: Shot Winner']} - {row['D2: Spin Winner']} - {row['D4: Winner Direction']}"

            wins["Winner Combo"] = wins.apply(build_winner_label, axis=1)
            # Count combinations
            combo_counts = (
                wins["Winner Combo"]
                .value_counts()
                .reset_index()
            )

            combo_counts.columns = ["Winner Combo", "Count"]

            # Add percent label
            total = combo_counts["Count"].sum()
            combo_counts["Percent"] = combo_counts["Count"] / total * 100
            combo_counts["Label"] = combo_counts["Percent"].round(0).astype(int).astype(str) + "%"

            # Create horizontal bar chart (better for long labels)
            fig = px.bar(
                combo_counts,
                x="Count",
                y="Winner Combo",
                orientation="h",
                text="Label",
                title="Winner Breakdown (Shot + Spin + Direction)"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Number of Winners / Forced Errors"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.write("This winner breakdown includes both winners and forced errors")
            txt2 = st.text_area(
                "Please input your coaching here "
            )

            st.write(txt2)

    with tab4:
        ###### Error Profile ######
        col1, col2, col3 = st.columns(3)
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

            # Filter to points where the OPPONENT won (i.e., player made the error)
            errors = df[df["C1: Who Won Point?"] == opponent].copy()

            # Keep rows where an error exists
            errors = errors[errors["F3: Shot Error"].notna()].copy()

            # Clean fields
            errors["F3: Shot Error"] = errors["F3: Shot Error"].astype(str).str.strip()
            errors["F2: Spin Error"] = errors["F2: Spin Error"].astype(str).str.strip()
            errors["F4: Error Direction"] = errors["F4: Error Direction"].astype(str).str.strip()

            # Optional: if some spin/direction are missing, keep label clean
            def build_error_label(row):
                parts = [row["F3: Shot Error"], row["F2: Spin Error"], row["F4: Error Direction"]]
                parts = [p for p in parts if p and str(p).lower() != "nan"]
                return " - ".join(parts)

            errors["Error Combo"] = errors.apply(build_error_label, axis=1)

            # Remove any accidental empty labels
            errors = errors[errors["Error Combo"].notna() & (errors["Error Combo"].str.strip() != "")].copy()

            # Count combinations
            combo_counts = (
                errors["Error Combo"]
                .value_counts()
                .reset_index()
            )
            combo_counts.columns = ["Error Combo", "Count"]

            # Add percent label
            total = combo_counts["Count"].sum()
            combo_counts["Percent"] = combo_counts["Count"] / total * 100
            combo_counts["Label"] = combo_counts["Percent"].round(0).astype(int).astype(str) + "%"

            # Horizontal bar chart
            fig = px.bar(
                combo_counts,
                x="Count",
                y="Error Combo",
                orientation="h",
                text="Label",
                title="Error Breakdown (Shot + Spin + Direction)"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(
                yaxis_title="",
                xaxis_title="Number of Errors"
            )

            st.plotly_chart(fig, use_container_width=True)
                    # Keep rows where winner exists
            


    ###### Pressure Points Profile ######

