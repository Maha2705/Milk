import streamlit as st
import sqlite3

def show_login_ui():
    st.subheader("🔐 Login")

    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type='password')

    if st.button("Login"):
        if not username or not password:
            st.warning("Please enter both username and password.")
            return

        conn = sqlite3.connect('dbs.db')
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            st.success(f"Welcome back, {username}! 🎉 Login successful.")
            st.info("👉 Go to the sidebar and click **Prediction** to continue.")
        else:
            st.error("❌ Invalid username or password.")
