import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
def show_regional_participation():
    st.title("Olympic Medal Share % Forecasting by Continent")

    # -------------------------------
    # STEP 1: Read data
    # -------------------------------
    # Replace with your CSV file path
    df = pd.read_csv("athlete_events.csv")

    # -------------------------------
    # STEP 2: Map NOC to continent
    # -------------------------------
    noc_to_continent = {
        'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
        'BRA': 'South America', 'ARG': 'South America', 'COL': 'South America',
        'GBR': 'Europe', 'FRA': 'Europe', 'GER': 'Europe', 'ITA': 'Europe', 'ESP': 'Europe', 
        'RUS': 'Europe', 'UKR': 'Europe', 'NED': 'Europe', 'SWE': 'Europe', 'SUI': 'Europe',
        'CHN': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia', 'IND': 'Asia',
        'AUS': 'Oceania', 'NZL': 'Oceania',
        'RSA': 'Africa', 'KEN': 'Africa', 'NGR': 'Africa', 'EGY': 'Africa'
    }

    df['Continent'] = df['NOC'].map(noc_to_continent)
    df = df.dropna(subset=['Continent'])  # Drop countries without continent mapping

    # -------------------------------
    # STEP 3: Compute medal counts per continent & year
    # -------------------------------
    df_medals = df[df['Medal'].notna()]  # Only rows where a medal was won

    medal_summary = df_medals.groupby(['Year', 'Continent']).size().reset_index(name='Medal_Count')

    # -------------------------------
    # STEP 4: Compute medal share %
    # -------------------------------
    medal_summary['Total_Medals_Per_Year'] = medal_summary.groupby('Year')['Medal_Count'].transform('sum')
    medal_summary['Medal_Share_Percent'] = (medal_summary['Medal_Count'] / medal_summary['Total_Medals_Per_Year']) * 100

    # -------------------------------
    # STREAMLIT UI
    # -------------------------------
    continent = st.selectbox(
        "Select a Continent",
        medal_summary['Continent'].unique()
    )

    st.subheader(f"Medal Share % Time Series: {continent}")

    subset = medal_summary[medal_summary['Continent'] == continent].sort_values('Year')
    years = subset['Year'].reset_index(drop=True)
    values = subset['Medal_Share_Percent'].reset_index(drop=True)

    # -------------------------------
    # STEP 5: Plot actual data
    # -------------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines+markers',
        name='Actual Medal Share %'
    ))

    # -------------------------------
    # STEP 6: ARIMA Forecasting
    # -------------------------------
    train_years = years[:-2]
    train_values = values[:-2]

    validation_years = years[-2:]
    validation_values = values[-2:]

    forecast_years = [2028, 2032]

    try:
        # Train ARIMA
        model = ARIMA(train_values, order=(1, 1, 1))
        fitted_model = model.fit()

        validation_forecast = fitted_model.forecast(2)

        fig.add_trace(go.Scatter(
            x=validation_years,
            y=validation_forecast,
            mode='markers',
            marker=dict(color='orange', size=10, symbol='circle-open'),
            name='Validation Forecast'
        ))

        # Refit on full data
        final_model = ARIMA(values, order=(1, 1, 1))
        final_fitted = final_model.fit()
        final_forecast = final_fitted.forecast(2)

        fig.add_trace(go.Scatter(
            x=forecast_years,
            y=final_forecast,
            mode='markers',
            marker=dict(color='red', size=12, symbol='x'),
            name='Forecast 2028 & 2032'
        ))

        st.write(f"**2028 Forecast**: {final_forecast.values[0]:.2f}%")
        st.write(f"**2032 Forecast**: {final_forecast.values[1]:.2f}%")

        # Optional: Show validation MAE
        mae = mean_absolute_error(validation_values, validation_forecast)
        st.write(f"**Validation MAE**: {mae:.2f}")

    except Exception as e:
        st.error(f"ARIMA model failed: {e}")

    fig.update_layout(
        title=f"ARIMA Medal Share % Forecast for {continent}",
        xaxis_title="Year",
        yaxis_title="Medal Share (%)",
        hovermode="x unified"
    )

    st.plotly_chart(fig)
