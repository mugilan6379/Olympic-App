import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_csv("athlete_events.csv")

def show_bio_insights():
    st.title("🔍 Athlete Bio Trait Insights")
    st.write("Compare bio traits like age, height, and weight between medalists and non-medalists.")

    df = load_data()
    df = df.dropna(subset=['Age', 'Height', 'Weight'])
    df['Medal_Won'] = df['Medal'].notna().astype(int)

    st.subheader("📊 Boxplots of Bio Traits")

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    sns.boxplot(data=df, x='Medal_Won', y='Age', ax=axs[0])
    axs[0].set_title('Age vs Medal Status')
    axs[0].set_xticklabels(['No Medal', 'Medal'])

    sns.boxplot(data=df, x='Medal_Won', y='Height', ax=axs[1])
    axs[1].set_title('Height vs Medal Status')
    axs[1].set_xticklabels(['No Medal', 'Medal'])

    sns.boxplot(data=df, x='Medal_Won', y='Weight', ax=axs[2])
    axs[2].set_title('Weight vs Medal Status')
    axs[2].set_xticklabels(['No Medal', 'Medal'])

    st.pyplot(fig)

    st.subheader("📌 Observations")
    st.markdown("""
    - Medalists tend to have a slightly different age and physical build compared to non-medalists.
    - You can use these trends to profile ideal athlete traits for specific events.
    - Outliers may represent exceptional athletes or unique training backgrounds.
    """)
