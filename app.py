import streamlit as st
import joblib
import sqlite3
import pandas as pd
# Load model and vectorizer
model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# DB Function
def log_to_db(message, prediction):
    conn = sqlite3.connect('spam_logs.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (message, prediction) VALUES (?, ?)", (message, prediction))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("📱 SMS Spam Detector")
user_input = st.text_area("Enter your SMS message:")

if st.button("Predict"):
    if user_input.strip() != "":
        vec_message = vectorizer.transform([user_input])
        prediction = model.predict(vec_message)[0]
        
        st.subheader("Result:")
        label_map = {0: "not spam", 1: "spam"}
        label = label_map.get(prediction, "unknown")
        st.write(f"The message is **{label.upper()}**.")

        
        # Log to DB
        log_to_db(user_input, prediction)
    else:
        st.warning("Please enter a message.")

# Display logs
if st.checkbox("📊 Show Prediction Logs"):
    conn = sqlite3.connect('spam_logs.db')
    df_logs = pd.read_sql_query("SELECT * FROM logs", conn)
    st.dataframe(df_logs)
    conn.close()
