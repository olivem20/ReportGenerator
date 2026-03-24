import streamlit as st
import pandas as pd
import plotly.express as px
   
def render_winners_profile(df, player):
    st.title("Winner Profile")
    col1, col2, col3 = st.columns(3) 
    col4, col5 = st.columns(2) 
    
    ###### Winner Profile ######
    with col1:
        # Only points player won
        wins = df[df["C1: Point Winner"] == player].copy()

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
            subtitle="Breakdown of all groundstroke points you won by hitting a winner or forcing an error",
            color="Winner Label",
            color_discrete_sequence=px.colors.sequential.Greens[::-1]
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside"
        )

        st.plotly_chart(fig, use_container_width=True)
        # st.write("This winner distribution includes both winners and shots that forced an error")
    
    
    with col2:
                # Points where YOU hit the winner (i.e., you won the point)
        winner_points = df[df["C1: Point Winner"] == player].copy()
        winner_points["D1: Winner Type"] = winner_points["D1: Winner Type"].replace(
            "Forced Error", "Forcing Error"
        )

        # Clean Winner Type
        winner_points["D1: Winner Type"] = winner_points["D1: Winner Type"].astype("string").str.strip()

        # Keep only rows where Winner Type exists
        winner_points = winner_points[
            winner_points["D1: Winner Type"].notna() &
            (winner_points["D1: Winner Type"].str.strip() != "")
        ].copy()

        # Count each Winner Type
        counts = winner_points["D1: Winner Type"].value_counts()

        summary = pd.DataFrame({
            "Winner Type": counts.index,
            "Count": counts.values
        })

        # Add percent (for labels)
        total = summary["Count"].sum()
        summary["Percent"] = summary["Count"].div(total).mul(100).round(1) if total > 0 else 0

        # Single stacked bar needs a constant x
        summary["Bar"] = "Winners Breakdown"

        fig = px.bar(
            summary,
            x="Bar",
            y="Count",
            color="Winner Type",
            text=summary.apply(lambda r: f'{int(r["Count"])} ({r["Percent"]}%)', axis=1),
            title="Winners Breakdown",
            subtitle="How you won points",
            barmode="stack"
        )

        fig.update_traces(textposition="inside")

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Count",
            legend_title_text="",
        )

        st.plotly_chart(fig, use_container_width=True)
        # st.write("This chart breaksdown how you won your points," \
        # "whether you won the point being offensive or if your opponent made" \
        # "an error")

    with col4:
        winners = df[
            (df["C1: Point Winner"] == player) &
            (df["D1: Winner Type"].notna())
        ].copy()

        winners["D3: Shot Winner"] = winners["D3: Shot Winner"].astype(str).str.strip()
        winners["D4: Winner Direction"] = winners["D4: Winner Direction"].astype(str).str.strip()

        # ---- FOREHAND ----
        fh = winners[winners["D3: Shot Winner"] == "Forehand"]

        fh_counts = (
            fh["D4: Winner Direction"]
            .value_counts()
            .reset_index()
        )
        fh_counts.columns = ["Direction", "Count"]

        fig_fh = px.bar(
            fh_counts,
            x="Direction",
            y="Count",
            text="Count",
            title="Forehand Winners by Direction"
        )

        fig_fh.update_traces(textposition="outside")
        st.plotly_chart(fig_fh, use_container_width=True)

    with col5:
        # ---- BACKHAND ----
        bh = winners[winners["D3: Shot Winner"] == "Backhand"]

        bh_counts = (
            bh["D4: Winner Direction"]
            .value_counts()
            .reset_index()
        )
        bh_counts.columns = ["Direction", "Count"]

        fig_bh = px.bar(
            bh_counts,
            x="Direction",
            y="Count",
            text="Count",
            title="Backhand Winners by Direction"
        )

        fig_bh.update_traces(textposition="outside")
        st.plotly_chart(fig_bh, use_container_width=True)


    with col3:
        won_points = df[df["C1: Point Winner"] == player].copy()

        aggressive = won_points[won_points["C2: Last Shot Winner"] == player].shape[0]
        steady = won_points[
            (won_points["C3: Last Shot Unforced Error"] != player) &
            (won_points["C3: Last Shot Unforced Error"].notna())
        ].shape[0]

        profile = pd.DataFrame({
            "Style": ["Aggressive", "Steady"],
            "Count": [aggressive, steady]
        })

        total = profile["Count"].sum()
        profile["Percent"] = (
            profile["Count"] / total * 100
        ).round(1) if total > 0 else 0

        fig = px.pie(
            profile,
            names="Style",
            values="Count",
            title="Points won by Phase",
            subtitle="AGGRESSIVE = player winners/forcing errors vs. STEADY = opponent unforced errors",
            color="Style",
            color_discrete_map={
                "Aggressive": "#98df8a",   # green
                "Steady": "#df8a8a"        # lighter green
            }
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="inside",
            hole=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

        # st.write(
        #     "Aggressive = points you finished with a winning shot. "
        #     "Steady = points won because of opponent making an unforced error."
        # )


    points_won = len(df[df["C1: Point Winner"] == player].copy())
        
    points_played = len(df)

    points_won_pct = points_won / points_played

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="Points Won / Points Played", value=f"{points_won} / {points_played}", width="stretch")
    with k3:
        st.metric(label="% Points Won", value=f"{points_won_pct:.1%}", width="stretch")
