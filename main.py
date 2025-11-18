import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------
# 1. PAGE CONFIG
# -------------------------------------
st.set_page_config(page_title="Zomato Data Dashboard", layout="wide")
st.title("📊 Zomato Bangalore Restaurants Dashboard")

# -------------------------------------
# 2. LOAD DATA
# -------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("zomato.csv")

df = load_data()

st.sidebar.header("Filters")

# -------------------------------------
# 3. FILTERS
# -------------------------------------
# Cuisine filter
all_cuisines = sorted(set(",".join(df['cuisines'].dropna()).split(",")))
cuisine_filter = st.sidebar.multiselect("Select Cuisines", all_cuisines)

# Avg Cost filter
cost_limit = st.sidebar.slider("Max Approx Cost for Two", 0, 3000, 800)

# Apply filters
filtered_df = df.copy()
if cuisine_filter:
    filtered_df = filtered_df[filtered_df["cuisines"].str.contains("|".join(cuisine_filter), case=False, na=False)]

filtered_df = filtered_df[filtered_df["approx_cost(for two people)"] <= cost_limit]

# -------------------------------------
# 4. METRICS
# -------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Restaurants", len(filtered_df))
c2.metric("Avg Rating", round(filtered_df["aggregate_rating"].mean(), 2))
c3.metric("Avg Cost for Two", int(filtered_df["approx_cost(for two people)"].mean()))
c4.metric("Online Delivery %", round((filtered_df['online_order']=="Yes").mean()*100, 2))

# -------------------------------------
# 5. TOP RESTAURANTS TABLE
# -------------------------------------
st.subheader("🏆 Top Rated Restaurants")
top_df = filtered_df.sort_values(by="aggregate_rating", ascending=False).head(20)
st.dataframe(top_df[["name", "location", "cuisines", "aggregate_rating", "approx_cost(for two people)"]])

# -------------------------------------
# 6. VISUALIZATIONS
# -------------------------------------

st.subheader("🍛 Cuisine Distribution")
fig1, ax1 = plt.subplots()
filtered_df["cuisines"].dropna().str.split(",").explode().value_counts().head(15).plot(kind='bar', ax=ax1)
ax1.set_ylabel("Count")
ax1.set_xlabel("Cuisine")
st.pyplot(fig1)

st.subheader("⭐ Rating Distribution")
fig2, ax2 = plt.subplots()
filtered_df["aggregate_rating"].plot(kind="hist", bins=20, ax=ax2)
ax2.set_xlabel("Ratings")
st.pyplot(fig2)

st.subheader("📍 Restaurant Count by Location")
fig3, ax3 = plt.subplots(figsize=(10, 4))
filtered_df["location"].value_counts().head(20).plot(kind="bar", ax=ax3)
ax3.set_ylabel("Count")
ax3.set_xlabel("Location")
st.pyplot(fig3)

# -------------------------------------
# 7. RAW DATA
# -------------------------------------
st.subheader("📄 Raw Dataset Preview")
st.dataframe(filtered_df)
