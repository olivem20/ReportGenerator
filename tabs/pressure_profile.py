import streamlit as st
import pandas as pd

def render_pressure_profile(df, player):
    st.header("Deuce Points")
    deuce_points = df[df["Deuce"].notna()].copy()

    deuce_points_played = len(deuce_points)

    deuce_points_won = len(
        deuce_points[deuce_points["C1: Point Winner"] == player]
    )

    win_pct = (deuce_points_won / deuce_points_played) * 100 if deuce_points_played > 0 else 0

    col2, col3 = st.columns(2)

    with col2:
        st.subheader("Deuce Point Outcomes")

        for deuce_count, (_, row) in enumerate(deuce_points.iterrows(), start=1):
            winner = row["C1: Point Winner"]
            player_won = str(winner).strip().lower() == str(player).strip().lower()

            card_bg = "rgba(34, 197, 94, 0.12)" if player_won else "rgba(239, 68, 68, 0.12)"
            card_border = "#22c55e" if player_won else "#ef4444"
            result_text = "Won" if player_won else "Lost"

            def clean_value(val):
                if pd.isna(val):
                    return ""
                return str(val)

            if pd.notna(row.get("C2: Last Shot Winner")):
                end_type = row.get("D1: Winner Type")
                shot = clean_value(row.get("D3: Shot Winner"))
                spin = clean_value(row.get("D2: Spin Winner"))

            elif pd.notna(row.get("C3: Last Shot Unforced Error")):
                end_type = row.get("E1: Error Type")
                if end_type == "Unforced Error":
                    end_type = "Opponent Unforced Error"
                shot = clean_value(row.get("E2: Shot Error"))
                spin = clean_value(row.get("E3: Spin Error"))

            else:
                end_type = "Other"
                shot = ""
                spin = ""


            st.markdown(
                f"""
                <div style="
                    background:{card_bg};
                    border-left:6px solid {card_border};
                    padding:14px 16px;
                    border-radius:12px;
                    margin-bottom:12px;
                ">
                    <div style="font-size:18px; font-weight:700; margin-bottom:6px;">
                        Deuce #{deuce_count} • {result_text}
                    </div>
                    <div style="font-size:15px; margin-bottom:4px;">
                        <strong>End Type:</strong> {end_type}
                    </div>
                    <div style="font-size:15px;">
                        <strong>Details:</strong> {spin} {shot} 
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

  

    st.metric(
        "Deuce Points Won",
        f"{deuce_points_won}/{deuce_points_played} ({win_pct:.0f}%)"
    )

    deuce_points = df[df["Deuce"].notna()].copy()

    c = st.container()
    with c:
        st.subheader("Weighted Pressure Points")

        pressure_scores = ["30-30", "30-40", "40-30", "40-40"]

        pressure_df = df[df["Game Score"].isin(pressure_scores)].copy()

        if len(pressure_df) > 0:
            pressure_df = pressure_df.reset_index(drop=True)
            pressure_df["Point #"] = range(1, len(pressure_df) + 1)

            # Define weights
            weight_map = {
                "30-30": 0.7,
                "40-30": 0.8,
                "30-40": 0.9,
                "40-40": 1.0,
            }

            # Assign base weight
            pressure_df["Weight"] = pressure_df["Game Score"].map(weight_map)

            # Determine win/loss
            pressure_df["Win"] = (
                pressure_df["C1: Point Winner"].astype(str).str.strip().str.lower()
                == str(player).strip().lower()
            )

            # Apply sign (+ for win, - for loss)
            pressure_df["Value"] = pressure_df["Weight"] * pressure_df["Win"].map({
                True: 1,
                False: -1
            })

            # Assign colors
            pressure_df["Color"] = pressure_df["Win"].map({
                True: "#22c55e",   # green
                False: "#ef4444"   # red
            })

            st.bar_chart(
                pressure_df,
                x="Point #",
                y="Value",
                color="Color"
            )

            st.caption("Bar height = pressure weight • Green = won, Red = lost")

        else:
            st.info("No pressure points found.")