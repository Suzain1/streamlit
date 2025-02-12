import streamlit as st
import json
import os

# File path for storing user data
USER_FILE = "users.json"

# Load users from JSON file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)["users"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save users to JSON file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump({"users": users}, file, indent=4)
    push_to_github()  # Push updates to GitHub

# Check if user exists
def user_exists(username):
    users = load_users()
    return any(user["username"] == username for user in users)

# Authenticate user login
def authenticate(username, password):
    users = load_users()
    return any(user["username"] == username and user["password"] == password for user in users)

# Push updates to GitHub
def push_to_github():
def push_to_github():
    os.system("git config --global user.email 'suzain1894@gmail.com'")
    os.system("git config --global user.name 'Suzain1'")
    os.system("git add users.json")
    os.system('git commit -m "Update users.json with new signup data"')
    os.system("git push https://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@github.com/Suzain1/streamlit.git main")  


# Streamlit UI
st.title("User Authentication System")

# Tabs for Login and Signup
tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

with tab2:
    st.subheader("Sign Up")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        if user_exists(new_username):
            st.error("Username already exists. Choose another.")
        else:
            users = load_users()
            users.append({"username": new_username, "password": new_password})
            save_users(users)
            st.success("Signup successful! You can now log in.")

# Debugging - Show current users
if st.button("Show Users (Debug)"):
    st.json({"users": load_users()})



