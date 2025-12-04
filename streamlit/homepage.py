import streamlit as st
import sys
from pathlib import Path

# Add project root to PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.services.user_service import register_user, login_user

st.set_page_config(page_title="Login", layout="centered")

# Session defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("User Login")

tab1, tab2 = st.tabs(["Login", "Register"])

# ---------------- LOGIN ----------------
with tab1:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, msg = login_user(username, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error(msg)

# ---------------- REGISTER ----------------
with tab2:
    new_user = st.text_input("New username")
    new_pass = st.text_input("New password", type="password")

    if st.button("Register"):
        success, msg = register_user(new_user, new_pass)

        if success:
            st.success(msg)
        else:
            st.error(msg)