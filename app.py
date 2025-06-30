import streamlit as st
import sqlite3
import pandas as pd

# Set up the Streamlit page
st.set_page_config(page_title="Resume Score Explorer", layout="wide")
st.title("🔍 Resume Score Explorer")

# Connect to SQLite database
db_path = "data/resume_scores.db"
conn = sqlite3.connect(db_path)

# Sidebar for view selection
view_option = st.sidebar.selectbox(
    "Select View",
    ("Overall Scores", "Top Application Engineers", "Top Engineering Managers", "Top AZ Similarity")
)

# SQL queries for each view (load full set of 150 candidates)
queries = {
    "Overall Scores": "SELECT * FROM overall_scores ORDER BY \"New Total Score\" DESC",
    "Top Application Engineers": "SELECT * FROM top_application_engineers ORDER BY \"AppEngAZ Combined\" DESC",
    "Top Engineering Managers": "SELECT * FROM top_engineering_managers",
    "Top AZ Similarity": "SELECT * FROM top_az_similarity"
}



# Execute selected query
df = pd.read_sql_query(queries[view_option], conn)

# Display results
st.subheader(view_option)
st.dataframe(df, use_container_width=True)

# Optional filter section
with st.expander("🔧 Filter Options"):
    min_app_score = st.slider("Minimum Application Engineer JD Score", 0, 100, 60)
    min_mgr_score = st.slider("Minimum Engineering Manager JD Score", 0, 100, 60)
    min_az_score = st.slider("Minimum Allison Ziets Similarity Score", 0, 100, 60)

    filtered_df = df[
        (df["Application Engineer JD"] >= min_app_score) &
        (df["Engineering Manager JD"] >= min_mgr_score) &
        (df["Allison Ziets Similarity"] >= min_az_score)
    ]

    st.markdown("### 🎯 Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

conn.close()
