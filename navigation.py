import streamlit as st
import sqlite3
import re
import base64
import os
from Prediction import show_prediction_ui  # Ensure show_prediction_ui() is defined in Prediction.py

# 🌟 Top nav links
st.markdown(
    """
    <style>
    .nav-links {
        text-align: right;
        padding: 10px;
    }
    .nav-links a {
        text-decoration: none;
        padding: 8px 15px;
        font-weight: bold;
        color: #d35400;
        border: 1px solid #d35400;
        border-radius: 5px;
        margin-left: 10px;
    }
    .nav-links a:hover {
        background-color: #d35400;
        color: white;
    }
    </style>
    <div class='nav-links'>
        <a href='?p=home'>🏠 Home</a>
        <a href='?p=reg'>📝 Register</a>
        <a href='?p=log'>🔐 Login</a>
    </div>
    """,
    unsafe_allow_html=True
)

# 🔧 Background setup
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

# 🌐 Routing based on ?p=
def navigation():
    return st.query_params.get('p', ['home'])[0].lower()

page = navigation()

# 🏠 HOME PAGE
if page == "home":
    add_bg_from_local("1.jpg")
    st.markdown("<h1 style='text-align:center; color:#d35400;'>Welcome to the Smart Milk Packaging System using Intelligent Packaging & Machine Learning</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<p style='text-align:justify;'>This system integrates intelligent packaging with ML algorithms to predict quality, shelf life, and sustainability of milk packaging options using Bagasse, PLA, and MAP technologies.</p>", unsafe_allow_html=True)

# 📝 REGISTER PAGE
elif page == "reg":
    add_bg_from_local("reg.avif")
    st.markdown("## 📝 Register")

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
                    st.success("✅ Registered successfully! Redirecting to prediction page...")
                    show_prediction_ui()  # Call the ML prediction page
                else:
                    st.error("Invalid email or phone number!")
            else:
                st.error("User already exists!")
        else:
            st.error("Passwords do not match!")
    conn.close()

# 🔐 LOGIN PAGE
elif page == "log":
    add_bg_from_local("login.jpg")
    st.markdown("## 🔐 Login")

    def validate_user(conn, name, password):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
        return cur.fetchone()

    conn = sqlite3.connect("dbs.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT NOT NULL);''')

    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(conn, name, password)
        if user:
            st.success(f"Welcome back, {user[1]}! 🎉")
            show_prediction_ui()  # Call ML prediction function
        else:
            st.error("Invalid credentials.")
    conn.close()

# ❌ PAGE NOT FOUND
else:
    st.warning("⚠️ Page not found. Please use the menu above.")
