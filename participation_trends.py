import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_participation_trends():
    
    st.title("👥 Athlete Participation Over Time by Gender")
    st.markdown("Visualizing the number of male and female athletes across Summer and Winter Olympics.")

    # Load data
    df_olympic = pd.read_csv('olympic_data_preprocessed.csv')
    
    df_olympic['Year'] = pd.to_datetime(df_olympic['Year'], format='%Y')
    # --- Overall Athlete Participation by Season (Time Series) ---

    st.subheader("📊 Total Olympic Athlete Participation Over Time")

    # Grouping by year and season
    summer_athletes = df_olympic[df_olympic['Season'] == 'Summer'].groupby(df_olympic['Year'].dt.year)['ID'].nunique()
    winter_athletes = df_olympic[df_olympic['Season'] == 'Winter'].groupby(df_olympic['Year'].dt.year)['ID'].nunique()

    # Convert to time series
    summer_ts = pd.Series(summer_athletes.values,
                        index=pd.to_datetime(summer_athletes.index, format='%Y'),
                        name='SummerAthletes')

    winter_ts = pd.Series(winter_athletes.values,
                        index=pd.to_datetime(winter_athletes.index, format='%Y'),
                        name='WinterAthletes')

    # Plot the time series
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(summer_ts, marker='o', linestyle='-', label='Summer Olympics')
    ax.plot(winter_ts, marker='o', linestyle='--', label='Winter Olympics')
    ax.set_title("Number of Unique Athletes by Olympic Season")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Athletes")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("""
    ### 📌 Insight
    - The **Summer Olympics** consistently attract **3–4x more athletes** than the Winter Games.
    - Both seasons show sharp growth in participation, especially from the **1980s onward**.
    - This reflects expanding global inclusion and increased country participation.
    """)

    # Group by year, season, and gender
    gender_counts = df_olympic.groupby(['Year', 'Season', 'Sex'])['ID'].nunique().unstack(fill_value=0)

    # Separate Summer and Winter
    summer_gender = gender_counts.loc[(slice(None), 'Summer'), :]
    winter_gender = gender_counts.loc[(slice(None), 'Winter'), :]

    # Plot setup
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # Summer plot
    axes[0].plot(summer_gender.index.get_level_values(0), summer_gender['F'], marker='o', label='Female')
    axes[0].plot(summer_gender.index.get_level_values(0), summer_gender['M'], marker='o', label='Male')
    axes[0].set_title('Summer Olympics: Athlete Gender Distribution')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Number of Athletes')
    axes[0].legend()
    axes[0].grid(True)

    # Label points (Summer)
    for i, year in enumerate(summer_gender.index.get_level_values(0)):
        if i % 2 == 0:
            axes[0].text(year, summer_gender.loc[(year, 'Summer'), 'F'], str(summer_gender.loc[(year, 'Summer'), 'F']), ha='center', va='bottom')
            axes[0].text(year, summer_gender.loc[(year, 'Summer'), 'M'], str(summer_gender.loc[(year, 'Summer'), 'M']), ha='center', va='bottom')

    # Winter plot
    axes[1].plot(winter_gender.index.get_level_values(0), winter_gender['F'], marker='o', label='Female')
    axes[1].plot(winter_gender.index.get_level_values(0), winter_gender['M'], marker='o', label='Male')
    axes[1].set_title('Winter Olympics: Athlete Gender Distribution')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Number of Athletes')
    axes[1].legend()
    axes[1].grid(True)

    # Label points (Winter)
    for i, year in enumerate(winter_gender.index.get_level_values(0)):
        if i % 2 == 0:
            axes[1].text(year, winter_gender.loc[(year, 'Winter'), 'F'], str(winter_gender.loc[(year, 'Winter'), 'F']), ha='center', va='bottom')
            axes[1].text(year, winter_gender.loc[(year, 'Winter'), 'M'], str(winter_gender.loc[(year, 'Winter'), 'M']), ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("## 📌 Key Insights from Gender Participation Trends")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("☀️ Summer Olympics")
        st.markdown("""
        - Male participation peaked at **~6600 athletes** in the 1990s.
        - **Female numbers were very low** until the 1980s.
        - From **1984 onward**, female participation **grew rapidly**, reaching **5000+ by 2016**.
        - ✅ By 2016, gender parity was nearly achieved in the Summer Olympics.
        """)

    with col2:
        st.subheader("❄️ Winter Olympics")
        st.markdown("""
        - Started with **only 12 female athletes** in 1924.
        - Steady growth from 1980s onward; over **1000 women competed by 2014**.
        - Male participation rose gradually, reaching **~1600 athletes**.
        - ✅ Gender gap remains, but has **narrowed significantly** in recent decades.
        """)

    st.markdown("---")

    st.markdown("""
    ### 🟰 **Overall Takeaway**
    The **1980s to 2000s** marked a global shift toward gender inclusion in sports.  
    This rise in female participation reflects **policy reforms**, **social progress**, and **increased investment** in women's athletics.
    """)

