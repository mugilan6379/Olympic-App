import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_country_representation_performance():
        st.title("🏅Top Medal-Winning Countries")

        # Load data
        try:
            df = pd.read_csv("olympic_data_preprocessed.csv")
        except Exception as e:
            st.error("Failed to load dataset.")
            st.exception(e)
            return

        df['Year'] = pd.to_datetime(df['Year'], format='%Y').dt.year


        df_medals = df[df['Medal'].notnull()]  # Only medal-winning rows

        # Sidebar toggle
        selected_season = st.radio("🏟️ Choose Olympic Season", ["Summer", "Winter"])

        season_df = df_medals[df_medals['Season'] == selected_season]

        # Medal counts by country & medal type
        medal_counts = season_df.groupby(['Team', 'Medal']).size().unstack(fill_value=0)

        # Ensure all medal types exist as columns
        for medal in ['Gold', 'Silver', 'Bronze']:
            if medal not in medal_counts.columns:
                medal_counts[medal] = 0

        medal_counts['Total'] = medal_counts[['Gold', 'Silver', 'Bronze']].sum(axis=1)
        top_countries = medal_counts.sort_values('Total', ascending=False).head(10)

        # Plotting
        st.subheader(f"Top 10 Countries - {selected_season} Olympics (Stacked Medal Count)")
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.bar(top_countries.index, top_countries['Bronze'], label='Bronze', color='firebrick')
        ax.bar(top_countries.index, top_countries['Gold'], bottom=top_countries['Bronze'], label='Gold', color='orange')
        ax.bar(top_countries.index,
               top_countries['Silver'],
               bottom=top_countries['Bronze'] + top_countries['Gold'],
               label='Silver', color='gray')

        ax.set_xlabel("Country")
        ax.set_ylabel("Total Medal Count")
        ax.set_title(f"Top 10 Countries - {selected_season} Olympics (Stacked Medal Count)")
        ax.legend(title="Medal Type")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Optional: Table view
        st.markdown("### 📊 Medal Breakdown Table")
        st.dataframe(top_countries[['Gold', 'Silver', 'Bronze', 'Total']])

   