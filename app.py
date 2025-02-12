import streamlit as st
import pandas as pd
import os
import time
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import json
import os
# Load environment variables
load_dotenv()

# Initialize AI Chatbot
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.2-90b-vision-preview"  # Replace with a valid model name
)

# Page Configuration
st.set_page_config(
    page_title="Women's Health",
    page_icon="🎀",
    layout="wide",
)

# Custom CSS Styles
st.markdown("""
    <style>
        body {
            background-color: #ffe4e1; /* Light pink background */
        }
        .header {
            text-align: left;
            font-family: Arial, sans-serif;
            font-size: 48px; /* Increased header font size */
            font-weight: bold;
            color: #e012e0;
            margin-bottom: 20px;
        }
        .introduction-box {
            background-color: white;
            border: 2px solid #ffb6c1; /* Soft pink border */
            border-radius: 10px;
            padding: 20px;
            font-family: Arial, sans-serif;
            font-size: 20px; /* Increased text font size */
            color: #4d004d; /* Dark pink text */
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin: 20px auto; /* Center the box horizontally with margin */
            width: 80%;
        }
        h1, h2, h3 {
            font-size: 32px; /* Increased header sizes for h1, h2, h3 */
            color: #4d004d; /* Consistent dark pink color */
        }
        label {
            font-size: 18px; /* Increased font size for labels */
            color: #4d004d; /* Consistent dark pink color */
        }
        .video-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .footer {
            background-color: #ffb6c1; /* Soft pink footer */
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            font-size: 18px; /* Increased footer font size */
            color: #4d004d; /* Dark pink text */
        }
        .centered {
            display: flex;
            justify-content: center;
        }
        .chatbot-container {
            margin-top: 30px;
            padding: 20px;
            background-color: #fce4ec; /* Light pink background for chatbot */
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .sidebar .css-17eq0hr {
            font-size: 20px; /* Increased sidebar font size */
        }
        .stTextInput > div > input {
            font-size: 18px; /* Increased input font size */
        }
        .stButton > button {
            font-size: 18px; /* Increased button font size */
        }
        .stSelectbox > div > div {
            font-size: 18px; /* Increased selectbox font size */
        }
    </style>
""", unsafe_allow_html=True)



# Define the JSON file path
USER_FILE = "users.json"

# Helper function to load user data
def load_users():
    if not os.path.exists(USER_FILE):
        return {}  # Return empty dict if file doesn't exist
    with open(USER_FILE, "r") as file:
        try:
            return json.load(file)  # Load JSON data
        except json.JSONDecodeError:
            return {}  # Return empty if file is corrupted

# Helper function to save user data
def save_user(name, email, password):
    users = load_users()
    if email in users:
        st.warning("User already exists. Please log in.")
    else:
        users[email] = {"name": name, "password": password}
        with open(USER_FILE, "w") as file:
            json.dump(users, file, indent=4)  # Save to JSON
        st.success("User registered successfully! Please log in.")

# Helper function to verify user credentials
def verify_user(email, password):
    users = load_users()
    if email in users and users[email]["password"] == password:
        return users[email]["name"]  # Return user name if authenticated
    return None

# Sidebar Navigation
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "🔑 Login/Signup"
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

# Sidebar Navigation
st.sidebar.title("Navigation")
sections = ["🔑 Login/Signup", "🏠 Home", "🛠 Techniques", "📚 Resources", "📞 Contact", "🤖 AI Assistant"]

if st.session_state["current_page"] != "🔑 Login/Signup":
    selected_page = st.sidebar.radio("Go to", sections, index=sections.index(st.session_state["current_page"]))
    if selected_page != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page

# Login/Signup Page
if st.session_state["current_page"] == "🔑 Login/Signup":
    st.title("Login/Signup")
    action = st.selectbox("Choose Action", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if action == "Signup":
        name = st.text_input("Name")
        if st.button("Sign Up"):
            if not name.strip():
                st.warning("Name cannot be empty.")
            else:
                save_user(name, email, password)

    elif action == "Login":
        if st.button("Log In"):
            user_name = verify_user(email, password)
            if user_name:
                st.session_state["user_name"] = user_name
                st.session_state["current_page"] = "🏠 Home"  # Redirect to Home
            else:
                st.error("Invalid email or password.")

# Home Page
if st.session_state["current_page"] == "🏠 Home":
    user_name = st.session_state.get("user_name", "User")
    st.markdown(f"<h1>Welcome, {user_name}!</h1>", unsafe_allow_html=True)
