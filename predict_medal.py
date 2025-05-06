import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

@st.cache_data
def load_data():
    return pd.read_csv("athlete_events.csv")

def show_prediction_page():
    st.title("🎯 Predict Medal Chance for an Athlete")

    df = load_data()
    df = df.dropna(subset=['Age', 'Height', 'Weight', 'Sex', 'Season', 'Event'])

    # Convert medal column to binary
    df['Medal_Won'] = df['Medal'].notna().astype(int)

    # Sidebar filters
    sex = st.selectbox("Select Sex", sorted(df['Sex'].unique()))
    season = st.selectbox("Select Season", sorted(df['Season'].unique()))
    event = st.selectbox("Select Event", sorted(df['Event'].unique()))

    # User input for athlete profile
    st.subheader("🏃 Athlete Info")
    age = st.slider("Age", 10, 60, 25)
    height = st.slider("Height (cm)", 120, 220, 175)
    weight = st.slider("Weight (kg)", 30, 150, 70)

    # Filter data based on sex, season, event
    event_df = df[
        (df['Sex'] == sex) &
        (df['Season'] == season) &
        (df['Event'] == event)
    ]

    if len(event_df) < 100:
        st.warning("⚠️ Not enough data to make a strong prediction for this event. Try a different one.")
        return

    # Prepare training data
    X = event_df[['Age', 'Height', 'Weight']]
    y = event_df['Medal_Won']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict for user input
    input_data = pd.DataFrame([[age, height, weight]], columns=['Age', 'Height', 'Weight'])
    probability = model.predict_proba(input_data)[0][1]

    st.success(f"🏅 Estimated Chance of Winning a Medal: **{probability * 100:.2f}%**")

    st.caption("Prediction based on historical athlete performance in similar events.")
