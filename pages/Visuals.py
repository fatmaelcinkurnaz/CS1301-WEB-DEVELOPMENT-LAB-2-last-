# This creates the page for displaying data visualizations.

import streamlit as st
import json
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")






# PART 1: GRAPHS FROM data.json

# Load data from JSON
with open("data.json", "r") as infile:
    data = json.load(infile)

players = data[0]["Player"]
ratings = data[0]["Rating"]
birth_years = data[0]["Birth Year"]

# GRAPH 1: Rating differences
st.subheader("How Close Are the Players' Ratings?")

lowest_rating = min(ratings)

player_data = sorted(
    zip(players, ratings),
    key=lambda item: item[1],
    reverse=True
)

sorted_players = [item[0] for item in player_data]
sorted_ratings = [item[1] for item in player_data]
rating_gaps = [rating - lowest_rating for rating in sorted_ratings]

fig1 = px.bar(
    x=rating_gaps,
    y=sorted_players,
    orientation="h",
    text=rating_gaps,
    title="Rating Advantage Compared with the Lowest-Rated Player",
    labels={
        "x": "Rating Points Above the Lowest Rating",
        "y": "Chess Player"
    }
)

fig1.update_traces(textposition="outside")
fig1.update_layout(
    yaxis={"autorange": "reversed"},
    xaxis={"rangemode": "tozero"},
    showlegend=False
)

st.plotly_chart(fig1, use_container_width=True)

st.caption(
    "Each bar shows how many rating points a player has "
    "above the lowest rating in this dataset."
)

# GRAPH 2: Interactive birth year vs. rating
st.subheader("Does Birth Year Relate to Chess Rating?")

if "minimum_rating" not in st.session_state:
    st.session_state["minimum_rating"] = min(ratings)

minimum_rating = st.slider(
    "Show players with at least this rating:",
    min_value=min(ratings),
    max_value=max(ratings),
    value=st.session_state["minimum_rating"],
    step=5,
    key="minimum_rating"
)

filtered_data = [
    (player, rating, year)
    for player, rating, year in zip(players, ratings, birth_years)
    if rating >= minimum_rating
]

if filtered_data:
    filtered_players = [item[0] for item in filtered_data]
    filtered_ratings = [item[1] for item in filtered_data]
    filtered_birth_years = [item[2] for item in filtered_data]

    fig2 = px.scatter(
        x=filtered_birth_years,
        y=filtered_ratings,
        text=filtered_players,
        title="Player Birth Year vs. FIDE Rating",
        labels={
            "x": "Birth Year",
            "y": "FIDE Rating"
        },
        hover_name=filtered_players
    )

    fig2.update_traces(textposition="top center")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No players match the selected rating threshold.")



# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---


import pandas as pd

st.divider()
st.title("Community Chess Data")

try:
    csv_data = pd.read_csv("data.csv")

    if not csv_data.empty:

        st.write("Explore the chess ratings submitted by users.")

        # GRAPH 3: Static Histogram
        st.subheader("How Are the Ratings Distributed?")

        fig3 = px.histogram(
            csv_data,
            x="Rating",
            nbins=8,
            title="Distribution of FIDE Ratings Among Survey Participants",
            labels={
                "Rating": "FIDE Rating",
                "count": "Number of Players"
            }
        )

        fig3.update_layout(
            xaxis_title="FIDE Rating",
            yaxis_title="Number of Players"
        )

        st.plotly_chart(fig3, use_container_width=True)

        # GRAPH 4: Interactive Rating Filter
        st.subheader("Explore Players by Rating")

        if "rating_threshold" not in st.session_state:
            st.session_state["rating_threshold"] = int(
                csv_data["Rating"].min()
            )

        rating_threshold = st.slider(
            "Select the minimum FIDE rating:",
            min_value=int(csv_data["Rating"].min()),
            max_value=int(csv_data["Rating"].max()),
            value=st.session_state["rating_threshold"],
            step=1,
            key="rating_threshold"
        )

        filtered_data = csv_data[
            csv_data["Rating"] >= rating_threshold
        ]

        # EXTRA CREDIT: Summary Statistics

        if not filtered_data.empty:

            mean_rating = filtered_data["Rating"].mean()
            median_rating = filtered_data["Rating"].median()

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Mean FIDE Rating",
                    value=f"{mean_rating:.2f}"
                )

            with col2:
                st.metric(
                    label="Median FIDE Rating",
                    value=f"{median_rating:.2f}"
                )

        # Display filtered data

        fig4 = px.bar(
            filtered_data,
            x="Player",
            y="Rating",
            title="FIDE Ratings of Selected Players",
            labels={
                "Player": "Chess Player",
                "Rating": "FIDE Rating"
            }
        )

        st.plotly_chart(fig4, use_container_width=True)

        st.write(
            f"Number of players matching the selected rating: {len(filtered_data)}"
        )

    else:
        st.warning("No survey data has been collected yet.")

except (FileNotFoundError, pd.errors.EmptyDataError):
    st.warning("No survey data has been collected yet.")

