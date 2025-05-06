import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def show_mens_100m_analysis():
    st.title("🏃 Men's 100m Sprint: Olympic History, Bio Insights & Medal Prediction")

    # Load data
    try:
        df = pd.read_csv("athlete_events.csv")
    except Exception as e:
        st.error("Failed to load dataset.")
        st.exception(e)
        return

    # Filter for Men's 100m Sprint
    event_df = df[(df["Event"] == "Athletics Men's 100 metres") & (df["Sport"] == "Athletics")].copy()

    if event_df.empty:
        st.warning("No data found for Men's 100m Sprint.")
        return

    st.markdown("## 🕰️ Olympic History")
    st.markdown("""
    The Men's 100m Sprint is often called the **Fastest Man on Earth** race.  
    From Jesse Owens to Usain Bolt, this event has symbolized national pride and peak athleticism.
    """)

    # Medal tally by country
    st.subheader("🥇 Top 10 Countries by Men's 100m Sprint Medals")
    medal_tally = (
        event_df[event_df["Medal"].notna()]
        .groupby("NOC")["Medal"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    medal_tally.sort_values(ascending=True).plot(kind='barh', ax=ax, color='skyblue')
    ax.set_xlabel("Number of Medals")
    ax.set_ylabel("Country (NOC Code)")
    ax.set_title("Top 10 Countries by Total Medals (Men's 100m Sprint)")
    for i, v in enumerate(medal_tally.sort_values(ascending=True)):
        ax.text(v + 0.5, i, str(v), color='black', va='center')
    st.pyplot(fig)

    # Bio insights
    st.markdown("## 📊 Bio Characteristics of Medalists vs Non-Medalists")

    event_df["is_medalist"] = event_df["Medal"].notna().astype(int)
    bio_df = event_df.dropna(subset=["Age", "Height", "Weight"])

    st.write(f"Number of valid athletes for analysis: {len(bio_df)}")

    if len(bio_df) < 50:
        st.error("Not enough bio data available for modeling and visualization.")
        return

    fig, axs = plt.subplots(1, 3, figsize=(18, 4))
    sns.boxplot(data=bio_df, x="is_medalist", y="Age", ax=axs[0])
    sns.boxplot(data=bio_df, x="is_medalist", y="Height", ax=axs[1])
    sns.boxplot(data=bio_df, x="is_medalist", y="Weight", ax=axs[2])

    axs[0].set_title("Age Comparison")
    axs[1].set_title("Height (cm) Comparison")
    axs[2].set_title("Weight (kg) Comparison")

    axs[0].set_xlabel("Medal Status")
    axs[1].set_xlabel("Medal Status")
    axs[2].set_xlabel("Medal Status")

    axs[0].set_ylabel("Age")
    axs[1].set_ylabel("Height (cm)")
    axs[2].set_ylabel("Weight (kg)")

    for ax in axs:
        ax.set_xticklabels(["No Medal", "Medalist"])

    plt.suptitle("Athlete Bio Characteristics by Medal Outcome", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("## 🔍 Insights from Bio Characteristics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("**Age**")
        st.markdown("""
        - Most sprinters fall between **22–28 years**
        - Medalists are concentrated around **24–27**
        - ✅ **Peak age range** for performance: *24–27*

        """)

    with col2:
        st.subheader("**Height**")
        st.markdown("""
        - Medalists are generally **taller**
        - Median height: **181–183 cm** (medalists) vs ~179 cm (non)
        - ✅ **Taller sprinters benefit from longer strides**
        """)

    with col3:
        st.subheader("**Weight**")
        st.markdown("""
        - Medalists weigh slightly **more**
        - Median: **75–78 kg**, indicating high lean mass
        - ✅ **Power-to-weight ratio critical for explosiveness**
        """)

    st.markdown("---")

    st.markdown("""
    ### 🎯 Summary
    The ideal Men's 100m Olympic sprinter is typically:
    - **24–27 years old**
    - **181–183 cm tall**
    - **75–78 kg**, muscular build

    This closely aligns with legends like **Usain Bolt**.
    """)


    # Predictive model
    st.markdown("## 🧠 Medal Prediction Model")

    features = bio_df[["Age", "Height", "Weight"]]
    target = bio_df["is_medalist"]

    try:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)

        # preds = model.predict(X_test)
        # acc = accuracy_score(y_test, preds)
        # st.write(f"**Model Accuracy**: {acc:.2f}")
        # Make predictions and calculate accuracy
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        st.write('0 - No medal and 1 - Medal(any type)')
        st.write(f"**Model Accuracy**: {acc:.2f}")

        # Generate classification report as dict
        report_dict = classification_report(y_test, preds, output_dict=True)
        report_df = pd.DataFrame(report_dict).transpose()

        # Round for readability
        report_df = report_df.round(2)

        # Display in Streamlit as a table
        st.markdown("### 📊 Classification Report")
        st.dataframe(report_df)
    except Exception as e:
        st.error("Model training failed.")
        st.exception(e)
        return

    # User input prediction
    st.markdown("## 🎯 Try It Yourself: Predict Medal Chances")

    age = st.slider("Age", 15, 40, 25)
    height = st.slider("Height (cm)", 150, 210, 180)
    weight = st.slider("Weight (kg)", 50, 110, 75)

    user_input = pd.DataFrame([[age, height, weight]], columns=["Age", "Height", "Weight"])

    try:
        prediction = model.predict(user_input)[0]
        prob = model.predict_proba(user_input)[0][1]

        if prediction == 1:
            st.success(f"This athlete is **likely to win a medal**! (Probability: {prob:.2f})")
        else:
            st.warning(f"The Probability to win the medal with the chosen characteristics: {prob:.2f})")
    except Exception as e:
        st.error("Prediction failed.")
        st.exception(e)
