import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing, metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Bagasse Quality Prediction", layout="centered")

# Set background
def add_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpg;base64,{encoded});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

add_bg("back.jpg")

st.markdown("<h1 style='color:#d35400;text-align:center;'>Bagasse Quality Prediction</h1>", unsafe_allow_html=True)

# Load data
df = pd.read_csv("bagasse_quality_dataset.csv")
df = df.dropna()

# Label Encoding
label_encoder = preprocessing.LabelEncoder()
df['Quality Classification'] = label_encoder.fit_transform(df['Quality Classification'])

X = df.drop('Quality Classification', axis=1)
y = df['Quality Classification']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Train model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

pca = PCA(n_components=6)
X_train_pca = pca.fit_transform(X_train_scaled)

model = RandomForestClassifier()
model.fit(X_train, y_train)
pred = model.predict(X_test)

acc = metrics.accuracy_score(pred, y_test) * 100

# Save model
with open("model.pickle", "wb") as f:
    pickle.dump(model, f)

# Input form
st.markdown("### Enter the following details to predict quality")

a1 = st.text_input("Sample ID")
a2 = st.text_input("Moisture Content (%)")
a3 = st.text_input("Fiber Length (mm)")
a4 = st.text_input("Pulp Yield (%)")
a5 = st.text_input("Ash Content (%)")
a6 = st.text_input("Fiber Diameter (µm)")
a7 = st.text_input("Sugar Content (%)")
a8 = st.text_input("Lignin Content (%)")

if st.button("Predict Quality"):
    if all([a1, a2, a3, a4, a5, a6, a7, a8]):
        try:
            data = [int(a1), float(a2), float(a3), float(a4), float(a5), float(a6), float(a7), float(a8)]
            result = model.predict([data])[0]
            quality = label_encoder.inverse_transform([result])[0]
            st.success(f"🎯 Predicted Quality: {quality}")
        except Exception as e:
            st.error("Invalid input format. Please enter correct numerical values.")
    else:
        st.warning("Please fill all input fields.")
