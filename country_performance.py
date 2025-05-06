import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv("athlete_events.csv")

def show_country_performance():
    df = load_data()

    st.title("Country-wise Performance")

    years = sorted(df['Year'].dropna().unique())
    countries = sorted(df['Team'].dropna().unique())
    sports = sorted(df['Sport'].dropna().unique())
    seasons = sorted(df['Season'].dropna().unique())
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_year = st.selectbox("Select Year", options=["All"] + years)
    with col2:
        selected_country = st.selectbox("Select Country", options=["All"] + countries)
    with col3:
        selected_sport = st.selectbox("Select Sport", options=["All"] + sports)
    with col4:
        selected_season = st.selectbox("Select Season",options=['All']+seasons)
    

    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['Team'] == selected_country]
    if selected_sport != "All":
        filtered_df = filtered_df[filtered_df['Sport'] == selected_sport]
    if selected_season != 'All':
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    
    
    medal_data = filtered_df.dropna(subset=['Medal'])
    medal_count = medal_data.groupby('Team')['Medal'].count().sort_values(ascending=False).head(10)
    try:
        st.subheader("Top 10 Countries by Medal Count")
        fig, ax = plt.subplots()
        medal_count.plot(kind='bar', ax=ax)
        ax.set_xlabel("Country")
        ax.set_ylabel("Number of Medals")
        ax.set_title("Top 10 Countries by Medal Count")
        st.pyplot(fig)
    except Exception as filter_error:
        st.error(f"Are your sure **{selected_country}** played in the year **{selected_year}** and competed in **{selected_sport}** sports?")
        #st.exception(filter_error)
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df)
