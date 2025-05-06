import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def forecast_medals():
    st.title("Olympic Medal Forecasting")

    # Load preprocessed dataset
    df = pd.read_csv("olympic_data_preprocessed.csv")

    # Country selector
    countries = df["Team"].dropna().unique()
    selected_country = st.selectbox("Select a Country", sorted(countries))

    # Number of Olympics to forecast
    steps = st.slider("Number of Future Olympics to Forecast", 1, 5, 3)

    # Filter and clean data for selected country
    country_df = df[df["Team"] == selected_country]

    # Count unique medals by event per year to avoid double-counting team medals
    medal_ts = (
        country_df
        .drop_duplicates(subset=["Year", "Event", "Medal"])
        .groupby("Year")["Medal"]
        .count()
        .reset_index()
    )

    # Convert year to datetime and set as index
    medal_ts["Year"] = pd.to_datetime(medal_ts["Year"], format="%Y")
    medal_ts.set_index("Year", inplace=True)
    medal_ts = medal_ts.asfreq('4YS')  # Olympic cycle frequency
    medal_ts.rename(columns={"Medal": "medal_count"}, inplace=True)

    if len(medal_ts.dropna()) < 5:
        st.warning("Not enough historical medal data to forecast for this country.")
        return

    # SARIMA model
    try:
        model = SARIMAX(
            medal_ts["medal_count"],
            order=(1, 1, 1),
            seasonal_order=(1, 0, 1, 3),
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        results = model.fit(disp=False)

        # Forecast future medals
        pred = results.get_forecast(steps=steps)
        forecast = pred.predicted_mean

        # Build future index for Olympics
        future_years = pd.date_range(
            start=medal_ts.index[-1] + pd.DateOffset(years=4),
            periods=steps,
            freq='4YS'
        )
        forecast.index = future_years

        # Plotting
        st.subheader(f"Forecasted Medals for {selected_country}")
        fig, ax = plt.subplots()
        ax.plot(medal_ts, label="Historical")
        ax.plot(forecast, label="Forecast", linestyle="--", marker="o")
        ax.set_title(f"SARIMA Forecast: {selected_country}")
        ax.set_ylabel("Medals")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Show forecast values
        st.write("Forecasted Medal Counts:")
        st.dataframe(forecast.rename("Forecasted Medals"))

    except Exception as e:
        st.error("Model fitting or forecasting failed.")
        st.exception(e)
