import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("olympic_data_preprocessed.csv")

def show_home():
    df = load_data()
    st.title("🏅 Olympic Sprint Dashboard")
    st.markdown("""
    Welcome to the **Olympic Sprint Dashboard** — your interactive platform for exploring over a century of Olympic history through data.

    ### 📊 What You Can Do Here:

    - **Country Performance:** Dive into how nations have performed across Olympic Games with medal trends and rankings.
    - **Medal Prediction:** Use athlete bio features to predict the likelihood of winning a medal using machine learning.
    - **Athlete Bio Insights:** Compare age, height, and weight of medalists vs. non-medalists and explore patterns across athlete profiles.
    - **Regional Participation:** Track how different continents have participated in the Olympics over time, including Summer and Winter seasons.
    - **Medal Map Explorer:** Explore total medals by country using an animated world map, including season-wise and time-based comparisons.

    ---
    📁 **Data Source:** Preprocessed Olympic athlete and event data  
    📅 **Coverage:** 1896 to 2016 (with predictions up to 2032)  
    👤 **Developed by:** [Your Name or Team Name]
    """)
    st.write("Explore the historical Olympic athletes data from 1896 to 2016.")
    st.dataframe(df)
