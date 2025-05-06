# main.py
import streamlit as st
from home import show_home
from country_performance import show_country_performance
from predict_medal import show_prediction_page
from athlete_bio_insights import show_bio_insights
from forecast_model import forecast_medals 
from mens_100m_analysis import show_mens_100m_analysis
from participation_trends import show_participation_trends
from regional_participation import show_regional_participation
from country_represent import show_country_representation_performance
from medal_choropleth import show_medal_choropleth


# Sidebar navigation
st.sidebar.title("Olympic Sprint Dashboard")
page = st.sidebar.radio("Go to", [
    "Home",
    "Country Performance",
    "Participation Trends",
    "Men's 100m Sprint Analysis" ,
    "Regional Participation",
    "Country Representation & Performance",
    "Medal Map Explorer"
])
# Route to selected page
try:
    if page == "Home":
        show_home()
    elif page == "Country Performance":
        show_country_performance()
    elif page == "Men's 100m Sprint Analysis":
        show_mens_100m_analysis() 
    elif page == "Participation Trends":
        show_participation_trends()
    elif page == "Regional Participation":
        show_regional_participation()
    elif page == "Country Representation & Performance":
        show_country_representation_performance()
    elif page == "Medal Map Explorer":
        show_medal_choropleth()

except Exception as e:
    st.error("Oops! Something went wrong while loading this page. Please try adjusting your filters or refresh the app.")
    st.exception(e)
