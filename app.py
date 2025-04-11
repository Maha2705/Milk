# app.py

import streamlit as st
import sqlite3
import re
import os
import base64
from navigation import navbar
from Prediction import show_prediction_ui  # Make sure this function is defined in Prediction.py

# Show the top nav
navbar()

# Optional background setup
def add_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string.decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Routing logic
def get_page():
    query_params = st.experimental_get_query_params()
    return query_params.get("p", ["home"])[0].lower()

page = get_page()

# Home Page
if page == "home":
    add_bg_from_local("1.jpg")
    st.title("Welcome to the Smart Milk Packaging System")
    st.write("---")
    st.write("This system uses ML to predict bagasse quality, shelf life, and PLA production.")

# Register Page
elif page == "reg":
    add_bg_from_local("reg.avif")
    st.subheader("📝 Register")

    def create_connection():
        return sqlite3.connect("dbs.db")

    def create_user(conn, user):
        sql = ''' INSERT INTO users(name, password, email, phone) VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()

    def user_exists(conn, email):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        return cur.fetchone() is not None

    def validate_email(email):
        return re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email)

    def validate_phone(phone):
        return re.match(r'^[6-9]\d{9}$', phone)

    conn = create_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL);''')

    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Register"):
        if password == confirm_password:
            if not user_exists(conn, email):
                if validate_email(email) and validate_phone(phone):
                    create_user(conn, (name, password, email, phone))
                    st.success("✅ Registered successfully!")
                    show_prediction_ui()
                else:
                    st.error("Invalid email or phone number!")
            else:
                st.error("User already exists!")
        else:
            st.error("Passwords do not match!")
    conn.close()

# Login Page
elif page == "log":
    add_bg_from_local("login.jpg")
    st.subheader("🔐 Login")

    def validate_user(conn, name, password):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
        return cur.fetchone()

    conn = sqlite3.connect("dbs.db")
    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(conn, name, password)
        if user:
            st.success(f"Welcome, {user[1]} 👋")
            show_prediction_ui()
        else:
            st.error("Invalid username or password")
    conn.close()

# Fallback
else:
    st.error("Page not found ❌")
