import streamlit as st
from datetime import date
from app.data.incidents import insert_incident, get_all_incidents

st.set_page_config(page_title="Incidents", layout="wide")

# Auth check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in.")
    st.stop()

st.title("Incidents")

tab1, tab2 = st.tabs(["View Incidents", "Add Incident"])

# ---------------- VIEW ----------------
with tab1:
    df = get_all_incidents()
    st.dataframe(df, use_container_width=True)

# ---------------- ADD NEW ----------------
with tab2:
    inc_date = st.date_input("Date", date.today())
    inc_type = st.text_input("Incident Type")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    status = st.selectbox("Status", ["Open", "Closed"])
    desc = st.text_area("Description")

    if st.button("Save Incident"):
        user = st.session_state.get("username", "system")

        insert_incident(
            inc_date.isoformat(),
            inc_type,
            severity,
            status,
            desc,
            user
        )

        st.success("Incident saved successfully!")