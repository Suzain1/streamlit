import streamlit as st
import json
import os

# File to store user data
USER_FILE = "users.json"

# Function to load users from JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            try:
                return json.load(file)["users"]
            except json.JSONDecodeError:
                return []
    return []

# Function to save users to JSON file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump({"users": users}, file, indent=4)
    push_to_github()  # Automatically push changes to GitHub

# Function to check if username exists
def user_exists(username):
    users = load_users()
    return any(user["username"] == username for user in users)

# Function to authenticate user login
def authenticate(username, password):
    users = load_users()
    return any(user["username"] == username and user["password"] == password for user in users)

# Function to push updated users.json to GitHub
def push_to_github():
    os.system("git config --global user.email 'suzain1894@gmail.com'")
    os.system("git config --global user.name 'Suzain1'")
    os.system("git add users.json")
    os.system('git commit -m "Update users.json with new signup data"')
    os.system("git push https://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@github.com/Suzain1/streamlit.git main") 

# Streamlit UI
st.title("User Authentication System")

# Signup Section
st.subheader("Sign Up")
new_username = st.text_input("Username")
new_password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if user_exists(new_username):
        st.error("Username already exists. Please choose another one.")
    else:
        users = load_users()
        users.append({"username": new_username, "password": new_password})
        save_users(users)
        st.success("Signup successful! You can now log in.")

# Login Section
st.subheader("Log In")
login_username = st.text_input("Login Username")
login_password = st.text_input("Login Password", type="password")

if st.button("Log In"):
    if authenticate(login_username, login_password):
        st.success(f"Welcome, {login_username}!")
    else:
        st.error("Invalid username or password.")

# Debugging: Show stored users (for testing purposes)
if st.button("Show Users (Debug)"):
    st.json({"users": load_users()})



