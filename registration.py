import streamlit as st
import sqlite3
import re

def show_register_ui():
    st.subheader("📝 Register")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type='password')
    email = st.text_input("Enter your email")
    phone = st.text_input("Enter your phone number")

    if st.button("Register"):
        if not username or not password or not email or not phone:
            st.warning("Please fill in all fields.")
            return

        # Basic validation
        if not re.match(r'^[6-9]\d{9}$', phone):
            st.warning("Phone number must be 10 digits starting with 6–9.")
            return

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            st.warning("Invalid email format.")
            return

        # Insert into DB
        conn = sqlite3.connect('dbs.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            password TEXT,
                            email TEXT,
                            phone TEXT
                        )''')

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            st.error("User already registered with this email.")
        else:
            cursor.execute("INSERT INTO users (name, password, email, phone) VALUES (?, ?, ?, ?)",
                           (username, password, email, phone))
            conn.commit()
            st.success("✅ Registered successfully! You can now log in.")
        conn.close()
