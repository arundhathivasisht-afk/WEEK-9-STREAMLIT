import streamlit as st
import pandas as pd
from app.data.incidents import get_all_incidents

st.set_page_config(page_title="Dashboard", layout="wide")

# --- AUTH CHECK ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first.")
    st.stop()

st.title("Dashboard")

# Load incident data
df = get_all_incidents()

if df.empty:
    st.info("No incidents found.")
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    severity_filter = st.selectbox("Severity", ["All"] + sorted(df["severity"].unique()))

# Apply filter
if severity_filter != "All":
    df = df[df["severity"] == severity_filter]

# --- Metrics ---
col1, col2 = st.columns(2)
col1.metric("Total Incidents", len(df))
col2.metric("Unique Types", df["incident_type"].nunique())

st.divider()

# --- Chart ---
st.subheader("Incidents by Severity")
st.bar_chart(df["severity"].value_counts())

st.subheader("Incident Table")
st.dataframe(df)