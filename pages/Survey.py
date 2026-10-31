# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.


import streamlit as st
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Chess Performance Survey ♟️")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):

    player_input = st.text_input("Enter your chess player name:")
    rating_input = st.text_input("Enter your FIDE rating:")

    submitted = st.form_submit_button("Submit Data")

    if submitted:

        if player_input.strip() == "" or rating_input.strip() == "":
            st.error("Please fill out both fields.")

        elif not rating_input.strip().isdigit():
            st.error("Please enter a valid numerical rating.")

        else:
            new_data = pd.DataFrame({
                "Player": [player_input.strip()],
                "Rating": [int(rating_input)]
            })

            file_exists = os.path.exists("data.csv") and os.path.getsize("data.csv") > 0

            new_data.to_csv(
                "data.csv",
                mode="a",
                header=not file_exists,
                index=False
            )

            st.success("Your data has been submitted!")
            st.write(f"Player: **{player_input}**")
            st.write(f"FIDE Rating: **{rating_input}**")


# DATA DISPLAY
st.divider()
st.header("Current Chess Performance Dataset")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)

else:
    st.info("No data has been collected yet.")
