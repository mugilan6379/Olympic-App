
import streamlit as st
import pandas as pd
import plotly.express as px

def show_medal_choropleth():
    st.title("🌍 Olympic Medal Distribution Map")
    st.markdown("Visualize the total Olympic medals by country and over time, including distinctions by Summer and Winter seasons.")

    # Load the dataset
    try:
        df = pd.read_csv('olympic_data_preprocessed.csv')
    except Exception as e:
        st.error("Failed to load dataset.")
        st.exception(e)
        return

    # Tab layout for three views
    tab1, tab2, tab3 = st.tabs(["🌐 Total Medals (Static)", "📆 Animated Over Time", "❄️ Summer vs Winter"])

    with tab1:
        country_medals = df.groupby('NOC')['Medal'].count().reset_index()
        fig1 = px.choropleth(country_medals, locations='NOC', locationmode='ISO-3',
                            color='Medal', color_continuous_scale='Viridis',
                            title='Total Olympic Medals by Country')
        st.plotly_chart(fig1)

    with tab2:
        country_medals_year = df.groupby(['NOC', 'Year'])['Medal'].count().reset_index()
        fig2 = px.choropleth(country_medals_year, locations='NOC', locationmode='ISO-3',
                            color='Medal', color_continuous_scale='Viridis',
                            animation_frame='Year',
                            title='Total Olympic Medals by Country Over Time')
        st.plotly_chart(fig2)

    with tab3:
        df['Season_NOC'] = df['Season'] + '_' + df['NOC']
        season_country_medals_year = df.groupby(['Season_NOC', 'Year'])['Medal'].count().reset_index()
        season_country_medals_year[['Season', 'NOC']] = season_country_medals_year['Season_NOC'].str.split('_', expand=True)
        fig3 = px.choropleth(season_country_medals_year, locations='NOC', locationmode='ISO-3',
                            color='Medal', color_continuous_scale='Viridis',
                            animation_frame='Year',
                            facet_col='Season',
                            title='Total Olympic Medals by Country and Season Over Time')
        st.plotly_chart(fig3)
