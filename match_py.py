# -*- coding: utf-8 -*-
"""Match.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XKizHkhBYvqISyQlmzgEN3OW49fSgswN
"""

import logging
import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

# Suppress specific warnings
logging.getLogger("streamlit").setLevel(logging.ERROR)

# Define the main function for cricket match prediction
def cricket_match_prediction():
    st.title('Cricket Match Win Prediction')

    # Sidebar to select between Input and Output screen
    page = st.radio("Select Page", ("Input Data", "Prediction Result"))

    # If the user selects the Input Data page
    if page == "Input Data":
        st.header("Enter Match Statistics")

        # User inputs for match features
        team_batting_strength = st.number_input('Team Batting Strength (Runs)', min_value=100, max_value=400, value=250)
        team_bowling_strength = st.number_input('Team Bowling Strength (Wickets)', min_value=0, max_value=20, value=10)
        opponent_batting_strength = st.number_input('Opponent Batting Strength (Runs)', min_value=100, max_value=400, value=220)
        opponent_bowling_strength = st.number_input('Opponent Bowling Strength (Wickets)', min_value=0, max_value=20, value=8)
        weather_conditions = st.selectbox('Weather Conditions', ['Clear', 'Cloudy', 'Rainy'])

        # Encoding weather condition as numerical value
        weather_conditions_map = {'Clear': 1, 'Cloudy': 2, 'Rainy': 3}
        weather_condition_value = weather_conditions_map[weather_conditions]

        # Save the user inputs in session state
        st.session_state.team_batting_strength = team_batting_strength
        st.session_state.team_bowling_strength = team_bowling_strength
        st.session_state.opponent_batting_strength = opponent_batting_strength
        st.session_state.opponent_bowling_strength = opponent_bowling_strength
        st.session_state.weather_condition_value = weather_condition_value

        # Proceed to the next page for prediction
        if st.button('Next: Get Prediction'):
            st.session_state.page = 'Prediction Result'
            st.experimental_rerun()

    # If the user selects the Prediction Result page
    elif page == "Prediction Result":
        st.header("Prediction Result")

        # Sample match dataset (replace with actual data)
        data = {
            'team_batting_strength': [250, 230, 300, 270, 200, 180, 260, 220, 240, 210],
            'team_bowling_strength': [10, 9, 15, 12, 8, 6, 11, 10, 14, 9],
            'opponent_batting_strength': [240, 220, 310, 260, 210, 190, 250, 230, 240, 220],
            'opponent_bowling_strength': [9, 8, 16, 12, 7, 5, 13, 10, 15, 9],
            'weather_conditions': [1, 2, 3, 1, 1, 2, 1, 2, 3, 1],  # 1: Clear, 2: Cloudy, 3: Rainy
            'match_result': ['Win', 'Lose', 'Win', 'Win', 'Lose', 'Lose', 'Win', 'Lose', 'Win', 'Lose'],
        }

        df = pd.DataFrame(data)

        # Encode categorical labels (Win / Lose)
        label_encoder = LabelEncoder()
        df['match_result'] = label_encoder.fit_transform(df['match_result'])  # Win = 1, Lose = 0

        # Features and target
        X = df.drop('match_result', axis=1)
        y = df['match_result']

        # Train a KNN classifier
        knn_classifier = KNeighborsClassifier(n_neighbors=3)
        knn_classifier.fit(X, y)

        # Prepare the match data from session state
        match_data = pd.DataFrame({
            'team_batting_strength': [st.session_state.team_batting_strength],
            'team_bowling_strength': [st.session_state.team_bowling_strength],
            'opponent_batting_strength': [st.session_state.opponent_batting_strength],
            'opponent_bowling_strength': [st.session_state.opponent_bowling_strength],
            'weather_conditions': [st.session_state.weather_condition_value],
        })

        # Predict match outcome based on user input
        match_prediction = knn_classifier.predict(match_data)
        predicted_result = label_encoder.inverse_transform(match_prediction)

        # Display the result
        st.write(f"Predicted Match Outcome: {predicted_result[0]}")

        # Option to go back to input screen
        if st.button('Go Back to Input'):
            st.session_state.page = 'Input Data'
            st.experimental_rerun()


# Run the cricket match prediction function
if __name__ == "__main__":
    cricket_match_prediction()



