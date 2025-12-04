CST1510 – Multi-Domain Intelligence Platform (Week 9 – Streamlit UI)
Student Name: Arundhathi Sivakumar Nair
Student ID: M01089665

This is the Week 9 Streamlit Frontend for my Multi-Domain Intelligence Platform coursework.

In Week 8, I built a SQLite-based backend with:

User authentication

CRUD operations

Data loading from CSVs

Incidents, Datasets & IT Tickets tables

In Week 9, I created a simple Streamlit interface that connects to the Week 8 backend and displays the platform’s data in a graphical format.


1. Homepage (Login + Registration)

Username/password login

Registration using bcrypt hashing

Basic input validation

Error handling for incorrect credentials

Stores login info in st.session_state

Widgets used (based on university labs):

st.text_input()

st.button()

st.tabs()

st.warning() / st.success() / st.error()


2. Dashboard

Shows:

Total number of cyber incidents

Bar charts and tables using Streamlit data display components

Uses pandas + SQLite to fetch real database data

Demonstrates simple analytics

st.metric()

st.dataframe()

st.bar_chart()

st.subheader()

st.columns()


3. Create Incident Page

Allows the user to add a new incident into the database.

Widgets used:

st.date_input()

st.text_input()

st.selectbox()

st.text_area()

st.button()

After submission:

The form calls the Week 8 insert_incident() function

On success - Shows st.success()


Streamlit — frontend interface

SQLite3 — database from Week 8

bcrypt — password hashing

pandas — reading + writing data

Python 3.12


The Streamlit UI directly interacts with the Week 8 backend.


Week 7: Authentication system (file-based)

Week 8: Database system (SQLite + CRUD)

Week 9: Streamlit UI


