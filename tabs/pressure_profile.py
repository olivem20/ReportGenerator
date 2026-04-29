import streamlit as st
import pandas as pd

def clutch_card(score: float):
    if score >= 1.5:
        bg = "rgba(34, 197, 94, 0.18)"
        border = "#22c55e"
        label = "Strong under pressure"
        desc = "Won more high-leverage points than lost, especially on the biggest moments."
    elif score > 0:
        bg = "rgba(132, 204, 22, 0.18)"
        border = "#84cc16"
        label = "Slightly positive"
        desc = "Came out ahead in pressure points overall."
    elif score == 0:
        bg = "rgba(148, 163, 184, 0.18)"
        border = "#94a3b8"
        label = "Even"
        desc = "Split high-leverage points evenly."
    elif score > -1.5:
        bg = "rgba(249, 115, 22, 0.18)"
        border = "#f97316"
        label = "Slightly negative"
        desc = "Lost slightly more pressure points than won."
    else:
        bg = "rgba(239, 68, 68, 0.18)"
        border = "#ef4444"
        label = "Needs improvement"
        desc = "Lost too many of the highest-leverage points in the match."

    st.markdown(
        f"""
        <div style="
            background:{bg};
            border-left:6px solid {border};
            padding:18px 20px;
            border-radius:12px;
            margin-bottom:14px;
        ">
            <div style="font-size:16px; color:white; font-weight:600; margin-bottom:8px;">
                Clutch Score
            </div>
            <div style="font-size:40px; font-weight:800; color:white; line-height:1;">
                {score:.1f}
            </div>
            <div style="font-size:16px; color:white; font-weight:600; margin-top:10px;">
                {label}
            </div>
            <div style="font-size:14px; color:rgba(255,255,255,0.78); margin-top:8px;">
                {desc}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_pressure_profile(df, player):
    deuce_points = df[df["Deuce"].notna()].copy()

    deuce_points_played = len(deuce_points)

    deuce_points_won = len(
        deuce_points[deuce_points["C1: Point Winner"] == player]
    )

    win_pct = (deuce_points_won / deuce_points_played) * 100 if deuce_points_played > 0 else 0


    st.metric(
        "Deuce Points Won",
        f"{deuce_points_won}/{deuce_points_played} ({win_pct:.0f}%)"
    )



    st.subheader("Deuce Point Outcomes")

    cols_per_row = 3  # 👈 change this (3 or 4 works best)

    rows = [
        deuce_points.iloc[i:i + cols_per_row]
        for i in range(0, len(deuce_points), cols_per_row)
    ]


    for row_df in rows:
        cols = st.columns(len(row_df))

        for col, (_, row) in zip(cols, row_df.iterrows()):
            deuce_count = row_df.index.get_loc(row.name) + 1
            first = int(row["Match Score"][0])
            second = int(row["Match Score"][2])

            set_number = first + second + 1
            winner = row["C1: Point Winner"]
            player_won = str(winner).strip().lower() == str(player).strip().lower()

            card_bg = "rgba(34, 197, 94, 0.12)" if player_won else "rgba(239, 68, 68, 0.12)"
            card_border = "#22c55e" if player_won else "#ef4444"
            result_text = "WON" if player_won else "LOST"

            def clean_value(val):
                return "" if pd.isna(val) else str(val)

            if pd.notna(row.get("C2: Last Shot Winner")):
                end_type = row.get("D1: Winner Type")
                shot = clean_value(row.get("D3: Shot Winner"))
                spin = clean_value(row.get("D2: Spin Winner"))

            elif pd.notna(row.get("C3: Last Shot Unforced Error")):
                end_type = row.get("E1: Error Type")
                if end_type == "Double Fault":
                    shot = "&nbsp;"
                    spin = ""
                else:
                    player_won = str(winner).strip().lower() == str(player).strip().lower()
                    if end_type == "Unforced Error":
                        if player_won:
                            end_type = "Opponent Unforced Error"
                        else:
                            end_type = "Unforced Error"
                    shot = clean_value(row.get("E2: Shot Error"))
                    spin = clean_value(row.get("E3: Spin Error"))

            else:
                end_type = "Other"
                shot = "&nbsp;"
                spin = " "

            col.markdown(
                f"""
                <div style="
                    background:{card_bg};
                    border-left:6px solid {card_border};
                    padding:12px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                <div style="font-size:14px; font-weight:700;">
                    Set {set_number}, {row["Set Score"]} • {result_text}
                </div>
                <div style="font-size:12px;">
                    {end_type}
                </div>
                <div style="font-size:12px;">
                    {spin} {shot}
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

  
    deuce_points = df[df["Deuce"].notna()].copy()

    c = st.container()
    with c:
        st.subheader("Weighted Pressure Points")

        pressure_scores = ["30-30", "30-40", "40-30", "40-40"]
        pressure_df = df[df["Game Score"].isin(pressure_scores)].copy()
        clutch_score = 0.0
        if len(pressure_df) > 0:
            pressure_df = pressure_df.reset_index(drop=True)
            pressure_df["Point #"] = range(1, len(pressure_df) + 1)
            pressure_df["Point #"] = pressure_df["Point #"].astype(str).str.zfill(2)
            
            pressure_df["Label"] = (
                pressure_df["Point #"].astype(str)
                + ". "
                + pressure_df["Set Score"].astype(str)
                + " | "
                + pressure_df["Game Score"].astype(str)
            )

            weight_map = {
                "30-30": 0.3,
                "40-30": 0.5,
                "30-40": 0.7,
                "40-40": 1.0,
            }

            pressure_df["Weight"] = pressure_df["Game Score"].map(weight_map)

            pressure_df["Win"] = (
                pressure_df["C1: Point Winner"].astype(str).str.strip().str.lower()
                == str(player).strip().lower()
            )

            pressure_df["Value"] = pressure_df["Weight"] * pressure_df["Win"].map({
                True: 1,
                False: -1
            })

            pressure_df["Color"] = pressure_df["Win"].map({
                True: "#22c55e",
                False: "#ef4444"
            })

            clutch_score = pressure_df["Value"].sum()
            clutch_card(clutch_score)
            st.bar_chart(
                pressure_df,
                x="Label",
                y="Value",
                color="Color"
            )

            st.caption("Bar height = pressure weight • Green = won, Red = lost")
        else:
            clutch_card(clutch_score)
            st.info("No pressure points found.")


    