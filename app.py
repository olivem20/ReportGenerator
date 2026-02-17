import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

        ############## SERVE TABLE ##############
        serve_metrics_table = pd.DataFrame(
        [
            {"Metric": "1st Serve %", "Value": f"{fs_pct:.1%}"},
            {"Metric": "1st Serve Points Won %", "Value": f"{fs_points_won:.1%}"},
            {"Metric": "2nd Serve Points Won %", "Value": f"{ss_points_won:.1%}"},
            {"Metric": "Aces", "Value": int(aces)},
            {"Metric": "Service Winners", "Value": int(aces)},
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

        fig1 = grouped_percentage_bar_chart(
            categories_deuce,
            usage_values,
            win_values,
            "Deuce Side: 1st Serve Placement"
        )

        st.pyplot(fig1)

        ############## AD CHART ##############

        usage_values = [
        ad_wide_serves,
        ad_body_serves,
        ad_t_serves
        ]

        win_values = [
            ad_wide_win,
            ad_body_win,
            ad_t_win
        ]

        fig2 = grouped_percentage_bar_chart(
            categories_ad,
            usage_values,
            win_values,
            "Ad Side: 1st Serve Placement"
        )

        st.pyplot(fig2)


    with tab2:
        ############## SERVE TABLE ##############
        

        
        ###### Returning Profile ######
        st.header("Return Profile")
        # Return Points Won Percentage
        returns = return_percentage(df, player, opponent)

        # Return points won on 1st serve percentage
        first_returns = first_return_pct(df, player, opponent)

        # Return points won on 2nd serve percentage
        second_returns = second_return_pct(df, player, opponent)

        firstReturnErrors = first_return_errors(df, player, opponent)
        secondReturnErrors = second_return_errors(df, player, opponent)
        
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
        # pressure point returns

    with tab3:
        ###### Winner Profile ######
        st.title("Winner Profile")
        st.header("Winner Type Count")
        win_points = df[df["C1: Who Won Point?"] == player]

        win_type_counts = (
            win_points["D1: Winner Type"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .reset_index()
        )

        win_type_counts.columns = ["Winner Type", "Count"]

        st.bar_chart(
            win_type_counts,
            x="Winner Type",
            y="Count",
            stack=False
        )

        ############# PIE CART #############

        # Only points player won
        wins = df[df["C1: Who Won Point?"] == player].copy()

        # Keep rows where there is a winner recorded
        wins = wins[
            wins["D3: Shot Winner"].notna()
        ]

        # Combine Spin + Shot
        wins["Winner Label"] = (
            wins["D3: Shot Winner"].astype(str).str.strip() + " - " +
            wins["D2: Spin Winner"].astype(str).str.strip()
        )

        winner_counts = wins["Winner Label"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            winner_counts,
            labels=winner_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=WINNER_PIE_COLORS[:len(winner_counts)]
        )

        ax.set_title("Winner Distribution (Shot + Spin)")

        st.pyplot(fig)

    with tab4:

        ###### Error Profile ######
        errors = df[df["C1: Who Won Point?"] == opponent].copy()

        # Only rows where there is an error recorded
        errors = errors[errors["F3: Shot Error"].notna()]

        # COMBINE ERROR SHOT AND SPIN HERE
        errors["Error Label"] = (
            errors["F3: Shot Error"].astype(str).str.strip()
            + " - "
            + errors["F2: Spin Error"].fillna("").astype(str).str.strip()
        )
        errors["Error Label"] = errors["Error Label"].str.replace(r"\s-\s$", "", regex=True)

        error_counts = (
            errors["Error Label"]
            .replace("", pd.NA)
            .dropna()
            .value_counts()
        )

        fig, ax = plt.subplots()

        ax.pie(
            error_counts,
            labels=error_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=ERROR_PIE_COLORS[:len(error_counts)]
        )

        ax.axis("equal")
        ax.set_title("Error Distribution (Shot + Spin)")

        st.pyplot(fig)



    ###### Pressure Points Profile ######

