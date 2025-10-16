import streamlit as st
from main import main_page
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

email = ''
def login_page():

    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if result.user:
            st.session_state["logged_in"] = True
            st.session_state['email'] = True
            st.rerun()
        else:
            st.error("Invalid email or password")


def signup_page():
    st.title("Sign Up")

    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if new_password == confirm_password:
            result = supabase.auth.sign_up({"email": new_email, "password": new_password})
            if result.user:
                st.success("Account created successfully! Please log in.")

                st.info("📧 Check your inbox for the verification email.")
                st.link_button("Open Gmail", "https://mail.google.com")
                st.link_button("Open Outlook", "https://outlook.live.com")

                st.session_state["page"] = "login"
                # st.rerun()
        else:
            st.error("Passwords do not match")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"


if st.session_state["logged_in"]:
    st.write(f"Have a great day!")
    if st.button("Logout"):
        supabase.auth.sign_out()
        st.session_state["logged_in"] = False
        st.session_state["page"] = "login"
        st.rerun()
    main_page(st.session_state['email'])
else:
    if st.session_state["page"] == "login":
        login_page()
        if st.button("Don't have an account? Sign Up"):
            st.session_state["page"] = "signup"
            st.rerun()
    elif st.session_state["page"] == "signup":
        signup_page()
        if st.button("Already have an account? Login"):
            st.session_state["page"] = "login"
            st.rerun()